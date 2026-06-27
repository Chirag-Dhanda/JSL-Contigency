import logging
import re
from typing import List, Dict
from modules.metadata_engine.service import MetadataEngineService

logger = logging.getLogger("HyperlinkEngine")

class HyperlinkEngineService:
    """
    Scans text (like AI responses) and injects markdown hyperlinks to Enterprise Entities.
    """
    def __init__(self, meta_engine: MetadataEngineService):
        self.meta_engine = meta_engine
        
        # Pre-compute a mapping of lowercase entity names to their IDs for fast replacement.
        # In a real system, this might use a dedicated search index (e.g. ElasticSearch) or a trie.
        self._entity_map: Dict[str, str] = {}
        for entity in self.meta_engine._entities.values():
            self._entity_map[entity.name.lower()] = entity.id
            
        logger.info("Hyperlink Engine Initialized.")

    def inject_hyperlinks(self, text: str) -> str:
        """
        Naive implementation: replaces known entity names with markdown links.
        e.g. "Check the Electric Arc Furnace" -> "Check the [Electric Arc Furnace](/explore/ent-123)"
        """
        # Sort names by length descending to avoid partial matching (e.g. matching "Pump" inside "Pump Station")
        sorted_names = sorted(self._entity_map.keys(), key=len, reverse=True)
        
        linked_text = text
        for name in sorted_names:
            if len(name) < 3: continue # Skip very short names to avoid crazy false positives
            
            # Case-insensitive replacement using regex word boundaries
            pattern = re.compile(rf"\b({re.escape(name)})\b", re.IGNORECASE)
            
            # The replacement string: [Original Text](/explore/entity_id)
            entity_id = self._entity_map[name]
            replacement = rf"[\1](/studio/explore/{entity_id})"
            
            linked_text = pattern.sub(replacement, linked_text)
            
        return linked_text
