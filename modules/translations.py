"""
Bilingual Translation Module (English & Hindi).
Provides structured translations for UI elements, statuses, guidelines, form fields, and dropdown options.
Preserves official scheme names, departments, and portal links accurately.
"""

from typing import Dict, Any

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # ---------------- Application Branding & Navigation ----------------
    "app_title": {
        "en": "Government Scheme Navigator",
        "hi": "भारत सरकार योजना मार्गदर्शक"
    },
    "tagline": {
        "en": "The Right Government Scheme for Every Citizen.",
        "hi": "हर नागरिक के लिए सही सरकारी योजना।"
    },
    "nav_home": {
        "en": "Home",
        "hi": "मुख्य पृष्ठ"
    },
    "nav_find_schemes": {
        "en": "Find My Schemes",
        "hi": "मेरी योजनाएं खोजें"
    },
    "nav_explorer": {
        "en": "Scheme Explorer",
        "hi": "योजना एक्सप्लोरर"
    },
    "nav_results": {
        "en": "Eligibility Results",
        "hi": "पात्रता परिणाम"
    },
    "nav_checklist": {
        "en": "Document Checklist",
        "hi": "दस्तावेज़ चेकलिस्ट"
    },
    "nav_ai_assistant": {
        "en": "AI Assistant",
        "hi": "एआई सहायक"
    },
    "nav_about": {
        "en": "About the Project",
        "hi": "परियोजना के बारे में"
    },

    # ---------------- Common UI Buttons & Labels ----------------
    "btn_check_eligibility": {
        "en": "Check Eligibility Now",
        "hi": "पात्रता की जांच करें"
    },
    "btn_reset_form": {
        "en": "Reset Profile",
        "hi": "फॉर्म रीसेट करें"
    },
    "btn_load_demo": {
        "en": "Load Demo Profile",
        "hi": "डेमो प्रोफाइल लोड करें"
    },
    "btn_download_pdf": {
        "en": "Download Official PDF Checklist",
        "hi": "पीडीएफ चेकलिस्ट डाउनलोड करें"
    },
    "btn_download_single_pdf": {
        "en": "Download Scheme PDF Checklist",
        "hi": "योजना चेकलिस्ट पीडीएफ डाउनलोड करें"
    },
    "btn_download_custom_pdf": {
        "en": "Download Customized PDF Checklist",
        "hi": "व्यक्तिगत पीडीएफ चेकलिस्ट डाउनलोड करें"
    },
    "btn_view_official": {
        "en": "Official Information Portal",
        "hi": "आधिकारिक सूचना पोर्टल"
    },
    "btn_apply_online": {
        "en": "Verified Application Portal",
        "hi": "ऑनलाइन आवेदन पोर्टल"
    },
    "btn_ask_ai": {
        "en": "Ask Question",
        "hi": "प्रश्न पूछें"
    },
    "btn_explain_fit": {
        "en": "Explain Top Match Fit",
        "hi": "शीर्ष योजना की पात्रता समझें"
    },
    "btn_summarize_checklist": {
        "en": "Summarize Document Checklist",
        "hi": "दस्तावेज़ चेकलिस्ट का सारांश"
    },
    "btn_clear_chat": {
        "en": "Clear Chat History",
        "hi": "बातचीत का इतिहास साफ़ करें"
    },

    # ---------------- Form Section Headers & Subtexts ----------------
    "form_header": {
        "en": "Citizen Profile & Economic Circumstances",
        "hi": "नागरिक विवरण एवं आर्थिक स्थिति"
    },
    "form_subtext": {
        "en": "Enter your profile details below to discover schemes you may be eligible for. No personal identifiers (like Aadhaar, bank numbers, or OTPs) are ever requested or stored.",
        "hi": "अपनी पात्रता जानने के लिए नीचे विवरण दर्ज करें। आधार संख्या, बैंक खाता या ओटीपी जैसी संवेदनशील जानकारी कभी नहीं मांगी जाती।"
    },
    "sec_demographic": {
        "en": "1. Demographic Information",
        "hi": "1. जनसांख्यिकीय विवरण"
    },
    "sec_economic": {
        "en": "2. Economic & Occupation Profile",
        "hi": "2. आर्थिक एवं व्यावसायिक स्थिति"
    },
    "sec_sector": {
        "en": "3. Sector-Specific Circumstances",
        "hi": "3. क्षेत्र-विशिष्ट परिस्थितियां"
    },

    # ---------------- Form Fields ----------------
    "label_age": {
        "en": "Age (in years)",
        "hi": "आयु (वर्षों में)"
    },
    "label_gender": {
        "en": "Gender",
        "hi": "लिंग"
    },
    "label_state": {
        "en": "State / Union Territory",
        "hi": "राज्य / केंद्र शासित प्रदेश"
    },
    "label_district": {
        "en": "District",
        "hi": "जिला"
    },
    "label_residence": {
        "en": "Area of Residence",
        "hi": "निवास क्षेत्र"
    },
    "label_annual_income": {
        "en": "Annual Family Income (INR ₹)",
        "hi": "वार्षिक पारिवारिक आय (रुपये ₹)"
    },
    "label_occupation": {
        "en": "Primary Occupation",
        "hi": "मुख्य व्यवसाय"
    },
    "label_social_category": {
        "en": "Social Category (Optional)",
        "hi": "सामाजिक श्रेणी (वैकल्पिक)"
    },
    "label_disability": {
        "en": "Person with Disability (PwD)",
        "hi": "दिव्यांगता की स्थिति"
    },
    "label_student_status": {
        "en": "Currently Enrolled Student?",
        "hi": "क्या आप वर्तमान में छात्र हैं?"
    },
    "label_education_level": {
        "en": "Highest Education Level",
        "hi": "शिक्षा का स्तर"
    },
    "label_farmer_status": {
        "en": "Engaged in Farming / Agriculture?",
        "hi": "क्या आप किसान / कृषि कार्य से जुड़े हैं?"
    },
    "label_landholding": {
        "en": "Cultivable Agricultural Landholding (Hectares)",
        "hi": "कृषि भूमि का रकबा (हेक्टेयर में)"
    },
    "label_tax_payer": {
        "en": "Have you paid Income Tax in the past year?",
        "hi": "क्या आपने पिछले वित्तीय वर्ष में आयकर दिया है?"
    },
    "label_lpg": {
        "en": "Household already has an active LPG connection?",
        "hi": "क्या आपके घर में पहले से एलपीजी गैस कनेक्शन है?"
    },
    "label_pucca_house": {
        "en": "Family owns a permanent pucca house in India?",
        "hi": "क्या परिवार के पास देश में कहीं भी पक्का मकान है?"
    },

    # ---------------- Dropdown Option Translations ----------------
    "opt_gender_female": {"en": "Female", "hi": "महिला (Female)"},
    "opt_gender_male": {"en": "Male", "hi": "पुरुष (Male)"},
    "opt_gender_transgender": {"en": "Transgender", "hi": "ट्रांसजेंडर (Transgender)"},
    "opt_gender_prefer_not": {"en": "Prefer not to say", "hi": "बताना नहीं चाहते (Prefer not to say)"},

    "opt_res_rural": {"en": "Rural", "hi": "ग्रामीण (Rural)"},
    "opt_res_urban": {"en": "Urban", "hi": "शहरी (Urban)"},
    "opt_res_semi_urban": {"en": "Semi-Urban", "hi": "अर्ध-शहरी (Semi-Urban)"},

    "opt_cat_general": {"en": "General", "hi": "सामान्य (General)"},
    "opt_cat_obc": {"en": "OBC", "hi": "अन्य पिछड़ा वर्ग (OBC)"},
    "opt_cat_sc": {"en": "SC", "hi": "अनुसूचित जाति (SC)"},
    "opt_cat_st": {"en": "ST", "hi": "अनुसूचित जनजाति (ST)"},
    "opt_cat_ews": {"en": "EWS", "hi": "आर्थिक रूप से कमजोर (EWS)"},
    "opt_cat_prefer_not": {"en": "Prefer not to say", "hi": "बताना नहीं चाहते"},

    "opt_occ_farmer": {"en": "Farmer / Agricultural Worker", "hi": "किसान / कृषि श्रमिक (Farmer)"},
    "opt_occ_student": {"en": "Student / Enrolled Scholar", "hi": "छात्र / विद्यार्थी (Student)"},
    "opt_occ_woman_entrepreneur": {"en": "Woman Entrepreneur / Self-Employed", "hi": "महिला उद्यमी / स्वरोजगार (Woman Entrepreneur)"},
    "opt_occ_street_vendor": {"en": "Street Vendor / Hawker", "hi": "स्ट्रीट वेंडर / फेरीवाले (Street Vendor)"},
    "opt_occ_artisan": {"en": "Traditional Artisan / Craftsperson", "hi": "पारंपरिक कारीगर / दस्तकार (Artisan)"},
    "opt_occ_business_owner": {"en": "Micro / Small Business Owner", "hi": "लघु / सूक्ष्म व्यवसाय मालिक (Business Owner)"},
    "opt_occ_unemployed": {"en": "Unemployed Youth / Job Seeker", "hi": "बेरोजगार युवा / नौकरी तलाशने वाले (Unemployed)"},
    "opt_occ_senior_citizen": {"en": "Senior Citizen / Retired", "hi": "वरिष्ठ नागरिक / सेवानिवृत्त (Senior Citizen)"},
    "opt_occ_employed": {"en": "Salaried / Wage Worker", "hi": "वेतनभोगी / कर्मचारी (Employed)"},
    "opt_occ_other": {"en": "Other / General Citizen", "hi": "अन्य नागरिक (Other)"},

    "opt_edu_school": {"en": "School", "hi": "विद्यालय स्तर (School)"},
    "opt_edu_hs": {"en": "Higher Secondary", "hi": "हायर सेकेंडरी (10+2)"},
    "opt_edu_vocational": {"en": "Vocational / ITI", "hi": "व्यावसायिक प्रशिक्षण / आईटीआई"},
    "opt_edu_ug": {"en": "Undergraduate", "hi": "स्नातक / कॉलेज डिग्री (Undergraduate)"},
    "opt_edu_pg": {"en": "Postgraduate", "hi": "स्नातकोत्तर (Postgraduate)"},
    "opt_edu_other": {"en": "Other", "hi": "अन्य (Other)"},

    # ---------------- Eligibility Statuses ----------------
    "status_potentially_eligible": {
        "en": "Potentially Eligible",
        "hi": "संभावित रूप से पात्र"
    },
    "status_more_info_required": {
        "en": "More Information Required",
        "hi": "अधिक जानकारी आवश्यक"
    },
    "status_likely_ineligible": {
        "en": "Likely Ineligible Under Listed Rules",
        "hi": "सूचीबद्ध नियमों के तहत संभावित अपात्र"
    },
    "status_official_verification": {
        "en": "Official Verification Required",
        "hi": "आधिकारिक सत्यापन आवश्यक"
    },

    # ---------------- Dashboard & Metrics ----------------
    "metric_total_schemes": {
        "en": "Total Schemes Evaluated",
        "hi": "कुल जांची गई योजनाएं"
    },
    "metric_eligible": {
        "en": "Potentially Eligible",
        "hi": "संभावित पात्र योजनाएं"
    },
    "metric_verification": {
        "en": "Official Verification Needed",
        "hi": "सत्यापन अपेक्षित"
    },
    "metric_documents": {
        "en": "Key Documents Needed",
        "hi": "आवश्यक दस्तावेज़"
    },
    "filter_heading": {
        "en": "Filter & Search Schemes",
        "hi": "योजनाएं खोजें एवं फ़िल्टर करें"
    },
    "search_placeholder": {
        "en": "Search by scheme name, keywords, or benefits...",
        "hi": "योजना का नाम, कीवर्ड या लाभ खोजें..."
    },
    "chat_placeholder": {
        "en": "Ask a question about government schemes (e.g. What documents do I need for PM-KISAN?)...",
        "hi": "सरकारी योजनाओं के बारे में कोई भी प्रश्न पूछें (उदा. पीएम-किसान के लिए क्या दस्तावेज़ चाहिए?)..."
    },
    "conditions_met": {
        "en": "Conditions Satisfied (Met)",
        "hi": "पूरी की गई शर्तें (नियम पूर्ण)"
    },
    "conditions_unmet": {
        "en": "Conditions Not Satisfied (Unmet)",
        "hi": "अधूरी शर्तें (नियम अपूर्ण)"
    },
    "info_needed": {
        "en": "Information Required to Confirm",
        "hi": "पुष्टि के लिए आवश्यक जानकारी"
    },
    "documents_needed": {
        "en": "Required Documents",
        "hi": "आवश्यक दस्तावेज़"
    },
    "ranking_score": {
        "en": "Demographic Relevance Ranking",
        "hi": "जनसांख्यिकीय प्रासंगिकता स्कोर"
    },
    "key_benefits": {
        "en": "Key Benefits",
        "hi": "प्रमुख लाभ"
    },
    "official_info_label": {
        "en": "Official Information",
        "hi": "आधिकारिक जानकारी"
    },
    "application_label": {
        "en": "Online Application",
        "hi": "ऑनलाइन आवेदन"
    },
    "offline_app_note": {
        "en": "Offline camp / Panchayat / CSC registration",
        "hi": "ऑफ़लाइन शिविर / ग्राम पंचायत / सीएससी केंद्र द्वारा"
    },
    "pro_tip": {
        "en": "Pro-Tip for Citizens: Most DBT benefits require that your Bank Account is active and mapped to your Aadhaar via the NPCI mapper. You can check NPCI status through your bank branch or online banking.",
        "hi": "नागरिकों के लिए सुझाव: अधिकांश डीबीटी (DBT) लाभों के लिए आवश्यक है कि आपका बैंक खाता सक्रिय हो और एनपीसीआई (NPCI) मैपर के माध्यम से आपके आधार से जुड़ा हो। आप अपनी बैंक शाखा या ऑनलाइन बैंकिंग द्वारा इसकी जांच कर सकते हैं।"
    },

    # ---------------- Disclaimers ----------------
    "disclaimer_text": {
        "en": "Important Disclaimer: The Government Scheme Navigator is an independent educational and civic tool. It does NOT guarantee eligibility, approval, or disbursement of benefits. Government rules, quotas, and application windows change periodically. Citizens must independently confirm details on the respective official government portals before applying.",
        "hi": "महत्वपूर्ण अस्वीकरण: भारत सरकार योजना मार्गदर्शक एक स्वतंत्र शैक्षणिक एवं नागरिक सहायता साधन है। यह पात्रता, अनुमोदन या लाभ के वितरण की गारंटी नहीं देता है। सरकारी नियम समय-समय पर संशोधित होते हैं। नागरिकों को आवेदन करने से पहले संबंधित आधिकारिक सरकारी पोर्टलों पर विवरणों की पुष्टि अवश्य करनी चाहिए।"
    },
    "empty_results": {
        "en": "No schemes matched the active filters. Try clearing your filters or updating your profile information.",
        "hi": "सक्रिय फ़िल्टर के अनुसार कोई योजना नहीं मिली। कृपया अपने फ़िल्टर हटाएं या प्रोफ़ाइल विवरण अपडेट करें।"
    }
}


def t(key: str, lang: str = "en") -> str:
    """
    Retrieve translated text for a given translation key and language code.
    Defaults to English if key or language is missing.
    """
    lang_code = "hi" if lang in ["hi", "hindi", "हिन्दी"] else "en"
    key_entry = TRANSLATIONS.get(key)
    if not key_entry:
        return key
    return key_entry.get(lang_code, key_entry.get("en", key))
