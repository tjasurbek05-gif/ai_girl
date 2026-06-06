"""
DeepSeek API client.
Pure transport layer — knows nothing about characters or scenarios.
"""

import logging
from openai import AsyncOpenAI, APIError
from config import config

logger = logging.getLogger(__name__)

# Lazy-initialised so the module can be imported without a live API key.
_client: AsyncOpenAI | None = None

# How many past messages to keep in context (user + assistant pairs).
MAX_HISTORY_MESSAGES = 30


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        )
    return _client


async def chat_completion(
    system_prompt: str,
    history: list[dict],
    user_message: str,
    *,
    max_tokens: int = 350,
    temperature: float = 0.92,
) -> str | None:
    """
    Send a chat completion request to DeepSeek.

    Args:
        system_prompt: The character's full system prompt.
        history:       Previous [{"role": ..., "content": ...}] turns.
        user_message:  The latest user input.
        max_tokens:    Maximum tokens in the reply.
        temperature:   Sampling temperature (higher = more creative).

    Returns:
        The model's reply string, or None on any error.
    """
    trimmed = history[-MAX_HISTORY_MESSAGES:]

    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    messages.extend(trimmed)
    messages.append({"role": "user", "content": user_message})

    try:
        response = await _get_client().chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            frequency_penalty=0.3,
        )
        return response.choices[0].message.content.strip()

    except APIError as exc:
        logger.error("DeepSeek API error: %s", exc)
        return None
    except Exception as exc:
        logger.exception("Unexpected error calling DeepSeek: %s", exc)
        return None
