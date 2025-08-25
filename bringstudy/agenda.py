from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
from typing import List


@dataclass
class Entry:
    """Agenda entry representing an exam, schedule item, or note."""

    title: str
    date: str
    category: str = "note"
    description: str = ""


class Agenda:
    """Persist agenda entries to a local JSON file."""

    def __init__(self, storage_path: Path | None = None) -> None:
        if storage_path is None:
            storage_path = Path.home() / ".local" / "share" / "BringStudy"
        self.storage_dir = storage_path
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.storage_dir / "agenda.json"
        if not self.file.exists():
            self._save([])

    def _load(self) -> List[Entry]:
        with self.file.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return [Entry(**item) for item in data]

    def _save(self, entries: List[Entry]) -> None:
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump([asdict(e) for e in entries], fh, indent=2)

    def add_entry(self, entry: Entry) -> None:
        entries = self._load()
        entries.append(entry)
        self._save(entries)

    def list_entries(self) -> List[Entry]:
        return self._load()
