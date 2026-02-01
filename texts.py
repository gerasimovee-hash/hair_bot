def format_result(data: dict) -> str:
    return (
        "🔍 Твой тип волос\n\n"
        f"Форма: {data['form']}\n"
        f"Толщина: {data['thickness']}\n"
        f"Густота: {data['density']}\n"
        f"Кожа головы: {data['scalp']}\n"
        f"Длина: {data['length']}\n"
        f"Пористость: {data['porosity']}\n"
        f"Состояние: {data['damage']}\n"
        f"Возраст: {data['age']}"
    )

