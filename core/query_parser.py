import re
from typing import Dict, List

class QueryParser:
    """
    Parses raw, unstructured text inputs from users to extract
    context-aware attributes like tone, pacing, and core thematic entities.
    """
    def __init__(self, tone_options: List[str], pacing_options: List[str]):
        self.tone_options = tone_options
        self.pacing_options = pacing_options

    def parse_prompt(self, prompt: str) -> Dict[str, any]:
        lowered = prompt.lower()
        
        # Rule-based entity matching for implicit metadata clues
        detected_tones = [t for t in self.tone_options if t.lower() in lowered]
        detected_pacing = [p for p in self.pacing_options if p.lower() in lowered]
        
        # Tokenize and extract key descriptive nouns/verbs, stripping standard NLP clutter
        keywords = set(re.findall(r'\b\w{4,}\b', lowered))
        stop_clues = {"story", "book", "about", "read", "novel", "plot", "like", "find"}
        keywords = keywords - stop_clues
        
        return {
            "clean_query": prompt,
            "tones": detected_tones,
            "pacing": detected_pacing,
            "keywords": keywords
        }