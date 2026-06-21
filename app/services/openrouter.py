from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"

TONE_PROMPTS: dict[str, str] = {
    "coach": "You are a direct, no-nonsense coach. Be honest, push them, don't sugarcoat.",
    "guide": "You are a gentle, supportive guide. Be warm, encouraging, and compassionate.",
    "friend": "You are a funny, relatable friend. Be casual, use humor, keep it real.",
}


def _get_tone_system(tone: str) -> str:
    return TONE_PROMPTS.get(tone, TONE_PROMPTS["coach"])


async def call_openrouter(prompt: str, system: str) -> str:
    async with httpx.AsyncClient() as client:
        res = await client.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=30,
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]


async def generate_plan(
    goal_name: str,
    target_amount: float,
    unit: str,
    deadline: str,
    constraints: list[dict[str, Any]],
    tone: str = "coach",
    achieved_so_far: float = 0,
) -> dict[str, Any]:
    system = (
        f"{_get_tone_system(tone)} You are a goal planning expert. "
        "Create a realistic daily plan that fits within the user's constraints. "
        "Return ONLY a JSON object. No other text."
    )

    constraints_text = "\n".join(
        [f"- {c.get('day', 'N/A')}: {c.get('available_hours', '?')}h available" for c in constraints]
    )

    context_line = f"Already achieved: {achieved_so_far} {unit}" if achieved_so_far else "Fresh goal."

    prompt = f"""
Goal: {goal_name}
Target: {target_amount} {unit}
Deadline: {deadline}
{context_line}

User's constraints:
{constraints_text}

Create a day-by-day plan. Return JSON:
{{
  "daily_target": <float>,
  "total_days": <int>,
  "schedule": [{{"day": <int>, "date": "<YYYY-MM-DD>", "target": <float>}}],
  "summary": "<1 sentence plan summary>"
}}
"""

    response = await call_openrouter(prompt, system)
    clean = response.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


async def generate_identity(
    name: str, categories: list[str], goal: str = "", tone: str = "coach"
) -> str:
    system = f"{_get_tone_system(tone)} You are an identity architect for students."
    prompt = f"""
Student name: {name}
Focus areas: {', '.join(categories)}
Personal goal: {goal or 'Not specified'}

Write a 2-3 sentence identity profile in second person (You are...). Be specific, not generic.
"""
    return await call_openrouter(prompt, system)


async def analyze_pace(
    goal_name: str,
    target_amount: float,
    achieved_so_far: float,
    days_elapsed: int,
    total_days: int,
    checkin_history: list[dict[str, Any]],
    tone: str = "coach",
) -> dict[str, Any]:
    system = (
        f"{_get_tone_system(tone)} You are a progress analyst. "
        "Analyze the user's pace and predict their completion date. "
        "Return ONLY a JSON object. No other text."
    )

    history_text = "\n".join(
        [f"- Day {c.get('day', '?')}: {c.get('amount', 0)} {c.get('unit', 'units')}" for c in checkin_history[-10:]]
    )

    prompt = f"""
Goal: {goal_name}
Target: {target_amount}
Achieved so far: {achieved_so_far}
Days elapsed: {days_elapsed} of {total_days}

Recent check-ins:
{history_text}

Analyze pace. Return JSON:
{{
  "predicted_completion_pct": <0-100>,
  "on_track": <bool>,
  "predicted_days_remaining": <int>,
  "today_target": <float>,
  "message": "<1 sentence status>"
}}
"""
    response = await call_openrouter(prompt, system)
    clean = response.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(clean)
