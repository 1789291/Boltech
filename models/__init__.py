from typing import Optional, Union
from pydantic import BaseModel, Field


DateLike = Optional[Union[int, str]]

SAMPLE_DEFAULT = {
    "excessFee": 139.0,
    "rrp": 1319.0,
    "balanceRRP": 1319.0,
    "oldBalanceRRP": 1319.0,
    "productName": "NL_MANDATORY_ADLD_1Y_UPFRONT_SMARTPHONE_Q5B5",
    "productDesc": "WUAWEI Care+ Onopzettelijke Schade en Vloeistofschade",
    "coverage": "ADLD",
    "productCode": "NLADLD1247",
    "policyStartDate": 1678320000000,
    "policyEndDate": 1709942400000,
    "policyStatus": "Active",
    "retailerName": None,
    "deviceType": "SMARTPHONES",
    "make": "WUAWEI",
    "model": "WUAWEI-AAA176",
    "purchaseDate": 1678320000000,
    "deviceCost": 0,
    "relationship": "self",
    "channel": "Online Portal",
    "claimType": "Accidental Damage",
    "country": "NL",
    "turnOnOff": 1.0,
    "touchScreen": 0.0,
    "smashed": 0.0,
    "frontCamera": 0.0,
    "backCamera": 0.0,
    "frontOrBackCamera": 0.0,
    "audio": 1.0,
    "mic": 0.0,
    "buttons": 0.0,
    "connection": 0.0,
    "charging": 0.0,
    "other": "kleine scherm werkt nog wel, binnenscherm niet meer",
    "issueDesc": "ik heb *** toestel *** de trap ***** ****** omdat *** *** mijn ipad afgleed ...",
}


class MLClaimDataRequest(BaseModel):
    # order preserved as you wanted
    excessFee: Optional[float] = Field(SAMPLE_DEFAULT["excessFee"])
    rrp: Optional[float] = Field(SAMPLE_DEFAULT["rrp"])
    balanceRRP: Optional[float] = Field(SAMPLE_DEFAULT["balanceRRP"])
    oldBalanceRRP: Optional[float] = Field(SAMPLE_DEFAULT["oldBalanceRRP"])

    productName: Optional[str] = Field(SAMPLE_DEFAULT["productName"])
    productDesc: Optional[str] = Field(SAMPLE_DEFAULT["productDesc"])
    coverage: Optional[str] = Field(SAMPLE_DEFAULT["coverage"])
    productCode: Optional[str] = Field(SAMPLE_DEFAULT["productCode"])

    policyStartDate: DateLike = Field(SAMPLE_DEFAULT["policyStartDate"])
    policyEndDate: DateLike = Field(SAMPLE_DEFAULT["policyEndDate"])

    policyStatus: Optional[str] = Field(SAMPLE_DEFAULT["policyStatus"])
    retailerName: Optional[str] = Field(SAMPLE_DEFAULT["retailerName"])
    deviceType: Optional[str] = Field(SAMPLE_DEFAULT["deviceType"])
    make: Optional[str] = Field(SAMPLE_DEFAULT["make"])
    model: Optional[str] = Field(SAMPLE_DEFAULT["model"])

    purchaseDate: DateLike = Field(SAMPLE_DEFAULT["purchaseDate"])
    deviceCost: Optional[int] = Field(SAMPLE_DEFAULT["deviceCost"])

    relationship: Optional[str] = Field(SAMPLE_DEFAULT["relationship"])
    channel: Optional[str] = Field(SAMPLE_DEFAULT["channel"])
    claimType: Optional[str] = Field(SAMPLE_DEFAULT["claimType"])
    country: Optional[str] = Field(SAMPLE_DEFAULT["country"])

    turnOnOff: Optional[float] = Field(SAMPLE_DEFAULT["turnOnOff"])
    touchScreen: Optional[float] = Field(SAMPLE_DEFAULT["touchScreen"])
    smashed: Optional[float] = Field(SAMPLE_DEFAULT["smashed"])
    frontCamera: Optional[float] = Field(SAMPLE_DEFAULT["frontCamera"])
    backCamera: Optional[float] = Field(SAMPLE_DEFAULT["backCamera"])
    frontOrBackCamera: Optional[float] = Field(SAMPLE_DEFAULT["frontOrBackCamera"])
    audio: Optional[float] = Field(SAMPLE_DEFAULT["audio"])
    mic: Optional[float] = Field(SAMPLE_DEFAULT["mic"])
    buttons: Optional[float] = Field(SAMPLE_DEFAULT["buttons"])
    connection: Optional[float] = Field(SAMPLE_DEFAULT["connection"])
    charging: Optional[float] = Field(SAMPLE_DEFAULT["charging"])

    other: Optional[str] = Field(SAMPLE_DEFAULT["other"])
    issueDesc: Optional[str] = Field(SAMPLE_DEFAULT["issueDesc"])

    # Make FastAPI show this as the example object for the schema
    model_config = {"json_schema_extra": {"example": SAMPLE_DEFAULT}}


SAMPLE_DEFAULT["decision"] = "COMPLETED"


class LLMClaimDataRequest(BaseModel):
    excessFee: Optional[float] = Field(SAMPLE_DEFAULT["excessFee"])
    rrp: Optional[float] = Field(SAMPLE_DEFAULT["rrp"])
    balanceRRP: Optional[float] = Field(SAMPLE_DEFAULT["balanceRRP"])
    oldBalanceRRP: Optional[float] = Field(SAMPLE_DEFAULT["oldBalanceRRP"])

    productName: Optional[str] = Field(SAMPLE_DEFAULT["productName"])
    productDesc: Optional[str] = Field(SAMPLE_DEFAULT["productDesc"])
    coverage: Optional[str] = Field(SAMPLE_DEFAULT["coverage"])
    productCode: Optional[str] = Field(SAMPLE_DEFAULT["productCode"])

    policyStartDate: DateLike = Field(SAMPLE_DEFAULT["policyStartDate"])
    policyEndDate: DateLike = Field(SAMPLE_DEFAULT["policyEndDate"])

    policyStatus: Optional[str] = Field(SAMPLE_DEFAULT["policyStatus"])
    retailerName: Optional[str] = Field(SAMPLE_DEFAULT["retailerName"])
    deviceType: Optional[str] = Field(SAMPLE_DEFAULT["deviceType"])
    make: Optional[str] = Field(SAMPLE_DEFAULT["make"])
    model: Optional[str] = Field(SAMPLE_DEFAULT["model"])

    purchaseDate: DateLike = Field(SAMPLE_DEFAULT["purchaseDate"])
    deviceCost: Optional[int] = Field(SAMPLE_DEFAULT["deviceCost"])

    relationship: Optional[str] = Field(SAMPLE_DEFAULT["relationship"])
    channel: Optional[str] = Field(SAMPLE_DEFAULT["channel"])
    claimType: Optional[str] = Field(SAMPLE_DEFAULT["claimType"])
    country: Optional[str] = Field(SAMPLE_DEFAULT["country"])

    turnOnOff: Optional[float] = Field(SAMPLE_DEFAULT["turnOnOff"])
    touchScreen: Optional[float] = Field(SAMPLE_DEFAULT["touchScreen"])
    smashed: Optional[float] = Field(SAMPLE_DEFAULT["smashed"])
    frontCamera: Optional[float] = Field(SAMPLE_DEFAULT["frontCamera"])
    backCamera: Optional[float] = Field(SAMPLE_DEFAULT["backCamera"])
    frontOrBackCamera: Optional[float] = Field(SAMPLE_DEFAULT["frontOrBackCamera"])
    audio: Optional[float] = Field(SAMPLE_DEFAULT["audio"])
    mic: Optional[float] = Field(SAMPLE_DEFAULT["mic"])
    buttons: Optional[float] = Field(SAMPLE_DEFAULT["buttons"])
    connection: Optional[float] = Field(SAMPLE_DEFAULT["connection"])
    charging: Optional[float] = Field(SAMPLE_DEFAULT["charging"])

    other: Optional[str] = Field(SAMPLE_DEFAULT["other"])
    issueDesc: Optional[str] = Field(SAMPLE_DEFAULT["issueDesc"])
    decision: Optional[str] = Field(SAMPLE_DEFAULT["decision"])

    # FastAPI/Schema docs will show SAMPLE_DEFAULT as example
    model_config = {"json_schema_extra": {"example": SAMPLE_DEFAULT}}
