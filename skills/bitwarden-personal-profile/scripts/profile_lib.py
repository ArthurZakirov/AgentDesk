from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_PATH = Path.home() / ".config" / "AgentDesk" / "personal-profile.yaml"


def profile_path(path: str | None = None) -> Path:
    return Path(path or os.environ.get("ADC_PERSONAL_PROFILE_PATH", DEFAULT_PATH)).expanduser()


def load_profile(path: str | None = None) -> dict[str, Any]:
    source = profile_path(path)
    if not source.exists():
        raise SystemExit(f"Profile file not found: {source}")
    text = source.read_text(encoding="utf-8")
    if source.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("YAML profiles require PyYAML. Install with: python3 -m pip install PyYAML") from exc
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise SystemExit("Profile root must be a mapping/object")
    return data


def language_value(value: Any, language: str = "en") -> Any:
    if not isinstance(value, dict):
        return value
    if language in value:
        return value[language]
    if "default" in value:
        return value["default"]
    if "en" in value:
        return value["en"]
    if "de" in value:
        return value["de"]
    return value


def normalize_language_values(value: Any, language: str = "en") -> Any:
    if isinstance(value, list):
        return [normalize_language_values(v, language) for v in value]
    if isinstance(value, dict):
        keys = set(value)
        if keys <= {"default", "de", "en"} and any(k in value for k in ("default", "de", "en")):
            return language_value(value, language)
        return {k: normalize_language_values(v, language) for k, v in value.items()}
    return value


def validate_profile(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must be 1")
    person = data.get("person")
    if not isinstance(person, dict):
        errors.append("person must be an object")
    else:
        for key in ("givenName", "familyName", "name"):
            if not person.get(key):
                errors.append(f"person.{key} is required")
        birth_date = person.get("birthDate")
        if birth_date and not _is_iso_date(str(birth_date)):
            errors.append("person.birthDate must be YYYY-MM-DD")
    contact = data.get("contact")
    if not isinstance(contact, dict):
        errors.append("contact must be an object")
    employment = data.get("employment")
    if isinstance(employment, dict):
        employer = employment.get("employer")
        if isinstance(employer, dict):
            employed_since = employer.get("employedSince")
            if employed_since and not _is_iso_date(str(employed_since)):
                errors.append("employment.employer.employedSince must be YYYY-MM-DD")
    return errors


def _is_iso_date(value: str) -> bool:
    parts = value.split("-")
    return (
        len(parts) == 3
        and len(parts[0]) == 4
        and len(parts[1]) == 2
        and len(parts[2]) == 2
        and all(part.isdigit() for part in parts)
    )
