from typing import Dict, List, Optional
import json
import re
import requests
from prompts import SYSTEM_PROMPT, USER_PROMPT


# -------------------------------
# Public entry point
# -------------------------------

def plan_slides(
    text: str,
    guidance: str,
    provider: Optional[str],
    api_key: Optional[str],
    model: Optional[str],
    min_slides: int,
    max_slides: int,
    add_speaker_notes: bool,
) -> Dict:
    """
    Plan the slide deck structure. 
    If provider/api_key is None, use a local heuristic parser.
    Returns a dict: 
    {"slides": [
        {"title": str, "bullets": [str], "notes": Optional[str]}, ...
    ]}
    """

    # ---------------------------
    # Local heuristic fallback
    # ---------------------------
    if provider is None or api_key is None:
        slides = []
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        for i, para in enumerate(paragraphs[:max_slides]):
            slides.append({
                "title": f"Slide {i+1}",
                "bullets": re.split(r"[.;•]\s*", para)[:5],
                "notes": f"Auto-generated notes for slide {i+1}" if add_speaker_notes else None
            })
        return {"slides": slides}

    # ---------------------------
    # External provider (LLM API call)
    # ---------------------------
    try:
        payload = {
            "system": SYSTEM_PROMPT,
            "user": USER_PROMPT.format(
                text=text,
                guidance=guidance,
                min_slides=min_slides,
                max_slides=max_slides,
                add_speaker_notes=add_speaker_notes,
            ),
            "model": model,
        }
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(provider, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        # Expecting model to return JSON with slides
        if "slides" in data:
            return data
        else:
            raise ValueError("Invalid response format from provider")

    except Exception as e:
        raise RuntimeError(f"Failed to plan slides with provider: {e}")
