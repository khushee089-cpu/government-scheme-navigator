"""
Rule-Based Eligibility Engine for Government Scheme Navigator.
Evaluates user profile against structured scheme rules deterministically.
"""

from typing import Dict, Any, List, Optional, Tuple


class EligibilityResult:
    """Represents the evaluation outcome for a scheme against a user profile."""

    STATUS_POTENTIALLY_ELIGIBLE = "Potentially Eligible"
    STATUS_MORE_INFO_REQUIRED = "More Information Required"
    STATUS_LIKELY_INELIGIBLE = "Likely Ineligible Under Listed Rules"
    STATUS_OFFICIAL_VERIFICATION = "Official Verification Required"

    def __init__(
        self,
        scheme_id: str,
        scheme_name: str,
        status: str,
        relevance_score: int,
        satisfied_conditions: List[Dict[str, Any]],
        unsatisfied_conditions: List[Dict[str, Any]],
        information_required: List[Dict[str, Any]],
        notes: Optional[str] = None
    ):
        self.scheme_id = scheme_id
        self.scheme_name = scheme_name
        self.status = status
        self.relevance_score = max(0, min(100, relevance_score))
        self.satisfied_conditions = satisfied_conditions
        self.unsatisfied_conditions = unsatisfied_conditions
        self.information_required = information_required
        self.notes = notes or ""
        self.score_disclaimer = (
            "Internal ranking score is used exclusively for sorting relevant schemes "
            "and does NOT represent approval probability or guarantee of benefits."
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scheme_id": self.scheme_id,
            "scheme_name": self.scheme_name,
            "status": self.status,
            "relevance_score": self.relevance_score,
            "score_disclaimer": self.score_disclaimer,
            "satisfied_conditions": self.satisfied_conditions,
            "unsatisfied_conditions": self.unsatisfied_conditions,
            "information_required": self.information_required,
            "notes": self.notes
        }


def normalize_str(val: Any) -> str:
    """Safely convert value to trimmed lowercase string."""
    if val is None:
        return ""
    return str(val).strip().lower()


def evaluate_scheme(user_profile: Dict[str, Any], scheme: Dict[str, Any]) -> EligibilityResult:
    """
    Evaluates a single user profile against a specific scheme's rules.
    Returns an EligibilityResult with fine-grained condition breakdowns.
    """
    rules = scheme.get("eligibility_rules", {})
    scheme_id = scheme.get("id", "UNKNOWN")
    scheme_name = scheme.get("name", "Unknown Scheme")
    scheme_level = scheme.get("scheme_level", "Central")

    satisfied: List[Dict[str, Any]] = []
    unsatisfied: List[Dict[str, Any]] = []
    info_needed: List[Dict[str, Any]] = []

    # Score counters for internal sorting
    relevance_points = 50

    # -------------------------------------------------------------
    # 1. State / Geographic Restriction
    # -------------------------------------------------------------
    user_state = normalize_str(user_profile.get("state"))
    allowed_states = [normalize_str(s) for s in rules.get("allowed_states", ["all"])]

    if "all" in allowed_states or scheme_level.lower() == "central":
        satisfied.append({
            "rule": "Geographic Applicability",
            "detail": f"Applicable nationwide across all States & UTs (Scheme Level: {scheme_level}).",
            "user_val": user_profile.get("state") or "Any"
        })
        relevance_points += 5
    else:
        if not user_state:
            info_needed.append({
                "rule": "State Domicile",
                "detail": f"This state-specific scheme is restricted to: {', '.join(rules.get('allowed_states', []))}.",
                "action": "Please specify your state of residence."
            })
        elif any(user_state == s for s in allowed_states):
            satisfied.append({
                "rule": "State Domicile",
                "detail": f"User is a resident of {user_profile.get('state')}, which matches scheme requirements.",
                "user_val": user_profile.get("state")
            })
            relevance_points += 15
        else:
            unsatisfied.append({
                "rule": "State Restriction",
                "detail": f"Scheme is restricted to {', '.join(rules.get('allowed_states', []))}.",
                "user_val": user_profile.get("state"),
                "reason": f"Resident of {user_profile.get('state')} is not eligible for this state scheme."
            })

    # -------------------------------------------------------------
    # 2. Age Checks (min_age and max_age)
    # -------------------------------------------------------------
    user_age = user_profile.get("age")
    min_age = rules.get("min_age")
    max_age = rules.get("max_age")

    if user_age is not None and str(user_age).isdigit() and int(user_age) > 0:
        age_val = int(user_age)
        age_passed = True

        if min_age is not None and age_val < min_age:
            age_passed = False
            unsatisfied.append({
                "rule": "Minimum Age",
                "detail": f"Minimum required age is {min_age} years.",
                "user_val": f"{age_val} years",
                "reason": f"Age ({age_val}) is below minimum requirement of {min_age} years."
            })

        if max_age is not None and age_val > max_age:
            age_passed = False
            unsatisfied.append({
                "rule": "Maximum Age",
                "detail": f"Maximum allowable age is {max_age} years.",
                "user_val": f"{age_val} years",
                "reason": f"Age ({age_val}) exceeds maximum threshold of {max_age} years."
            })

        if age_passed:
            age_desc = "Age within permissible range"
            if min_age is not None and max_age is not None:
                age_desc = f"Age ({age_val}) falls within allowed range ({min_age} - {max_age} years)."
            elif min_age is not None:
                age_desc = f"Age ({age_val}) meets minimum age of {min_age} years."
            elif max_age is not None:
                age_desc = f"Age ({age_val}) does not exceed maximum age of {max_age} years."
            satisfied.append({
                "rule": "Age Requirement",
                "detail": age_desc,
                "user_val": f"{age_val} years"
            })
            relevance_points += 10
    else:
        # Age not provided or 0
        if min_age is not None or max_age is not None:
            limits = []
            if min_age is not None:
                limits.append(f"min {min_age}")
            if max_age is not None:
                limits.append(f"max {max_age}")
            info_needed.append({
                "rule": "Age Verification",
                "detail": f"Scheme specifies age criteria ({', '.join(limits)} years).",
                "action": "Please provide your age to verify eligibility."
            })

    # -------------------------------------------------------------
    # 3. Income Checks (max_income)
    # -------------------------------------------------------------
    user_income = user_profile.get("annual_income")
    max_income = rules.get("max_income")

    if max_income is not None:
        if user_income is not None and user_income != "":
            try:
                inc_val = float(user_income)
                if inc_val <= max_income:
                    satisfied.append({
                        "rule": "Annual Family Income",
                        "detail": f"Annual income of ₹{inc_val:,.0f} is within ceiling of ₹{max_income:,.0f}.",
                        "user_val": f"₹{inc_val:,.0f}"
                    })
                    relevance_points += 15
                else:
                    unsatisfied.append({
                        "rule": "Income Ceiling",
                        "detail": f"Family income limit is ₹{max_income:,.0f} per annum.",
                        "user_val": f"₹{inc_val:,.0f}",
                        "reason": f"Reported income exceeds eligibility ceiling by ₹{inc_val - max_income:,.0f}."
                    })
            except (ValueError, TypeError):
                info_needed.append({
                    "rule": "Income Verification",
                    "detail": f"Ceiling of ₹{max_income:,.0f} applies.",
                    "action": "Please provide a valid numeric income."
                })
        else:
            info_needed.append({
                "rule": "Income Verification",
                "detail": f"Scheme has an income threshold of ₹{max_income:,.0f} per year.",
                "action": "Please enter your family's annual income."
            })
    else:
        satisfied.append({
            "rule": "Income Requirement",
            "detail": "No strict income ceiling specified under published guidelines.",
            "user_val": "Not Restricted"
        })
        relevance_points += 5

    # -------------------------------------------------------------
    # 4. Occupation Checks
    # -------------------------------------------------------------
    allowed_occ = [normalize_str(o) for o in rules.get("allowed_occupations", ["any"])]
    user_occ = normalize_str(user_profile.get("occupation"))

    if "any" in allowed_occ:
        satisfied.append({
            "rule": "Occupation Requirement",
            "detail": "Open to citizens across all occupations.",
            "user_val": user_profile.get("occupation") or "Any"
        })
        relevance_points += 5
    else:
        if not user_occ or user_occ in ["", "none", "prefer not to say"]:
            info_needed.append({
                "rule": "Occupation Verification",
                "detail": f"Scheme is targeted to: {', '.join(rules.get('allowed_occupations', []))}.",
                "action": "Please select your primary occupation."
            })
        elif user_occ in allowed_occ or any(user_occ in ao or ao in user_occ for ao in allowed_occ):
            satisfied.append({
                "rule": "Occupation Requirement",
                "detail": f"Occupation ({user_profile.get('occupation')}) aligns with target beneficiaries.",
                "user_val": user_profile.get("occupation")
            })
            relevance_points += 20
        else:
            unsatisfied.append({
                "rule": "Occupation Restriction",
                "detail": f"Scheme is targeted to: {', '.join(rules.get('allowed_occupations', []))}.",
                "user_val": user_profile.get("occupation"),
                "reason": f"Selected occupation ({user_profile.get('occupation')}) does not match the target beneficiary occupations."
            })

    # -------------------------------------------------------------
    # 5. Gender Checks
    # -------------------------------------------------------------
    allowed_gen = [normalize_str(g) for g in rules.get("allowed_genders", ["any"])]
    user_gender = normalize_str(user_profile.get("gender"))

    if "any" in allowed_gen:
        satisfied.append({
            "rule": "Gender Requirement",
            "detail": "Applicable regardless of gender.",
            "user_val": user_profile.get("gender") or "Any"
        })
    else:
        if not user_gender or user_gender in ["prefer not to say", ""]:
            info_needed.append({
                "rule": "Gender Specificity",
                "detail": f"This scheme has gender-specific guidelines ({', '.join(rules.get('allowed_genders', []))}).",
                "action": "Select gender if you wish to confirm eligibility for women/gender-specific benefits."
            })
        elif user_gender in allowed_gen:
            satisfied.append({
                "rule": "Gender Requirement",
                "detail": f"Gender ({user_profile.get('gender')}) matches scheme guidelines.",
                "user_val": user_profile.get("gender")
            })
            relevance_points += 15
        else:
            unsatisfied.append({
                "rule": "Gender Restriction",
                "detail": f"Scheme is restricted to {', '.join(rules.get('allowed_genders', []))} applicants.",
                "user_val": user_profile.get("gender"),
                "reason": f"Applicant gender ({user_profile.get('gender')}) does not match scheme target."
            })

    # -------------------------------------------------------------
    # 6. Social Category Checks (SC/ST/OBC/EWS)
    # -------------------------------------------------------------
    allowed_cats = [normalize_str(c) for c in rules.get("allowed_social_categories", ["any"])]
    user_cat = normalize_str(user_profile.get("social_category"))

    if "any" in allowed_cats:
        satisfied.append({
            "rule": "Social Category",
            "detail": "Open to all social categories without restriction.",
            "user_val": user_profile.get("social_category") or "Any"
        })
    else:
        if not user_cat or user_cat in ["prefer not to say", ""]:
            info_needed.append({
                "rule": "Social Category Verification",
                "detail": f"Special category criteria apply ({', '.join(rules.get('allowed_social_categories', []))}).",
                "action": "Provide social category if seeking reserved category scholarship or welfare benefits."
            })
        elif user_cat in allowed_cats:
            satisfied.append({
                "rule": "Social Category Requirement",
                "detail": f"Social category ({user_profile.get('social_category')}) matches target reservation.",
                "user_val": user_profile.get("social_category")
            })
            relevance_points += 15
        else:
            unsatisfied.append({
                "rule": "Social Category Restriction",
                "detail": f"Targeted specifically for {', '.join(rules.get('allowed_social_categories', []))} communities.",
                "user_val": user_profile.get("social_category"),
                "reason": f"Category ({user_profile.get('social_category')}) is not covered under this specific program."
            })

    # -------------------------------------------------------------
    # 7. Residence Checks (Rural / Urban)
    # -------------------------------------------------------------
    allowed_res = [normalize_str(r) for r in rules.get("allowed_residence", ["rural", "urban"])]
    user_res = normalize_str(user_profile.get("residence"))

    if "rural" in allowed_res and "urban" in allowed_res:
        satisfied.append({
            "rule": "Residence Applicability",
            "detail": "Open to both rural and urban residents nationwide.",
            "user_val": user_profile.get("residence") or "All Areas"
        })
    elif not user_res:
        info_needed.append({
            "rule": "Area of Residence",
            "detail": f"Scheme targets {', '.join(rules.get('allowed_residence', []))} areas.",
            "action": "Please specify Rural or Urban residence."
        })
    elif user_res in allowed_res:
        satisfied.append({
            "rule": "Residence Area Match",
            "detail": f"Residence ({user_profile.get('residence')}) matches target area.",
            "user_val": user_profile.get("residence")
        })
        relevance_points += 10
    else:
        unsatisfied.append({
            "rule": "Residence Area Restriction",
            "detail": f"Scheme is restricted to {', '.join(rules.get('allowed_residence', []))} areas.",
            "user_val": user_profile.get("residence"),
            "reason": f"User residence ({user_profile.get('residence')}) is not covered by this scheme."
        })

    # -------------------------------------------------------------
    # 8. Farmer Status & Landholding Requirements
    # -------------------------------------------------------------
    farmer_req = rules.get("farmer_status_required", False)
    user_is_farmer = user_profile.get("farmer_status")

    if farmer_req:
        if user_is_farmer is True or user_occ == "farmer":
            satisfied.append({
                "rule": "Farmer Status",
                "detail": "User is verified as engaged in farming/agriculture.",
                "user_val": "Farmer"
            })
            relevance_points += 15

            # Cultivable land check
            if rules.get("requires_cultivable_land"):
                land = user_profile.get("landholding_hectares")
                if land is not None and float(land) > 0:
                    satisfied.append({
                        "rule": "Cultivable Landholding",
                        "detail": f"Cultivable land record confirmed ({land} hectares).",
                        "user_val": f"{land} ha"
                    })
                elif land is not None and float(land) == 0:
                    unsatisfied.append({
                        "rule": "Cultivable Landholding",
                        "detail": "Scheme requires ownership of cultivable landholding.",
                        "user_val": "0 ha / Landless",
                        "reason": "PM-KISAN guidelines require cultivable agricultural land title in applicant's name."
                    })
                else:
                    info_needed.append({
                        "rule": "Landholding Record",
                        "detail": "Scheme requires verified cultivable land title.",
                        "action": "Enter cultivable landholding in hectares."
                    })
        elif user_is_farmer is False and user_occ and user_occ != "farmer":
            unsatisfied.append({
                "rule": "Farmer Requirement",
                "detail": "Exclusive to agricultural landholding farmers.",
                "user_val": user_profile.get("occupation") or "Non-farmer",
                "reason": "Applicant is not an agricultural farmer."
            })
        else:
            info_needed.append({
                "rule": "Farmer Status",
                "detail": "Scheme requires landholding farmer status.",
                "action": "Indicate whether you own cultivable agricultural land."
            })

    # -------------------------------------------------------------
    # 9. Student Status
    # -------------------------------------------------------------
    student_req = rules.get("student_status_required", False)
    user_is_student = user_profile.get("student_status")

    if student_req:
        if user_is_student is True or user_occ == "student":
            satisfied.append({
                "rule": "Student Enrolment",
                "detail": "Enrolment in recognized educational institution confirmed.",
                "user_val": "Student"
            })
            relevance_points += 20
        elif user_is_student is False and user_occ and user_occ != "student":
            unsatisfied.append({
                "rule": "Student Requirement",
                "detail": "Exclusively for enrolled students.",
                "user_val": user_profile.get("occupation") or "Non-student",
                "reason": "Applicant is not actively enrolled as a student."
            })
        else:
            info_needed.append({
                "rule": "Student Enrolment",
                "detail": "Scheme requires active enrolment in educational courses.",
                "action": "Confirm whether you are an enrolled student."
            })

    # -------------------------------------------------------------
    # 10. Specific Disqualifiers / Exclusions
    # -------------------------------------------------------------
    # Check Income Tax Payer disqualifier (e.g. APY, PM-KISAN, IGNOAPS)
    user_tax_payer = user_profile.get("is_tax_payer", False)
    exclusions = rules.get("exclusions", [])

    tax_payer_excluded = any("tax" in normalize_str(ex) for ex in exclusions)
    if tax_payer_excluded and user_tax_payer:
        unsatisfied.append({
            "rule": "Tax Payer Exclusion",
            "detail": "Individuals paying Income Tax are explicitly excluded under scheme rules.",
            "user_val": "Income Tax Payer",
            "reason": "Applicant has paid income tax, which disqualifies them from this social assistance benefit."
        })

    # Existing LPG connection exclusion (for Ujjwala PMUY)
    if scheme_id == "SCHEME-005":
        has_lpg = user_profile.get("has_lpg_connection")
        if has_lpg is True:
            unsatisfied.append({
                "rule": "LPG Connection Exclusion",
                "detail": "Applicant household must not already possess an LPG cylinder connection.",
                "user_val": "Has LPG Connection",
                "reason": "PMUY is exclusively for households without any prior LPG connection."
            })
        elif has_lpg is False:
            satisfied.append({
                "rule": "No Existing LPG Connection",
                "detail": "Household confirmed as having no prior LPG connection.",
                "user_val": "No LPG Connection"
            })

    # Existing Pucca house exclusion (for PMAY)
    if scheme_id in ["SCHEME-003", "SCHEME-004"]:
        owns_pucca = user_profile.get("owns_pucca_house")
        if owns_pucca is True:
            unsatisfied.append({
                "rule": "Pucca House Ownership Exclusion",
                "detail": "Family should not own a permanent pucca house anywhere in India.",
                "user_val": "Owns Pucca House",
                "reason": "PMAY assistance is strictly for homeless or kutcha-house dwelling families."
            })
        elif owns_pucca is False:
            satisfied.append({
                "rule": "No Pucca House Ownership",
                "detail": "Beneficiary family does not own a pucca house.",
                "user_val": "No Pucca House"
            })

    # -------------------------------------------------------------
    # 11. Determine Final Eligibility Status
    # -------------------------------------------------------------
    notes = ""
    special_cond = rules.get("special_conditions")

    if unsatisfied:
        status = EligibilityResult.STATUS_LIKELY_INELIGIBLE
        relevance_points = max(10, relevance_points - 40)
        notes = "One or more listed criteria do not match your current profile."
    elif info_needed:
        status = EligibilityResult.STATUS_MORE_INFO_REQUIRED
        relevance_points = max(30, min(75, relevance_points))
        notes = "Profile meets preliminary requirements, but additional information is needed to confirm."
    else:
        # All listed rules are satisfied!
        # Check if scheme requires official field survey / BPL list / quota endorsement
        if special_cond and ("secc" in special_cond.lower() or "bpl" in special_cond.lower() or "quota" in special_cond.lower() or "camp" in special_cond.lower()):
            status = EligibilityResult.STATUS_OFFICIAL_VERIFICATION
            relevance_points = min(95, relevance_points + 10)
            notes = f"Demographics align, but final qualification depends on official records: {special_cond}"
        else:
            status = EligibilityResult.STATUS_POTENTIALLY_ELIGIBLE
            relevance_points = min(98, relevance_points + 20)
            notes = "Your profile matches all primary eligibility conditions listed in official guidelines."

    return EligibilityResult(
        scheme_id=scheme_id,
        scheme_name=scheme_name,
        status=status,
        relevance_score=relevance_points,
        satisfied_conditions=satisfied,
        unsatisfied_conditions=unsatisfied,
        information_required=info_needed,
        notes=notes
    )


def evaluate_all_schemes(user_profile: Dict[str, Any], schemes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Evaluates a user profile against all provided schemes.
    Merges evaluation results with scheme metadata for dashboard presentation.
    """
    results = []
    for s in schemes:
        eval_res = evaluate_scheme(user_profile, s)
        result_dict = eval_res.to_dict()
        # Merge scheme metadata
        result_dict.update({
            "department": s.get("department"),
            "scheme_level": s.get("scheme_level"),
            "category": s.get("category"),
            "target_beneficiaries": s.get("target_beneficiaries"),
            "short_description": s.get("short_description"),
            "benefits": s.get("benefits"),
            "required_documents": s.get("required_documents", []),
            "official_information_url": s.get("official_information_url"),
            "official_application_url": s.get("official_application_url"),
            "source_url": s.get("source_url"),
            "last_verification_date": s.get("last_verification_date"),
            "data_verification_status": s.get("data_verification_status", "Verified")
        })
        results.append(result_dict)

    # Sort primarily by status priority, then by relevance score descending
    status_priority = {
        EligibilityResult.STATUS_POTENTIALLY_ELIGIBLE: 1,
        EligibilityResult.STATUS_OFFICIAL_VERIFICATION: 2,
        EligibilityResult.STATUS_MORE_INFO_REQUIRED: 3,
        EligibilityResult.STATUS_LIKELY_INELIGIBLE: 4
    }

    results.sort(
        key=lambda item: (
            status_priority.get(item["status"], 99),
            -item["relevance_score"],
            item["scheme_name"]
        )
    )

    return results
