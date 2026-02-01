# content_loader.py
from __future__ import annotations
import yaml

def load_content(path: str = "content.yml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_description(profile: dict, content: dict) -> str:
    form = profile["form"]
    scalp = profile["scalp"]
    length = profile["length"]
    porosity = profile["porosity"]
    damage = profile["damage"]
    age = profile["age"]

    # Блоки текста
    parts: list[str] = []
    parts.append(f'{content["intro"]["title"]}\n')
    parts.append(f'*{content["form"][form]["name"]}*\n')
    parts.append(content["form"][form]["about"])

    labels = content["labels"]

    bullets = [
    f'• {labels["thickness"][profile["thickness"]]}',
    f'• {labels["density"][profile["density"]]}',
    f'• {content["scalp"][scalp]["name"]}',
    f'• {content["length"][length]["name"]}',
    f'• {labels["porosity"][profile["porosity"]]}',
    f'• {labels["damage"][profile["damage"]]}',
    ]

    parts.append(f'\n\n{content["presentation"]["bullets_title"]}\n' + "\n".join(bullets))

    # Рекомендации: соберём из модулей и уберём повторы
    tips = []
    tips += content["form"][form].get("care", [])
    tips += content["scalp"][scalp].get("care", [])
    tips += content["length"][length].get("care", [])
    tips += content["porosity"][porosity].get("care", [])
    tips += content["damage"][damage].get("care", [])

    seen = set()
    tips_unique = []
    for t in tips:
        if t not in seen:
            tips_unique.append(t)
            seen.add(t)

    parts.append(
        f'\n\n{content["presentation"]["tips_title"]}\n'
        + "\n".join(f"• {t}" for t in tips_unique[:8])
    )

    age_note = content["age"][age]["note"]
    parts.append(f"\n\n🧩 Примечание: {age_note}")

    return "\n".join(parts)
