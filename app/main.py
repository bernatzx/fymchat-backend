from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import grammar, translator, paraphrase

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Englify AI API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", os.getenv("CORS_ORIGINS")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grammar.router)
app.include_router(translator.router)
app.include_router(paraphrase.router)


@app.get("/")
def root():
    return {"message": "FymChat API is running"}
