from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class ImageMetadata:
    name: str
    format: str
    size: tuple
    created_at: Optional[str]
    location: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return asdict(self)
