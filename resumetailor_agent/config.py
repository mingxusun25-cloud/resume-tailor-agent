from __future__ import annotations

import os

from pydantic import BaseModel


class AppConfig(BaseModel):
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = ""
    llm_timeout_seconds: float = 20.0
    retrieval_mode: str = "hybrid"
    embedding_backend: str = "local"
    embedding_dimensions: int = 64

    @property
    def llm_enabled(self) -> bool:
        return bool(self.openai_api_key and self.openai_model)

    @property
    def mode(self) -> str:
        return "llm" if self.llm_enabled else "rule"

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            openai_model=os.getenv("OPENAI_MODEL", ""),
            retrieval_mode=os.getenv("RETRIEVAL_MODE", "hybrid"),
            embedding_backend=os.getenv("EMBEDDING_BACKEND", "local"),
            embedding_dimensions=int(os.getenv("EMBEDDING_DIMENSIONS", "64")),
        )
