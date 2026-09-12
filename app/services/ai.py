import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ..schemas.grammar import GrammarCheckResponse
from ..schemas.translator import TranslationResponse

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")).aio


async def check_grammar(sentence: str) -> GrammarCheckResponse:
    system_instruction = """
      You are an English grammar checker and English learning assistant.

      Your task is to check the student's English sentence.

      Rules:
      1. Correct grammar, spelling, punctuation, and word usage when necessary.
      2. Keep the original meaning of the sentence.
      3. If the sentence is already correct, keep the corrected answer exactly the same.
      4. Explain the mistakes clearly and briefly in simple English.
      5. Do not add information that is not present in the student's sentence.
      6. The explanation should help an English learner understand the mistake.
    """

    prompt = f"""
      Student sentence: {sentence}
    """

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=GrammarCheckResponse,
        temperature=0.1,
    )

    response = await client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=config,
    )

    parsed = response.parsed

    if parsed is None:
        raise ValueError("AI failed to generate a valid response")

    return parsed


async def translate_text(text: str, target_language: str) -> TranslationResponse:
    system_instruction = """
      You are a professional translator and language learning assistant.

      Your task is to translate the user's text into the requested target language.

      Rules:
      1. Preserve the original meaning accurately.
      2. Use natural and grammatically correct language.
      3. Do not add or remove information.
      4. Preserve the original tone and context when possible.
      5. Return only the translation in the required JSON format.
    """

    prompt = f"""
      Target language: {target_language}
      Text to translate: {text}
    """

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=TranslationResponse,
        temperature=0.1,
    )

    response = await client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=config,
    )

    parsed = response.parsed

    if parsed is None:
        raise ValueError("AI failed to generate a valid translation")

    return parsed


from ..schemas.paraphrase import ParaphraseResponse


async def paraphrase_text(text: str) -> ParaphraseResponse:
    system_instruction = """
      You are an English writing assistant.

      Your task is to paraphrase the user's English text.

      Rules:
      1. Preserve the original meaning.
      2. Do not add or remove important information.
      3. Use different words and sentence structures.
      4. Make the result natural, clear, and grammatically correct.
      5. Keep the original tone and context when possible.
      6. Do not make the text unnecessarily longer.
      7. Return only the paraphrased text in the required JSON format.
    """

    prompt = f"""
      Text to paraphrase: {text}
    """

    config = types.GenerateContentConfig(
      system_instruction=system_instruction,
      response_mime_type="application/json",
      response_schema=ParaphraseResponse,
      temperature=0.3,
    )

    response = await client.models.generate_content(
      model="gemini-3.6-flash",
      contents=prompt,
      config=config,
    )

    parsed = response.parsed

    if parsed is None:
      raise ValueError("AI failed to generate a valid paraphrase")

    return parsed
