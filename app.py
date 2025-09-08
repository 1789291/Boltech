# app.py
import os
import json
import pandas as pd

from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import Dict, Tuple, List
from openai import OpenAI
from dotenv import load_dotenv

from config.settings import Settings
from inference import Infer
from preprocess import Preprocessor
from train import Train
from models import MLClaimDataRequest, LLMClaimDataRequest

load_dotenv()
settings = Settings()

ARTIFACTS_DIR = getattr(settings, "artifacts_path", "artifacts")
MODEL_PATH = os.path.join(
    ARTIFACTS_DIR, "model.pkl"
)  # adjust to your trainer’s save path


def prepare_model_on_startup() -> None:
    """
    If model artifact doesn't exist, run the full pipeline:
    read -> preprocess -> train (which should save artifacts to ARTIFACTS_DIR).
    """
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    if not os.path.exists(MODEL_PATH):
        # --- your original startup code ---
        df = pd.read_excel(os.path.join(settings.data_path))
        preprocess = Preprocessor(df)
        df = preprocess.preprocess()

        trainer = Train(df)
        trainer.run()  # make sure this saves to MODEL_PATH (or adjust path above)
        # -----------------------------------
    # else: artifacts already present; nothing to do


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    prepare_model_on_startup()
    yield
    # Shutdown (nothing special)


app = FastAPI(lifespan=lifespan)


def build_chatgpt_prompts(record: Dict) -> Tuple[str, str]:
    glossary_text = "\n".join(
        f"- **{k}**: {v}" for k, v in settings.COLUMN_GLOSSARY.items()
    )

    system_prompt = (
        "You are an impartial insurance claims reviewer. The system has already decided "
        "to COMPLETED or DECLINED each claim. Your job is to explain that decision clearly, "
        "concisely, and defensibly using only the provided fields. Do not re-decide the outcome, "
        "and do not invent facts. If information is missing, say so."
    )

    user_prompt = f"""
You are given:

1) Column meanings:
{glossary_text}

2) The claim record (JSON). It already contains the final decision under "decision".
Use ONLY this data to explain why the claim was accepted or rejected.

```json
{json.dumps(record, ensure_ascii=False, indent=2)}
"""
    return system_prompt, user_prompt


@app.post("/predict")
def predict(features: MLClaimDataRequest) -> dict:
    df = pd.DataFrame([features.model_dump()]).reindex(columns=settings.FIELD_ORDER)
    infer = Infer(df)
    return {"prediction": infer.predict()}


@app.post("/batch-predict")
def batch_predict(features: List[MLClaimDataRequest]) -> dict:
    rows = [f.model_dump() for f in features]
    df = pd.DataFrame(rows).reindex(columns=settings.FIELD_ORDER)
    infer = Infer(df)
    preds = infer.predict()
    return {"predictions": list(preds)}


@app.post("/llm")
def llm(record: LLMClaimDataRequest):
    system_prompt, user_prompt = build_chatgpt_prompts(record=record.model_dump())
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    # Optional: allow running `python app.py` to warm the model once
    prepare_model_on_startup()
    # Typically you'd start via: `uvicorn app:app --host 0.0.0.0 --port 8000`
