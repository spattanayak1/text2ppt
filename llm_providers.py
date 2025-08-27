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
"""Plan the slide deck structure. If provider/api_key is None, use a local heuristic parser.
Returns a dict: {"slides": [{"title": str, "bullets": [str], "notes": Optional[str]} ...]}
