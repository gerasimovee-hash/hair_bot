def apply_corrections(data: dict) -> dict:
    # Осветление → высокая пористость
    if data.get("damage") == "bleached":
        data["porosity"] = "high"

    # Кудри → минимум сухость
    if data.get("form") in ["3", "4"] and data.get("length") == "normal":
        data["length"] = "dry"

    return data

