import os
import json
import pandas as pd

from fastapi import FastAPI
from typing import Dict, Tuple, List
from openai import OpenAI
from dotenv import load_dotenv


from config.settings import Settings
from inference import Infer

from models import MLClaimDataRequest, LLMClaimDataRequest


app = FastAPI()
settings = Settings()
load_dotenv()


def build_chatgpt_prompts(record: Dict) -> Tuple[str, str]:
    """
    Returns (system_prompt, user_prompt)
    - system_prompt sets the role and tone
    - user_prompt includes the column meanings + the provided record and asks for the reason
    """
    # Glossary as bullet points
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
def predict(features: List[MLClaimDataRequest]) -> dict:

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
    # print(resp.choices[0].message.content)

    return resp.choices[0].message.content
