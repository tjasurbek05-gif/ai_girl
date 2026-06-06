import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

_JSON_PATH = Path(__file__).parent.parent / "characters" / "characters.json"


@dataclass
class Scenario:
    id: str
    title: dict
    description: dict
    opening: dict
    gems_cost: int = 0
    photo_file_id: Optional[str] = None


@dataclass
class Character:
    id: str
    name: str
    avatar: str
    tagline: dict
    personality: str
    scenarios: list = field(default_factory=list)
    photo_file_id: Optional[str] = None


def load_characters() -> tuple[list[Character], dict[str, Character]]:
    with _JSON_PATH.open(encoding="utf-8") as f:
        raw = json.load(f)

    characters = []
    for c in raw:
        scenarios = [
            Scenario(
                id=s["id"],
                title=s["title"],
                description=s["description"],
                opening=s["opening"],
                gems_cost=s.get("gems_cost", 0),
                photo_file_id=s.get("photo_file_id"),
            )
            for s in c.get("scenarios", [])
        ]
        characters.append(Character(
            id=c["id"],
            name=c["name"],
            avatar=c["avatar"],
            tagline=c["tagline"],
            personality=c["personality"],
            scenarios=scenarios,
            photo_file_id=c.get("photo_file_id"),
        ))

    return characters, {ch.id: ch for ch in characters}


CHARACTERS, _MAP = load_characters()


def get_character(character_id: str) -> Character | None:
    return _MAP.get(character_id)


def get_scenario(character_id: str, scenario_id: str) -> Scenario | None:
    char = get_character(character_id)
    if not char:
        return None
    return next((s for s in char.scenarios if s.id == scenario_id), None)
