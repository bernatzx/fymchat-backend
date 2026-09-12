from fastapi import APIRouter

from ..schemas.translator import (
    TranslationRequest,
    TranslationResponse,
)
from ..services.ai import translate_text

router = APIRouter(
    prefix="/translator",
    tags=["Translator"],
)


@router.post(
    "/translate",
    response_model=TranslationResponse,
)
async def translate(
    request: TranslationRequest,
):
    return await translate_text(
        request.text,
        request.target_language,
    )
