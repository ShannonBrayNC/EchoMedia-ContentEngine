"""Production adapter contracts and registry for EchoMedia Ad Studio.

This module closes the adapter plumbing portion of EMAS-001 for the RC lane.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class AdapterRegistryError(RuntimeError):
    pass


class AdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, object] = {}

    def register(self, name: str, adapter: object) -> None:
        if name in self._adapters:
            raise AdapterRegistryError(f"Adapter already registered: {name}")
        self._adapters[name] = adapter

    def get(self, name: str):
        if name not in self._adapters:
            raise AdapterRegistryError(f"Adapter not registered: {name}")
        return self._adapters[name]


@dataclass(frozen=True)
class SavedAsset:
    asset_id: str
    path: str
    size_bytes: int


class StorageAdapter(Protocol):
    def save_asset(self, source_path: str | Path, destination_path: str | Path) -> SavedAsset:
        ...

    def read_text(self, path: str | Path) -> str:
        ...

    def write_text(self, path: str | Path, content: str) -> None:
        ...

    def exists(self, path: str | Path) -> bool:
        ...


class LocalFilesystemStorageAdapter:
    """Production RC filesystem adapter.

    It intentionally uses local paths so CI and local development can run without cloud secrets.
    A future Azure Blob adapter should implement the same protocol.
    """

    def __init__(self, root_path: str | Path = ".") -> None:
        self.root_path = Path(root_path)

    def resolve(self, path: str | Path) -> Path:
        candidate = self.root_path / Path(path)
        resolved_root = self.root_path.resolve()
        resolved_candidate = candidate.resolve()
        if not str(resolved_candidate).startswith(str(resolved_root)):
            raise ValueError(f"Path escapes storage root: {path}")
        return resolved_candidate

    def save_asset(self, source_path: str | Path, destination_path: str | Path) -> SavedAsset:
        source = Path(source_path)
        destination = self.resolve(destination_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return SavedAsset(asset_id=destination.stem, path=str(destination), size_bytes=destination.stat().st_size)

    def read_text(self, path: str | Path) -> str:
        return self.resolve(path).read_text(encoding="utf-8")

    def write_text(self, path: str | Path, content: str) -> None:
        destination = self.resolve(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    def exists(self, path: str | Path) -> bool:
        return self.resolve(path).exists()


class ImageGenerationAdapter(Protocol):
    name: str

    def generate(self, request: dict) -> dict:
        ...


class NoProviderImageGenerationAdapter:
    """Safe no-provider adapter for tests and CI.

    It does not call paid providers. It returns a deterministic draft artifact descriptor.
    """

    name = "no-provider"

    def generate(self, request: dict) -> dict:
        if not request.get("sourceRegistryVerified"):
            raise ValueError("Generation requires source-registry consent verification.")
        return {
            "provider": self.name,
            "state": "draft",
            "outputId": request.get("outputId") or "draft-output",
            "message": "No-provider mode generated a draft descriptor only.",
        }


class AdapterConfig:
    @staticmethod
    def load(path: str | Path) -> dict:
        config_path = Path(path)
        if not config_path.exists():
            return {}
        return json.loads(config_path.read_text(encoding="utf-8"))


def build_default_registry(root_path: str | Path = ".") -> AdapterRegistry:
    registry = AdapterRegistry()
    registry.register("local-filesystem", LocalFilesystemStorageAdapter(root_path=root_path))
    registry.register("no-provider", NoProviderImageGenerationAdapter())
    return registry
