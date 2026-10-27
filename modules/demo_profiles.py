"""
Preconfigured Demo Profiles for Hackathon Evaluation and Demonstration.
Contains 5 realistic, completely fictional user personas.
"""

from typing import Dict, Any, List

DEMO_PROFILES: Dict[str, Dict[str, Any]] = {
    "farmer_uttarakhand": {
        "label": "Ramesh Patel - Small Farmer (Uttarakhand)",
        "persona_title": "Small Landholding Farmer",
        "description": "44-year-old farmer living in rural Dehradun, cultivating 1.2 hectares of land with annual income of ₹1,40,000.",
        "profile": {
            "full_name": "Ramesh Patel (Demo)",
            "age": 44,
            "gender": "Male",
            "state": "Uttarakhand",
            "district": "Dehradun",
            "residence": "Rural",
            "annual_income": 140000,
            "occupation": "farmer",
            "social_category": "OBC",
            "disability_status": False,
            "student_status": False,
            "education_level": "Higher Secondary",
            "farmer_status": True,
            "landholding_hectares": 1.2,
            "is_tax_payer": False,
            "has_lpg_connection": True,
            "owns_pucca_house": True
        },
        "expected_matches": ["PM-KISAN", "PM Suraksha Bima Yojana", "Atal Pension Yojana", "PMMSY"]
    },
    "student_maharashtra": {
        "label": "Priya Sharma - College Student (Maharashtra)",
        "persona_title": "Undergraduate SC Student",
        "description": "19-year-old undergraduate student from Pune from an SC family, exploring scholarships and apprenticeships.",
        "profile": {
            "full_name": "Priya Sharma (Demo)",
            "age": 19,
            "gender": "Female",
            "state": "Maharashtra",
            "district": "Pune",
            "residence": "Urban",
            "annual_income": 180000,
            "occupation": "student",
            "social_category": "SC",
            "disability_status": False,
            "student_status": True,
            "education_level": "Undergraduate",
            "farmer_status": False,
            "landholding_hectares": 0.0,
            "is_tax_payer": False,
            "has_lpg_connection": True,
            "owns_pucca_house": True
        },
        "expected_matches": ["Post-Matric Scholarship for SC/ST Students", "NAPS", "PMKVY 4.0", "PMSBY"]
    },
    "woman_entrepreneur_up": {
        "label": "Sunita Devi - Aspiring Woman Entrepreneur (Uttar Pradesh)",
        "persona_title": "Rural Woman Artisan & Entrepreneur",
        "description": "32-year-old woman in rural Varanasi looking for loans, skill incentives, and clean cooking fuel.",
        "profile": {
            "full_name": "Sunita Devi (Demo)",
            "age": 32,
            "gender": "Female",
            "state": "Uttar Pradesh",
            "district": "Varanasi",
            "residence": "Rural",
            "annual_income": 120000,
            "occupation": "woman entrepreneur",
            "social_category": "OBC",
            "disability_status": False,
            "student_status": False,
            "education_level": "School",
            "farmer_status": False,
            "landholding_hectares": 0.0,
            "is_tax_payer": False,
            "has_lpg_connection": False,
            "owns_pucca_house": False
        },
        "expected_matches": ["Stand-Up India Scheme", "PMMY (Mudra)", "PMUY 2.0 (Ujjwala)", "PM Vishwakarma", "PMAY-G"]
    },
    "street_vendor_delhi": {
        "label": "Manoj Kumar - Urban Street Vendor (Delhi)",
        "persona_title": "Urban Micro-Enterprise / Street Vendor",
        "description": "28-year-old street food cart vendor in Delhi seeking working capital credit and social security.",
        "profile": {
            "full_name": "Manoj Kumar (Demo)",
            "age": 28,
            "gender": "Male",
            "state": "Delhi",
            "district": "Central Delhi",
            "residence": "Urban",
            "annual_income": 95000,
            "occupation": "street vendor",
            "social_category": "General",
            "disability_status": False,
            "student_status": False,
            "education_level": "School",
            "farmer_status": False,
            "landholding_hectares": 0.0,
            "is_tax_payer": False,
            "has_lpg_connection": True,
            "owns_pucca_house": False
        },
        "expected_matches": ["PM SVANidhi", "PMMY (Mudra)", "PMSBY", "Atal Pension Yojana", "Ayushman Bharat PM-JAY"]
    },
    "senior_citizen_rajasthan": {
        "label": "Ram Lal - Low-Income Senior Citizen (Rajasthan)",
        "persona_title": "BPL Senior Citizen",
        "description": "66-year-old retired unorganized worker in rural Rajasthan seeking old-age pension and healthcare support.",
        "profile": {
            "full_name": "Ram Lal (Demo)",
            "age": 66,
            "gender": "Male",
            "state": "Rajasthan",
            "district": "Jaipur",
            "residence": "Rural",
            "annual_income": 48000,
            "occupation": "senior citizen",
            "social_category": "SC",
            "disability_status": False,
            "student_status": False,
            "education_level": "School",
            "farmer_status": False,
            "landholding_hectares": 0.0,
            "is_tax_payer": False,
            "has_lpg_connection": True,
            "owns_pucca_house": False
        },
        "expected_matches": ["IGNOAPS (Old Age Pension)", "Ayushman Bharat PM-JAY", "PMSBY"]
    }
}


def get_demo_profile_keys() -> List[str]:
    return list(DEMO_PROFILES.keys())


def get_demo_profile(key: str) -> Dict[str, Any]:
    return DEMO_PROFILES.get(key, {})
