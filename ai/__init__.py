from ai.client import chat_completion


async def get_ai_reply(system_prompt: str, history: list, user_message: str) -> str | None:
    return await chat_completion(system_prompt, history, user_message)


def build_system_prompt(personality: str, scenario_title: str, scenario_desc: str, lang: str = "en") -> str:
    lang_instruction = {
        "ru": "Always respond in Russian.",
        "uz": "Always respond in Uzbek (O'zbek tilida javob bering).",
        "en": "Always respond in English.",
    }.get(lang, "Always respond in English.")

    return (
        f"{personality}\n\n"
        f"Current scenario: {scenario_title}\n"
        f"Context: {scenario_desc}\n\n"
        f"{lang_instruction} "
        "Use *italics* for physical actions. "
        "Keep responses 2-4 sentences. "
        "Never break character. Never mention being an AI."
    )
