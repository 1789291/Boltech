import os
import toml


class Settings:

    def __init__(self):

        config_dir = os.path.dirname(__file__)
        config_path = os.path.join(config_dir, "config.toml")

        with open(config_path, "r") as file:
            config = toml.load(file)

        self.data_path = config["path"]["data_path"]
        self.model_save_path = config["path"]["model_save_path"]
        self.test_size = config["data"]["test_size"]
        self.random_state = config["random_state"]["seed"]

        self.drop_cols = config["columns"]["drop"]
        self.datetime_cols = config["columns"]["datetime"]
        self.binary_cols = config["columns"]["binary"]
        self.continous_cols = config["columns"]["continuous"]
        self.category_cols = config["columns"]["category"]
        self.target_col = config["columns"]["target"]

        self.target_mapping = dict(
            zip(config["target"]["keys"], config["target"]["values"])
        )

        self.FIELD_ORDER = [
            "excessFee",
            "rrp",
            "balanceRRP",
            "oldBalanceRRP",
            "productName",
            "productDesc",
            "coverage",
            "productCode",
            "policyStartDate",
            "policyEndDate",
            "policyStatus",
            "retailerName",
            "deviceType",
            "make",
            "model",
            "purchaseDate",
            "deviceCost",
            "relationship",
            "channel",
            "claimType",
            "country",
            "turnOnOff",
            "touchScreen",
            "smashed",
            "frontCamera",
            "backCamera",
            "frontOrBackCamera",
            "audio",
            "mic",
            "buttons",
            "connection",
            "charging",
            "other",
            "issueDesc",
        ]

        self.COLUMN_GLOSSARY = {
            "excessFee": "Customer deductible applied to approved claims.",
            "rrp": "Device recommended retail price at purchase.",
            "balanceRRP": "RRP remaining/used for pricing or settlement.",
            "oldBalanceRRP": "Previous RRP balance.",
            "productName": "Internal product plan name (market/coverage/term/type).",
            "productDesc": "Human-readable description of the plan/coverage.",
            "coverage": "Coverage code (e.g., ADLD = Accidental Damage; ADLD/THEFT = Accidental Damage + Theft).",
            "productCode": "Internal product identifier/code.",
            "policyStartDate": "Policy start date (epoch ms or dd/mm/yyyy).",
            "policyEndDate": "Policy end date (epoch ms or dd/mm/yyyy).",
            "policyStatus": "Policy state (Active, Cancelled, Lapsed).",
            "retailerName": "Retail channel or merchant.",
            "deviceType": "Device category (SMARTPHONES, WEARABLES, etc.).",
            "make": "Device manufacturer.",
            "model": "Device model identifier.",
            "purchaseDate": "Device purchase date (epoch ms or dd/mm/yyyy).",
            "deviceCost": "Cash price paid for the device (if known).",
            "relationship": "Relationship of claimant to owner (e.g., self).",
            "channel": "Claim submission channel.",
            "claimType": "Declared claim cause/type (e.g., Accidental Damage, Theft).",
            "country": "Country/market of cover/claim.",
            "turnOnOff": "Triage: device powers on/off (1=yes, 0=no).",
            "touchScreen": "Triage: touchscreen working (1=yes, 0=no).",
            "smashed": "Triage: screen/body visibly smashed (1=yes, 0=no).",
            "frontCamera": "Triage: front camera working (1=yes, 0=no).",
            "backCamera": "Triage: rear camera working (1=yes, 0=no).",
            "frontOrBackCamera": "Triage: any camera working (1=yes, 0=no).",
            "audio": "Triage: audio working (1=yes, 0=no).",
            "mic": "Triage: microphone working (1=yes, 0=no).",
            "buttons": "Triage: buttons working (1=yes, 0=no).",
            "connection": "Triage: connectivity working (1=yes, 0=no).",
            "charging": "Triage: charging works (1=yes, 0=no).",
            "other": "Short free-text summary of the issue.",
            "issueDesc": "Long free-text narrative of the incident/issue.",
            "decision": "Final decision already made by your system (COMPLETED/DECLINED).",
        }
