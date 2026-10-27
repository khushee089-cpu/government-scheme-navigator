"""
Data Loader Module for Government Scheme Navigator.
Handles loading, caching, schema validation, and retrieval of scheme records.
"""

import json
import os
from typing import List, Dict, Any, Optional, Tuple

DEFAULT_SCHEME_PATHS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "schemes.json"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "schemes.json"),
    "schemes.json",
    "data/schemes.json"
]

REQUIRED_SCHEME_FIELDS = [
    "id",
    "name",
    "department",
    "scheme_level",
    "category",
    "target_beneficiaries",
    "short_description",
    "benefits",
    "eligibility_rules",
    "required_documents",
    "official_information_url",
    "last_verification_date",
    "data_verification_status"
]


def find_scheme_file() -> Optional[str]:
    """Locate the schemes.json file from known possible locations."""
    for path in DEFAULT_SCHEME_PATHS:
        if os.path.exists(path) and os.path.isfile(path):
            return os.path.abspath(path)
    return None


def validate_scheme_record(scheme: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate a single scheme dictionary against required fields and structure.
    Returns (is_valid, error_message).
    """
    if not isinstance(scheme, dict):
        return False, "Scheme record is not a dictionary."

    for field in REQUIRED_SCHEME_FIELDS:
        if field not in scheme:
            return False, f"Missing required field: '{field}' in scheme ID {scheme.get('id', 'UNKNOWN')}."

    rules = scheme.get("eligibility_rules")
    if not isinstance(rules, dict):
        return False, f"eligibility_rules must be a dict in scheme ID {scheme.get('id')}."

    if not isinstance(scheme.get("required_documents"), list):
        return False, f"required_documents must be a list in scheme ID {scheme.get('id')}."

    return True, "Valid"


def load_schemes(filepath: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load schemes from JSON file.
    If filepath is None, searches in default locations.
    Raises FileNotFoundError or ValueError if invalid.
    """
    resolved_path = filepath if filepath else find_scheme_file()

    if not resolved_path or not os.path.exists(resolved_path):
        raise FileNotFoundError(
            f"Scheme database file could not be found. Checked paths: {DEFAULT_SCHEME_PATHS}"
        )

    try:
        with open(resolved_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Corrupted or invalid JSON in {resolved_path}: {exc}") from exc
    except Exception as exc:
        raise IOError(f"Error reading {resolved_path}: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError(f"Expected a list of schemes in {resolved_path}, got {type(data).__name__}.")

    valid_schemes = []
    for item in data:
        is_valid, msg = validate_scheme_record(item)
        if is_valid:
            valid_schemes.append(item)
        else:
            # We log or skip but do not completely crash if one item has a minor schema flaw
            continue

    if not valid_schemes:
        raise ValueError(f"No valid schemes loaded from {resolved_path}.")

    return valid_schemes


def get_scheme_by_id(scheme_id: str, schemes: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    """Retrieve a single scheme record by its unique ID."""
    if schemes is None:
        schemes = load_schemes()
    for s in schemes:
        if s.get("id") == scheme_id:
            return s
    return None


def get_categories(schemes: List[Dict[str, Any]]) -> List[str]:
    """Return sorted unique list of scheme categories."""
    cats = {s.get("category", "General") for s in schemes if s.get("category")}
    return sorted(list(cats))


def get_all_departments(schemes: List[Dict[str, Any]]) -> List[str]:
    """Return sorted unique list of scheme departments/ministries."""
    depts = {s.get("department") for s in schemes if s.get("department")}
    return sorted(list(depts))
