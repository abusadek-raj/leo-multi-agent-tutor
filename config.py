
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")


# ============================================================
# CrewAI + Groq compatibility fix
# ============================================================
# CrewAI 1.15.x adds "cache_breakpoint" to agent messages.
# Groq does not accept this field.
#
# IMPORTANT:
# This patch MUST happen BEFORE creating the CrewAI LLM.
# ============================================================

import crewai.llms.cache as crew_cache

crew_cache.mark_cache_breakpoint = lambda msg: msg


# ============================================================
# Create CrewAI LLM
# ============================================================

from crewai import LLM

llm = LLM(
    model="groq/openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0.3
)