import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ..schemas.grammar import GrammarCheckResponse
from ..schemas.translator import TranslationResponse
from ..schemas.paraphrase import ParaphraseResponse

load_dotenv()

MODEL = "gemini-3.6-flash"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")).aio


async def _generate(
    *,
    prompt: str,
    system_instruction: str,
    response_schema,
    temperature: float = 0.1,
):
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=response_schema,
        temperature=temperature,
    )

    response = await client.models.generate_content(
        model=MODEL, contents=prompt, config=config
    )

    parsed = response.parsed

    if parsed is None:
        raise ValueError("Ai failed to generate a valid response")

    return parsed


async def check_grammar(sentence: str) -> GrammarCheckResponse:
    system_instruction = """
      You are an English grammar checker and learning assistant.

      Check the student's sentence for grammar, spelling, punctuation, and word choice.

      Rules:
      1. Preserve the original meaning.
      2. Make only necessary corrections.
      3. IIf already correct, keep it unchanged.
      4. Explain errors briefly in simple English.
      5. Do not add information.
    """

    prompt = f"""
      Student sentence: {sentence}
    """

    return await _generate(
        prompt=prompt,
        system_instruction=system_instruction,
        response_schema=GrammarCheckResponse,
    )


async def translate_text(text: str, target_language: str) -> TranslationResponse:
    system_instruction = """
      You are a professional translator.

      Translate the text into the requested target language.

      Rules:
      1. Preserve the exact meaning, tone, and context.
      2. Do not add, remove, or interpret information.
      3. Use natural and grammatically correct language.
    """

    prompt = f"""
      Target language: {target_language}
      Text to translate: {text}
    """

    return await _generate(
        prompt=prompt,
        system_instruction=system_instruction,
        response_schema=TranslationResponse,
    )


async def paraphrase_text(text: str) -> ParaphraseResponse:
    system_instruction = """
      You are an English writing assistant.

      Paraphrase the user's English text.

      Rules:
      1. Preserve the original meaning and important information.
      2. Use different wording and sentence structure.
      3. Keep the same tone and context.
      4. Make it natural, clear, and concise.
      5. Do not unnecessarily lengthen the text.
    """

    prompt = f"""
      Text to paraphrase: {text}
    """

    return await _generate(
        prompt=prompt,
        system_instruction=system_instruction,
        response_schema=ParaphraseResponse,
        temperature=0.3,
    )
