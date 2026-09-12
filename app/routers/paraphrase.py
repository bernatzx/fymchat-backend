from fastapi import APIRouter

from ..schemas.paraphrase import (
    ParaphraseRequest,
    ParaphraseResponse,
)
from ..services.ai import paraphrase_text

router = APIRouter(
    prefix="/paraphrase",
    tags=["Paraphrase"],
)


@router.post(
    "/",
    response_model=ParaphraseResponse,
)
async def paraphrase(
    request: ParaphraseRequest,
):
    return await paraphrase_text(request.text)
