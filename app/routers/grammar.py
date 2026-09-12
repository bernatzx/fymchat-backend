from fastapi import APIRouter

from ..schemas.grammar import (
    GrammarCheckRequest,
    GrammarCheckResponse,
)

from ..services.ai import check_grammar

router = APIRouter(
    prefix="/grammar",
    tags=["Grammar"],
)


@router.post("/check", response_model=GrammarCheckResponse)
async def grammar_check(req: GrammarCheckRequest):
    return await check_grammar(req.sentence)
