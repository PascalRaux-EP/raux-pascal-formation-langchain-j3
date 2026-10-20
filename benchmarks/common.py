"""Cas d'usage commun : un agent, 2 outils, une sortie structurée."""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

QUESTION = (
    "Quelle heure est-il en UTC, et combien font 17 x 23 ? "
    "D'après la documentation interne, combien de jours de télétravail par semaine ?"
)
SYSTEM_PROMPT = (
    "Tu es un assistant concis. Utilise les outils pour les faits précis, "
    "et search_docs pour toute question sur la documentation interne "
    "(cite les fichiers sources), puis réponds de façon structurée."
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
    jours_teletravail: int = Field(description="Jours de télétravail par semaine (documentation)")
    sources: list[str] = Field(description="Noms des fichiers de la documentation utilisés")
    resume: str = Field(description="Une phrase de synthèse")


# Logique métier pure, partagée : chaque framework ne fait que l'enrober.
def utc_now() -> str:
    """Return the current UTC timestamp in ISO format."""
    return datetime.now(tz=timezone.utc).isoformat()


def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


# --- Source documentaire (RAG) -------------------------------------------
# Récupération volontairement simple (recoupement de mots-clés, sans base
# vectorielle) pour que la comparaison porte sur les frameworks d'agents.
CORPUS_DIR = Path(__file__).parent / "corpus"


def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"\w+", text.lower()) if len(w) > 2}


def search_docs(query: str) -> str:
    """Search the internal documentation and return the best matching passages with their source file."""
    q = _tokens(query)
    scored = []
    for path in sorted(CORPUS_DIR.glob("*.md")):
        text = path.read_text()
        scored.append((len(q & _tokens(text)), path.name, text))
    scored.sort(reverse=True)
    best = [f"[{name}]\n{text}" for score, name, text in scored[:2] if score > 0]
    return "\n\n".join(best) or "Aucun document pertinent."
