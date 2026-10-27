"""
Recommendations, Filtering, and Document Aggregation Module.
Provides helper functions for search, multi-faceted filtering, and document checklist synthesis.
"""

from typing import List, Dict, Any, Optional


def filter_schemes(
    evaluated_schemes: List[Dict[str, Any]],
    query: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    scheme_level: Optional[str] = None,
    occupation: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Apply multi-faceted filters to evaluated scheme results.
    """
    filtered = evaluated_schemes

    if query and query.strip():
        q = query.strip().lower()
        filtered = [
            s for s in filtered
            if q in s.get("scheme_name", "").lower()
            or q in s.get("short_description", "").lower()
            or q in s.get("department", "").lower()
            or q in s.get("category", "").lower()
            or q in s.get("benefits", "").lower()
        ]

    if category and category != "All Categories":
        filtered = [s for s in filtered if s.get("category") == category]

    if status and status != "All Statuses":
        filtered = [s for s in filtered if s.get("status") == status]

    if scheme_level and scheme_level != "All Levels":
        filtered = [s for s in filtered if s.get("scheme_level") == scheme_level]

    if occupation and occupation != "All Occupations":
        occ_lower = occupation.lower()
        # Checks if target beneficiaries or description matches occupation
        filtered = [
            s for s in filtered
            if occ_lower in str(s.get("target_beneficiaries", "")).lower()
            or occ_lower in str(s.get("short_description", "")).lower()
            or "any" in str(s.get("target_beneficiaries", "")).lower()
        ]

    return filtered


def aggregate_document_checklist(schemes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregates all required documents from eligible / relevant schemes into categorized checklist.
    Returns:
    {
        "total_documents": int,
        "categories": {
            "Identity Proof": [{"document": str, "schemes": [str]}],
            "Income & Category Proof": [...],
            "Residence & Domicile": [...],
            "Occupation, Land & Business": [...],
            "Banking & Direct Benefit Transfer": [...]
        }
    }
    """
    doc_to_schemes: Dict[str, List[str]] = {}

    for s in schemes:
        # Include schemes that are potentially eligible, official verification, or more info
        if s.get("status") in [
            "Potentially Eligible",
            "Official Verification Required",
            "More Information Required"
        ]:
            s_name = s.get("scheme_name", "Scheme")
            # Extract short acronym/name
            short_name = s_name.split("(")[0].strip()
            for doc in s.get("required_documents", []):
                doc_clean = doc.strip()
                if doc_clean not in doc_to_schemes:
                    doc_to_schemes[doc_clean] = []
                if short_name not in doc_to_schemes[doc_clean]:
                    doc_to_schemes[doc_clean].append(short_name)

    # Classify documents into clean groups
    categorized: Dict[str, List[Dict[str, Any]]] = {
        "Identity & Personal KYC": [],
        "Banking & Direct Benefit Transfer (DBT)": [],
        "Income, Caste & Social Category": [],
        "Residence & Domicile Proof": [],
        "Occupation, Land, Education & Business Proof": []
    }

    for doc, scheme_list in doc_to_schemes.items():
        doc_lower = doc.lower()
        item = {"document": doc, "schemes": scheme_list}

        if any(w in doc_lower for w in ["bank", "passbook", "dbt", "npci", "ifsc"]):
            categorized["Banking & Direct Benefit Transfer (DBT)"].append(item)
        elif any(w in doc_lower for w in ["income", "caste", "bpl", "ration card", "secc", "family card"]):
            categorized["Income, Caste & Social Category"].append(item)
        elif any(w in doc_lower for w in ["domicile", "residence", "utility bill", "electricity", "lease"]):
            categorized["Residence & Domicile Proof"].append(item)
        elif any(w in doc_lower for w in ["land", "khasra", "khatauni", "marksheet", "student", "admission", "udyam", "vending", "project report", "dpr"]):
            categorized["Occupation, Land, Education & Business Proof"].append(item)
        else:
            categorized["Identity & Personal KYC"].append(item)

    # Remove empty categories
    active_categories = {k: v for k, v in categorized.items() if v}

    return {
        "total_documents": len(doc_to_schemes),
        "categories": active_categories
    }
