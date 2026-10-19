"""Cas d'usage commun : un agent, 2 outils, une sortie structurée."""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

QUESTION = "Quelle heure est-il en UTC, et combien font 17 x 23 ?"
SYSTEM_PROMPT = (
    "Tu es un assistant concis. Utilise les outils pour les faits précis, "
    "puis réponds de façon structurée."
)

# Modèle via OpenRouter (LangChain, PydanticAI, Haystack)
OPENROUTER_MODEL = "openai/gpt-4.1-mini"
OPENROUTER_URL = "https://openrouter.ai/api/v1"


def openrouter_key() -> str:
    return os.environ["OPENROUTER_API_KEY"]


class Reponse(BaseModel):
    """Sortie structurée attendue, identique pour tous les frameworks."""

    heure_utc: str = Field(description="Heure UTC au format ISO")
    produit: int = Field(description="Résultat de la multiplication")
    resume: str = Field(description="Une phrase de synthèse")


# Logique métier pure, partagée : chaque framework ne fait que l'enrober.
def utc_now() -> str:
    """Return the current UTC timestamp in ISO format."""
    return datetime.now(tz=timezone.utc).isoformat()


def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b
