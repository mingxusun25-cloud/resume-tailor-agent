from __future__ import annotations

import json
import re
from pathlib import Path

from resumetailor_agent.schemas import MaterialChunk


SUPPORTED_SUFFIXES = {".md", ".txt", ".json"}


def _extract_title(path: Path, content: str) -> str:
    for line in content.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return path.stem.replace("_", " ").strip() or "Untitled Material"


def _read_text(path: Path) -> str:
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False, indent=2)
        return json.dumps(data, ensure_ascii=False)
    return path.read_text(encoding="utf-8")


def _split_into_paragraphs(path: Path, raw_text: str) -> list[str]:
    if path.suffix.lower() == ".json":
        return [raw_text]

    body_lines = raw_text.splitlines()
    if body_lines and body_lines[0].startswith("#"):
        body_lines = body_lines[1:]

    body_text = "\n".join(body_lines).strip()
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body_text) if part.strip()]
    return paragraphs or [raw_text]


def load_material_chunks(materials_dir: Path) -> list[MaterialChunk]:
    chunks: list[MaterialChunk] = []

    for path in sorted(materials_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue

        raw_text = _read_text(path).strip()
        if not raw_text:
            continue

        title = _extract_title(path, raw_text)
        paragraphs = _split_into_paragraphs(path, raw_text)

        for index, paragraph in enumerate(paragraphs, start=1):
            chunks.append(
                MaterialChunk(
                    id=f"{path.stem}-{index}",
                    title=title,
                    type="material",
                    source_file=str(path),
                    raw_text=paragraph,
                    tags=[],
                    summary=paragraph.splitlines()[0][:120],
                )
            )

    return chunks
