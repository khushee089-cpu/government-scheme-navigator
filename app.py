"""
Government Scheme Navigator
Main Application File (Streamlit)
"The Right Government Scheme for Every Citizen."
"""

import os
import streamlit as st
import pandas as pd
from typing import Dict, Any, List

# Import local modules
from modules.data_loader import (
    load_schemes,
    get_categories,
    get_all_departments,
    get_scheme_by_id
)
from modules.eligibility import (
    evaluate_all_schemes,
    EligibilityResult
)
from modules.recommendations import (
    filter_schemes,
    aggregate_document_checklist
)
from modules.demo_profiles import (
    DEMO_PROFILES,
    get_demo_profile
)
from modules.translations import t
from modules.ai_assistant import (
    ask_ai_assistant,
    explain_scheme_fit,
    explain_checklist_summary
)
from modules.pdf_generator import (
    generate_eligibility_pdf,
    generate_single_scheme_pdf
)

# -----------------------------------------------------------------------------
# 1. Streamlit Page Configuration & Theming
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Government Scheme Navigator | भारत सरकार योजना मार्गदर्शक",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern hackathon-grade UI
CUSTOM_CSS = """
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Header hero banner */
    .hero-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%);
        color: white;
        padding: 2.2rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.15);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .hero-tagline {
        font-size: 1.15rem;
        font-weight: 400;
        margin-top: 0.5rem;
        color: #e0f2fe;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: transform 0.15s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0.2rem 0;
    }
    .metric-lbl {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Scheme Cards */
    .scheme-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        border-left: 6px solid #1e3a8a;
    }
    .scheme-card-eligible {
        border-left: 6px solid #16a34a !important;
    }
    .scheme-card-verif {
        border-left: 6px solid #0284c7 !important;
    }
    .scheme-card-info {
        border-left: 6px solid #ea580c !important;
    }
    .scheme-card-ineligible {
        border-left: 6px solid #94a3b8 !important;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.3rem;
    }
    .badge-eligible { background-color: #dcfce7; color: #166534; }
    .badge-verif { background-color: #e0f2fe; color: #0369a1; }
    .badge-info { background-color: #ffedd5; color: #c2410c; }
    .badge-ineligible { background-color: #f1f5f9; color: #475569; }
    .badge-central { background-color: #ede9fe; color: #6b21a8; }
    .badge-state { background-color: #fef08a; color: #854d0e; }
    .badge-category { background-color: #f3f4f6; color: #374151; }

    /* Footer styling */
    .app-footer {
        margin-top: 3.5rem;
        padding: 1.5rem 1rem;
        border-top: 1px solid #e2e8f0;
        background-color: #f8fafc;
        border-radius: 8px;
        text-align: center;
        font-size: 0.85rem;
        color: #64748b;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. State Initialization & Data Preloading
# -----------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "age": 30,
        "gender": "Female",
        "state": "Uttar Pradesh",
        "district": "",
        "residence": "Rural",
        "annual_income": 120000,
        "occupation": "woman entrepreneur",
        "social_category": "OBC",
        "disability_status": False,
        "student_status": False,
        "education_level": "Higher Secondary",
        "farmer_status": False,
        "landholding_hectares": 0.0,
        "is_tax_payer": False,
        "has_lpg_connection": False,
        "owns_pucca_house": False
    }

if "evaluated_schemes" not in st.session_state:
    st.session_state["evaluated_schemes"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Load Scheme Dataset
try:
    ALL_SCHEMES = load_schemes()
except Exception as e:
    st.error(f"⚠️ Error loading scheme database: {e}")
    st.stop()

# If evaluation has not run yet, evaluate initial default profile
if not st.session_state["evaluated_schemes"]:
    st.session_state["evaluated_schemes"] = evaluate_all_schemes(
        st.session_state["user_profile"],
        ALL_SCHEMES
    )

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

OCCUPATIONS = [
    ("farmer", "Farmer / Agricultural Worker"),
    ("student", "Student / Enrolled Scholar"),
    ("woman entrepreneur", "Woman Entrepreneur / Self-Employed"),
    ("street vendor", "Street Vendor / Hawker"),
    ("artisan", "Traditional Artisan / Craftsperson"),
    ("business owner", "Micro / Small Business Owner"),
    ("unemployed", "Unemployed Youth / Job Seeker"),
    ("senior citizen", "Senior Citizen / Retired"),
    ("employed", "Salaried / Wage Worker"),
    ("other", "Other / General Citizen")
]

# -----------------------------------------------------------------------------
# 3. Sidebar Navigation & Global Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    col_logo1, col_logo2 = st.columns([1, 2])
    with col_logo1:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=75)
    with col_logo2:
        st.markdown("#### Scheme Navigator<br/><span style='font-size:0.75rem; color:#64748b;'>Civic Tech Platform</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🇮🇳 Navigation")
    
    # Language Toggle
    lang_choice = st.radio(
        "Language / भाषा",
        options=["English", "हिन्दी"],
        index=0 if st.session_state["lang"] == "en" else 1,
        horizontal=True
    )
    current_lang = "hi" if lang_choice == "हिन्दी" else "en"
    st.session_state["lang"] = current_lang

    nav_options = [
        ("home", t("nav_home", current_lang), "🏠"),
        ("find_schemes", t("nav_find_schemes", current_lang), "📝"),
        ("explorer", t("nav_explorer", current_lang), "🔍"),
        ("results", t("nav_results", current_lang), "📊"),
        ("checklist", t("nav_checklist", current_lang), "📋"),
        ("ai_assistant", t("nav_ai_assistant", current_lang), "🤖"),
        ("about", t("nav_about", current_lang), "ℹ️")
    ]

    selected_nav = st.radio(
        "Go to",
        options=[opt[0] for opt in nav_options],
        format_func=lambda x: next(f"{opt[2]} {opt[1]}" for opt in nav_options if opt[0] == x),
        label_visibility="collapsed"
    )

    st.markdown("---")
    
    # Demo Profile Quick Loader in Sidebar
    st.markdown("### ⚡ Demo Personas")
    st.caption("Quickly test realistic hackathon personas:")
    demo_keys = list(DEMO_PROFILES.keys())
    demo_labels = [DEMO_PROFILES[k]["label"] for k in demo_keys]
    chosen_demo_idx = st.selectbox(
        "Select Persona",
        options=range(len(demo_keys)),
        format_func=lambda i: demo_labels[i]
    )

    if st.button("Load Persona 🚀", use_container_width=True):
        selected_key = demo_keys[chosen_demo_idx]
        persona_data = get_demo_profile(selected_key)
        st.session_state["user_profile"] = persona_data["profile"].copy()
        st.session_state["evaluated_schemes"] = evaluate_all_schemes(
            st.session_state["user_profile"],
            ALL_SCHEMES
        )
        st.toast(f"Loaded: {persona_data['persona_title']}!", icon="✅")
        st.rerun()

    st.markdown("---")
    # AI Mode status
    api_key_env = os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY")
    if api_key_env:
        st.success("🟢 AI Assistant: Online (API Connected)")
    else:
        st.info("🔵 AI Assistant: Offline Grounded Mode (Zero-cost, 100% reliable)")

    st.caption("v1.0.0 • College Hackathon Edition")

# -----------------------------------------------------------------------------
# 4. View 1: Home (Landing Page)
# -----------------------------------------------------------------------------
if selected_nav == "home":
    st.markdown(
        f"""
        <div class="hero-container">
            <h1 class="hero-title">🏛️ {t("app_title", current_lang)}</h1>
            <p class="hero-tagline">{t("tagline", current_lang)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Key Highlights Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Verified Schemes</div>
                <div class="metric-val" style="color: #1e3a8a;">{len(ALL_SCHEMES)}</div>
                <div style="font-size: 0.8rem; color: #64748b;">Central & State Portals</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        pot_count = sum(1 for s in st.session_state["evaluated_schemes"] if s["status"] == "Potentially Eligible")
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">{t('metric_eligible', current_lang)}</div>
                <div class="metric-val" style="color: #16a34a;">{pot_count}</div>
                <div style="font-size: 0.8rem; color: #64748b;">For Active Profile</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Rule Engine</div>
                <div class="metric-val" style="color: #0284c7;">100%</div>
                <div style="font-size: 0.8rem; color: #64748b;">Deterministic & Grounded</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Languages</div>
                <div class="metric-val" style="color: #7c3aed;">2</div>
                <div style="font-size: 0.8rem; color: #64748b;">English & हिन्दी Supported</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # 4-Step Visual Journey
    st.subheader("How It Works: 4 Easy Steps to Your Benefits")
    step1, step2, step3, step4 = st.columns(4)
    with step1:
        st.markdown("##### 1. Fill Profile")
        st.write("Share basic details like age, occupation, state, and income. No sensitive personal data or OTPs needed.")
    with step2:
        st.markdown("##### 2. Rule Evaluation")
        st.write("Our deterministic engine tests all official eligibility conditions and highlights satisfied vs unsatisfied rules.")
    with step3:
        st.markdown("##### 3. Get Checklist")
        st.write("Review all required paperwork, explanations, and download a professional PDF summary.")
    with step4:
        st.markdown("##### 4. Apply Officially")
        st.write("Directly visit official verified government portals (.gov.in / .nic.in) to complete your application safely.")

    st.markdown("---")

    # Quick Action Callouts
    c_btn1, c_btn2, c_btn3 = st.columns([1, 1, 1])
    with c_btn1:
        if st.button("📝 Start Finding Schemes", use_container_width=True, type="primary"):
            st.session_state["nav"] = "find_schemes"
            st.rerun()
    with c_btn2:
        if st.button("🔍 Browse Scheme Explorer", use_container_width=True):
            st.session_state["nav"] = "explorer"
            st.rerun()
    with c_btn3:
        if st.button("🤖 Talk to AI Assistant", use_container_width=True):
            st.session_state["nav"] = "ai_assistant"
            st.rerun()

    # Featured Schemes preview
    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("Featured National Welfare Programs")
    f_cols = st.columns(3)
    for idx, sch in enumerate(ALL_SCHEMES[:3]):
        with f_cols[idx]:
            st.markdown(
                f"""
                <div class="scheme-card" style="min-height: 220px;">
                    <span class="badge badge-central">{sch['scheme_level']}</span>
                    <span class="badge badge-category">{sch['category']}</span>
                    <h4 style="margin: 0.5rem 0 0.3rem 0; color: #1e3a8a;">{sch['name']}</h4>
                    <p style="font-size: 0.85rem; color: #475569; margin-bottom: 0.5rem;">{sch['short_description'][:130]}...</p>
                    <p style="font-size: 0.85rem; font-weight: 600; color: #0f766e;">Benefit: {sch['benefits'][:90]}...</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------------------------------------------------
# 5. View 2: Find My Schemes (User Profile Form)
# -----------------------------------------------------------------------------
elif selected_nav == "find_schemes":
    st.subheader(f"📝 {t('form_header', current_lang)}")
    st.write(t("form_subtext", current_lang))

    # Fast demo profile filler bar
    with st.expander("✨ Need a quick test profile? Select a Demo Persona", expanded=False):
        d_cols = st.columns([3, 1])
        with d_cols[0]:
            quick_demo = st.selectbox(
                "Choose Persona",
                options=list(DEMO_PROFILES.keys()),
                format_func=lambda k: f"{DEMO_PROFILES[k]['label']} - {DEMO_PROFILES[k]['description']}"
            )
        with d_cols[1]:
            st.write("")
            st.write("")
            if st.button("Apply Profile", use_container_width=True):
                st.session_state["user_profile"] = DEMO_PROFILES[quick_demo]["profile"].copy()
                st.session_state["evaluated_schemes"] = evaluate_all_schemes(
                    st.session_state["user_profile"],
                    ALL_SCHEMES
                )
                st.success(f"Applied profile for {DEMO_PROFILES[quick_demo]['label']}!")
                st.rerun()

    prof = st.session_state["user_profile"]

    with st.form("profile_form"):
        st.markdown(f"#### {t('sec_demographic', current_lang)}")
        col_d1, col_d2, col_d3 = st.columns(3)

        with col_d1:
            age_input = st.number_input(
                t("label_age", current_lang),
                min_value=0,
                max_value=120,
                value=int(prof.get("age", 25)),
                help="Age in completed years. Used to check minimum and maximum age criteria."
            )

        with col_d2:
            gender_options = ["Female", "Male", "Transgender", "Prefer not to say"]
            gender_labels = {
                "Female": t("opt_gender_female", current_lang),
                "Male": t("opt_gender_male", current_lang),
                "Transgender": t("opt_gender_transgender", current_lang),
                "Prefer not to say": t("opt_gender_prefer_not", current_lang)
            }
            current_gender = prof.get("gender", "Female")
            gender_idx = gender_options.index(current_gender) if current_gender in gender_options else 0
            gender_input = st.selectbox(
                t("label_gender", current_lang),
                options=gender_options,
                index=gender_idx,
                format_func=lambda k: gender_labels.get(k, k)
            )

        with col_d3:
            social_cat_options = ["General", "OBC", "SC", "ST", "EWS", "Prefer not to say"]
            cat_labels = {
                "General": t("opt_cat_general", current_lang),
                "OBC": t("opt_cat_obc", current_lang),
                "SC": t("opt_cat_sc", current_lang),
                "ST": t("opt_cat_st", current_lang),
                "EWS": t("opt_cat_ews", current_lang),
                "Prefer not to say": t("opt_cat_prefer_not", current_lang)
            }
            current_cat = prof.get("social_category", "General")
            cat_idx = social_cat_options.index(current_cat) if current_cat in social_cat_options else 0
            cat_input = st.selectbox(
                t("label_social_category", current_lang),
                options=social_cat_options,
                index=cat_idx,
                format_func=lambda k: cat_labels.get(k, k),
                help="Handled respectfully. Some scholarships and subsidies are earmarked for specific categories."
            )

        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            state_idx = INDIAN_STATES.index(prof.get("state", "Uttar Pradesh")) if prof.get("state") in INDIAN_STATES else 0
            state_input = st.selectbox(
                t("label_state", current_lang),
                options=INDIAN_STATES,
                index=state_idx
            )
        with col_g2:
            district_input = st.text_input(
                t("label_district", current_lang),
                value=str(prof.get("district", ""))
            )
        with col_g3:
            res_options = ["Rural", "Urban", "Semi-Urban"]
            res_labels = {
                "Rural": t("opt_res_rural", current_lang),
                "Urban": t("opt_res_urban", current_lang),
                "Semi-Urban": t("opt_res_semi_urban", current_lang)
            }
            current_res = prof.get("residence", "Rural")
            res_idx = res_options.index(current_res) if current_res in res_options else 0
            residence_input = st.selectbox(
                t("label_residence", current_lang),
                options=res_options,
                index=res_idx,
                format_func=lambda k: res_labels.get(k, k)
            )

        st.markdown("---")
        st.markdown(f"#### {t('sec_economic', current_lang)}")
        col_e1, col_e2 = st.columns(2)

        with col_e1:
            income_input = st.number_input(
                t("label_annual_income", current_lang),
                min_value=0,
                max_value=10000000,
                value=int(prof.get("annual_income", 120000)),
                step=10000,
                help="Total annual gross income of the family from all sources in Indian Rupees (INR)."
            )

        with col_e2:
            occ_keys = [o[0] for o in OCCUPATIONS]
            occ_labels = {
                "farmer": t("opt_occ_farmer", current_lang),
                "student": t("opt_occ_student", current_lang),
                "woman entrepreneur": t("opt_occ_woman_entrepreneur", current_lang),
                "street vendor": t("opt_occ_street_vendor", current_lang),
                "artisan": t("opt_occ_artisan", current_lang),
                "business owner": t("opt_occ_business_owner", current_lang),
                "unemployed": t("opt_occ_unemployed", current_lang),
                "senior citizen": t("opt_occ_senior_citizen", current_lang),
                "employed": t("opt_occ_employed", current_lang),
                "other": t("opt_occ_other", current_lang)
            }
            current_occ = prof.get("occupation", "woman entrepreneur")
            occ_idx = occ_keys.index(current_occ) if current_occ in occ_keys else 0
            occ_input = st.selectbox(
                t("label_occupation", current_lang),
                options=occ_keys,
                index=occ_idx,
                format_func=lambda k: occ_labels.get(k, k)
            )

        st.markdown("---")
        st.markdown(f"#### {t('sec_sector', current_lang)}")
        col_s1, col_s2, col_s3 = st.columns(3)

        with col_s1:
            is_farmer = st.checkbox(
                t("label_farmer_status", current_lang),
                value=bool(prof.get("farmer_status", False))
            )
            land_val = st.number_input(
                t("label_landholding", current_lang),
                min_value=0.0,
                max_value=100.0,
                value=float(prof.get("landholding_hectares", 0.0)),
                step=0.25,
                disabled=not is_farmer
            )

        with col_s2:
            is_student = st.checkbox(
                t("label_student_status", current_lang),
                value=bool(prof.get("student_status", False))
            )
            edu_levels = ["School", "Higher Secondary", "Vocational / ITI", "Undergraduate", "Postgraduate", "Other"]
            edu_labels = {
                "School": t("opt_edu_school", current_lang),
                "Higher Secondary": t("opt_edu_hs", current_lang),
                "Vocational / ITI": t("opt_edu_vocational", current_lang),
                "Undergraduate": t("opt_edu_ug", current_lang),
                "Postgraduate": t("opt_edu_pg", current_lang),
                "Other": t("opt_edu_other", current_lang)
            }
            current_edu = prof.get("education_level", "Higher Secondary")
            edu_idx = edu_levels.index(current_edu) if current_edu in edu_levels else 0
            edu_input = st.selectbox(
                t("label_education_level", current_lang),
                options=edu_levels,
                index=edu_idx,
                format_func=lambda k: edu_labels.get(k, k),
                disabled=not is_student
            )

        with col_s3:
            is_tax_payer = st.checkbox(
                t("label_tax_payer", current_lang),
                value=bool(prof.get("is_tax_payer", False)),
                help="Many social pensions and DBT schemes exclude individuals who file income tax."
            )
            has_lpg = st.checkbox(
                t("label_lpg", current_lang),
                value=bool(prof.get("has_lpg_connection", False)),
                help="PM Ujjwala requires applicant household to have no existing LPG connection."
            )
            owns_pucca = st.checkbox(
                t("label_pucca_house", current_lang),
                value=bool(prof.get("owns_pucca_house", False)),
                help="PMAY housing grants require that family does not own a permanent pucca house."
            )

        st.markdown("<br/>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            submitted = st.form_submit_button(f"🔍 {t('btn_check_eligibility', current_lang)}", type="primary", use_container_width=True)
        with col_btn2:
            reset_clicked = st.form_submit_button(f"🔄 {t('btn_reset_form', current_lang)}", use_container_width=True)

    if submitted:
        updated_profile = {
            "age": age_input,
            "gender": gender_input,
            "social_category": cat_input,
            "state": state_input,
            "district": district_input,
            "residence": residence_input,
            "annual_income": income_input,
            "occupation": occ_input,
            "disability_status": prof.get("disability_status", False),
            "student_status": is_student,
            "education_level": edu_input if is_student else "Not Applicable",
            "farmer_status": is_farmer,
            "landholding_hectares": land_val if is_farmer else 0.0,
            "is_tax_payer": is_tax_payer,
            "has_lpg_connection": has_lpg,
            "owns_pucca_house": owns_pucca
        }
        st.session_state["user_profile"] = updated_profile
        st.session_state["evaluated_schemes"] = evaluate_all_schemes(updated_profile, ALL_SCHEMES)
        st.toast("Profile updated and schemes evaluated!", icon="🎯")
        st.success("✅ Profile evaluation completed! Review your recommendations below or click 'Eligibility Results' in navigation.")

    if reset_clicked:
        st.session_state["user_profile"] = {
            "age": 25,
            "gender": "Prefer not to say",
            "state": "Uttar Pradesh",
            "district": "",
            "residence": "Rural",
            "annual_income": 100000,
            "occupation": "other",
            "social_category": "Prefer not to say",
            "disability_status": False,
            "student_status": False,
            "education_level": "None",
            "farmer_status": False,
            "landholding_hectares": 0.0,
            "is_tax_payer": False,
            "has_lpg_connection": False,
            "owns_pucca_house": False
        }
        st.session_state["evaluated_schemes"] = evaluate_all_schemes(
            st.session_state["user_profile"],
            ALL_SCHEMES
        )
        st.info("Profile has been reset to defaults.")
        st.rerun()

# -----------------------------------------------------------------------------
# 6. View 3: Scheme Explorer
# -----------------------------------------------------------------------------
elif selected_nav == "explorer":
    st.subheader(f"🔍 {t('nav_explorer', current_lang)}")
    st.write("Browse and search the verified Indian Government Scheme dataset without needing to fill a profile.")

    # Filter Bar
    c_f1, c_f2, c_f3 = st.columns([2, 1, 1])
    with c_f1:
        search_query = st.text_input(
            "Search",
            placeholder=t("search_placeholder", current_lang),
            label_visibility="collapsed"
        )
    with c_f2:
        categories = ["All Categories"] + get_categories(ALL_SCHEMES)
        sel_cat = st.selectbox("Category Filter", options=categories, label_visibility="collapsed")
    with c_f3:
        level_filter = st.selectbox("Scheme Level", options=["All Levels", "Central", "State"], label_visibility="collapsed")

    # Apply Filters
    filtered_list = ALL_SCHEMES
    if search_query:
        sq = search_query.lower()
        filtered_list = [
            s for s in filtered_list
            if sq in s.get("name", "").lower()
            or sq in s.get("short_description", "").lower()
            or sq in s.get("department", "").lower()
            or sq in s.get("benefits", "").lower()
        ]
    if sel_cat != "All Categories":
        filtered_list = [s for s in filtered_list if s.get("category") == sel_cat]
    if level_filter != "All Levels":
        filtered_list = [s for s in filtered_list if s.get("scheme_level") == level_filter]

    st.caption(f"Showing **{len(filtered_list)}** schemes:")

    if not filtered_list:
        st.info(t("empty_results", current_lang))
    else:
        for sch in filtered_list:
            level_badge = "badge-central" if sch["scheme_level"] == "Central" else "badge-state"
            level_text = "केंद्रीय योजना (Central)" if (current_lang == "hi" and sch["scheme_level"] == "Central") else ("राज्य योजना (State)" if current_lang == "hi" else sch["scheme_level"])
            
            # Show Hindi name prominently if Hindi mode is active
            display_name = sch.get("hindi_name") if (current_lang == "hi" and sch.get("hindi_name")) else sch["name"]
            secondary_name = f"<div style='font-size:0.85rem; color:#64748b;'>{sch['name']}</div>" if (current_lang == "hi" and sch.get("hindi_name")) else ""
            
            with st.container():
                st.markdown(
                    f"""
                    <div class="scheme-card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span class="badge {level_badge}">{level_text}</span>
                                <span class="badge badge-category">{sch['category']}</span>
                                <span class="badge" style="background-color: #dcfce7; color: #166534;">Verified: {sch['last_verification_date']}</span>
                                <h3 style="margin: 0.4rem 0 0.1rem 0; color: #1e3a8a;">{display_name}</h3>
                                {secondary_name}
                                <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.3rem; margin-bottom: 0.6rem;">🏛️ {sch['department']}</div>
                            </div>
                        </div>
                        <p style="font-size: 0.92rem; color: #334155;">{sch['short_description']}</p>
                        <div style="background-color: #f8fafc; border-left: 3px solid #0f766e; padding: 0.6rem 0.8rem; border-radius: 4px; margin-bottom: 0.8rem;">
                            <strong style="color: #0f766e;">{t('key_benefits', current_lang)}:</strong> {sch['benefits']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                expander_label = f"📋 {'पात्रता मानदंड एवं दस्तावेज़ देखें: ' if current_lang == 'hi' else 'View Eligibility Criteria & Documents for '}{display_name}"
                with st.expander(expander_label):
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        st.markdown(f"**{'पात्रता आवश्यकताएं' if current_lang == 'hi' else 'Eligibility Requirements'}:**")
                        rules = sch.get("eligibility_rules", {})
                        if rules.get("min_age") or rules.get("max_age"):
                            st.write(f"- {'आयु सीमा:' if current_lang == 'hi' else 'Age limit:'} {rules.get('min_age', 0)} {'से' if current_lang == 'hi' else 'to'} {rules.get('max_age', 'कोई सीमा नहीं' if current_lang == 'hi' else 'No limit')} {'वर्ष' if current_lang == 'hi' else 'years'}")
                        if rules.get("max_income"):
                            st.write(f"- {'वार्षिक पारिवारिक आय सीमा:' if current_lang == 'hi' else 'Annual Income ceiling:'} ₹{rules.get('max_income'):,.0f}")
                        if rules.get("allowed_occupations"):
                            st.write(f"- {'लक्षित व्यवसाय:' if current_lang == 'hi' else 'Target Occupations:'} {', '.join(rules.get('allowed_occupations'))}")
                        if rules.get("allowed_states"):
                            st.write(f"- {'राज्य प्रयोज्यता:' if current_lang == 'hi' else 'State applicability:'} {', '.join(rules.get('allowed_states'))}")
                        if rules.get("exclusions"):
                            st.write(f"- {'प्रमुख बहिष्करण:' if current_lang == 'hi' else 'Key Exclusions:'} {', '.join(rules.get('exclusions')[:2])}")
                    with col_e2:
                        st.markdown(f"**{t('documents_needed', current_lang)}:**")
                        for d in sch.get("required_documents", []):
                            st.write(f"- {d}")

                    st.markdown(
                        f"""
                        🔗 **{t('official_info_label', current_lang)}:** <a href="{sch['official_information_url']}" target="_blank">{sch['official_information_url']}</a><br/>
                        """ +
                        (f"""📝 **{t('application_label', current_lang)}:** <a href="{sch['official_application_url']}" target="_blank">{sch['official_application_url']}</a>""" if sch.get('official_application_url') and 'http' in sch.get('official_application_url') else f"📝 **{t('application_label', current_lang)}:** {t('offline_app_note', current_lang)}"),
                        unsafe_allow_html=True
                    )

                    st.markdown("<br/>", unsafe_allow_html=True)
                    # Independent Single-Scheme PDF Checklist Download
                    try:
                        single_pdf_bytes = generate_single_scheme_pdf(
                            st.session_state.get("user_profile"),
                            sch,
                            eval_result=None,
                            lang=current_lang
                        )
                        btn_label = f"📥 {t('btn_download_single_pdf', current_lang)} ({display_name.split('(')[0].strip()})"
                        st.download_button(
                            label=btn_label,
                            data=single_pdf_bytes,
                            file_name=f"{sch.get('id', 'Scheme')}_Checklist_{current_lang}.pdf",
                            mime="application/pdf",
                            key=f"dl_exp_{sch.get('id', 'sch')}"
                        )
                    except Exception as pdf_err:
                        st.error(f"⚠️ Could not generate PDF for {sch.get('name')}: {pdf_err}")

# -----------------------------------------------------------------------------
# 7. View 4: Eligibility Results Dashboard
# -----------------------------------------------------------------------------
elif selected_nav == "results":
    st.subheader(f"📊 {t('nav_results', current_lang)}")

    evaluated = st.session_state["evaluated_schemes"]
    if not evaluated:
        st.warning("No scheme evaluations available. Please fill out your profile in 'Find My Schemes'.")
        st.stop()

    # Metric summary banners
    c1, c2, c3, c4 = st.columns(4)
    pot_count = sum(1 for s in evaluated if s["status"] == EligibilityResult.STATUS_POTENTIALLY_ELIGIBLE)
    verif_count = sum(1 for s in evaluated if s["status"] == EligibilityResult.STATUS_OFFICIAL_VERIFICATION)
    info_count = sum(1 for s in evaluated if s["status"] == EligibilityResult.STATUS_MORE_INFO_REQUIRED)
    inelig_count = sum(1 for s in evaluated if s["status"] == EligibilityResult.STATUS_LIKELY_INELIGIBLE)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">{t('status_potentially_eligible', current_lang)}</div>
                <div class="metric-val" style="color: #16a34a;">{pot_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">{t('status_official_verification', current_lang)}</div>
                <div class="metric-val" style="color: #0284c7;">{verif_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">{t('status_more_info_required', current_lang)}</div>
                <div class="metric-val" style="color: #ea580c;">{info_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Likely Ineligible</div>
                <div class="metric-val" style="color: #64748b;">{inelig_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # Filter Controls
    col_r1, col_r2, col_r3 = st.columns([2, 1, 1])
    with col_r1:
        res_query = st.text_input("Filter results", placeholder="Search evaluated schemes...", label_visibility="collapsed")
    with col_r2:
        status_filter = st.selectbox(
            "Status Filter",
            options=["All Statuses", EligibilityResult.STATUS_POTENTIALLY_ELIGIBLE, EligibilityResult.STATUS_OFFICIAL_VERIFICATION, EligibilityResult.STATUS_MORE_INFO_REQUIRED, EligibilityResult.STATUS_LIKELY_INELIGIBLE],
            label_visibility="collapsed"
        )
    with col_r3:
        sort_choice = st.selectbox(
            "Sort By",
            options=["Relevance Score (Highest First)", "Scheme Name (A-Z)"],
            label_visibility="collapsed"
        )

    filtered_res = filter_schemes(evaluated, query=res_query, status=status_filter)

    if sort_choice == "Scheme Name (A-Z)":
        filtered_res = sorted(filtered_res, key=lambda x: x["scheme_name"])
    else:
        # Default priority and relevance score
        pass

    st.caption(f"Showing **{len(filtered_res)}** evaluated schemes:")

    if not filtered_res:
        st.info(t("empty_results", current_lang))
    else:
        for idx, res in enumerate(filtered_res):
            status = res["status"]
            card_class = "scheme-card-ineligible"
            badge_class = "badge-ineligible"

            if status == EligibilityResult.STATUS_POTENTIALLY_ELIGIBLE:
                card_class = "scheme-card-eligible"
                badge_class = "badge-eligible"
                status_display = t("status_potentially_eligible", current_lang)
            elif status == EligibilityResult.STATUS_OFFICIAL_VERIFICATION:
                card_class = "scheme-card-verif"
                badge_class = "badge-verif"
                status_display = t("status_official_verification", current_lang)
            elif status == EligibilityResult.STATUS_MORE_INFO_REQUIRED:
                card_class = "scheme-card-info"
                badge_class = "badge-info"
                status_display = t("status_more_info_required", current_lang)
            else:
                status_display = t("status_likely_ineligible", current_lang)

            # Display Hindi scheme name prominently if Hindi mode is active
            display_name = res.get("hindi_name") if (current_lang == "hi" and res.get("hindi_name")) else res['scheme_name']
            secondary_name = f"<div style='font-size:0.85rem; color:#64748b;'>{res['scheme_name']}</div>" if (current_lang == "hi" and res.get("hindi_name")) else ""

            st.markdown(
                f"""
                <div class="scheme-card {card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="badge {badge_class}">{status_display}</span>
                            <span class="badge badge-category">{res.get('category')}</span>
                            <span class="badge badge-category">{res.get('scheme_level')}</span>
                            <h3 style="margin: 0.3rem 0 0.1rem 0; color: #1e3a8a;">{display_name}</h3>
                            {secondary_name}
                            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.3rem;">🏛️ {res.get('department')}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.3rem; font-weight: 700; color: #1e3a8a;">{res['relevance_score']}<span style="font-size: 0.85rem; color: #64748b;">/100</span></div>
                            <div style="font-size: 0.72rem; color: #64748b;" title="{res['score_disclaimer']}">{t('ranking_score', current_lang)} ℹ️</div>
                        </div>
                    </div>
                    <p style="font-size: 0.92rem; color: #334155; margin-top: 0.5rem;">{res.get('short_description')}</p>
                    <div style="background-color: #f8fafc; border-left: 3px solid #0f766e; padding: 0.6rem 0.8rem; border-radius: 4px; margin-bottom: 0.8rem;">
                        <strong style="color: #0f766e;">{t('key_benefits', current_lang)}:</strong> {res.get('benefits')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Condition details expander
            expander_title = f"🔍 {'विस्तृत मूल्यांकन विवरण: ' if current_lang == 'hi' else 'Detailed Evaluation Breakdown for '}{display_name}"
            with st.expander(expander_title, expanded=(idx == 0)):
                cond_col1, cond_col2 = st.columns(2)

                with cond_col1:
                    st.markdown(f"**{t('conditions_met', current_lang)}:**")
                    if res.get("satisfied_conditions"):
                        for sc in res["satisfied_conditions"]:
                            st.markdown(f"- ✅ **{sc['rule']}**: {sc['detail']}")
                    else:
                        st.caption("कोई विशिष्ट शर्त अभी पुष्ट नहीं हुई है।" if current_lang == "hi" else "No specific conditions confirmed yet.")

                    if res.get("information_required"):
                        st.markdown(f"<br/>**{t('info_needed', current_lang)}:**", unsafe_allow_html=True)
                        for ic in res["information_required"]:
                            st.markdown(f"- ⚠️ **{ic['rule']}**: {ic['action']}")

                with cond_col2:
                    st.markdown(f"**{t('conditions_unmet', current_lang)}:**")
                    if res.get("unsatisfied_conditions"):
                        for uc in res["unsatisfied_conditions"]:
                            st.markdown(f"- ❌ **{uc['rule']}**: {uc.get('reason', uc['detail'])}")
                    else:
                        st.markdown("*(कोई नहीं। सभी मूल्यांकन की गई शर्तें पूरी हैं!)*" if current_lang == "hi" else "*(None. All evaluated listed rules are satisfied!)*")

                    st.markdown(f"<br/>**{t('documents_needed', current_lang)}:**", unsafe_allow_html=True)
                    for d in res.get("required_documents", []):
                        st.markdown(f"- 📄 {d}")

                st.markdown("---")
                link_col1, link_col2 = st.columns(2)
                with link_col1:
                    st.markdown(f"🔗 **{t('official_info_label', current_lang)}:** [{res.get('official_information_url')}]({res.get('official_information_url')})")
                with link_col2:
                    app_link = res.get("official_application_url")
                    if app_link and "http" in app_link:
                        st.markdown(f"📝 **{t('application_label', current_lang)}:** [{app_link}]({app_link})")
                    else:
                        st.markdown(f"📝 **{t('application_label', current_lang)}:** {t('offline_app_note', current_lang)}")

                st.markdown("<br/>", unsafe_allow_html=True)
                # Customized Single Scheme PDF Download
                try:
                    res_pdf_bytes = generate_single_scheme_pdf(
                        st.session_state.get("user_profile"),
                        res,
                        eval_result=res,
                        lang=current_lang
                    )
                    short_title = display_name.split("(")[0].strip()
                    btn_label = f"📥 {t('btn_download_custom_pdf', current_lang)} ({short_title})"
                    st.download_button(
                        label=btn_label,
                        data=res_pdf_bytes,
                        file_name=f"{res.get('scheme_id', 'Scheme')}_Assessment_{current_lang}.pdf",
                        mime="application/pdf",
                        key=f"dl_res_{res.get('scheme_id', idx)}_{idx}"
                    )
                except Exception as pdf_err:
                    st.error(f"⚠️ Could not generate customized PDF: {pdf_err}")

# -----------------------------------------------------------------------------
# 8. View 5: Document Checklist
# -----------------------------------------------------------------------------
elif selected_nav == "checklist":
    st.subheader(f"📋 {t('nav_checklist', current_lang)}")
    st.write("Aggregated list of documents required for your potentially eligible schemes. Check off what you have ready!")

    checklist_data = aggregate_document_checklist(st.session_state["evaluated_schemes"])

    col_chk_top, col_chk_pdf = st.columns([3, 1])
    with col_chk_top:
        st.info(f"📑 Total unique documents identified across your eligible schemes: **{checklist_data['total_documents']}**")
    with col_chk_pdf:
        # Generate Consolidated PDF on demand with error boundary
        try:
            pdf_bytes = generate_eligibility_pdf(
                st.session_state.get("user_profile"),
                st.session_state.get("evaluated_schemes"),
                checklist_data,
                lang=current_lang
            )
            st.download_button(
                label=f"📥 {t('btn_download_pdf', current_lang)}",
                data=pdf_bytes,
                file_name="Govt_Schemes_Checklist_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as pdf_err:
            st.error(f"⚠️ Could not generate PDF report: {pdf_err}")

    # Optional Scheme-Specific PDF Checklist selector
    exp_single_title = "📄 किसी विशिष्ट योजना की चेकलिस्ट डाउनलोड करें" if current_lang == "hi" else "📄 Download Checklist for a Specific Individual Scheme"
    with st.expander(exp_single_title):
        scheme_options = ALL_SCHEMES
        scheme_labels = [f"{s.get('hindi_name') or s['name']} ({s['category']})" if current_lang == "hi" else f"{s['name']} ({s['category']})" for s in scheme_options]
        sel_idx = st.selectbox(
            "योजना चुनें" if current_lang == "hi" else "Select Scheme",
            options=range(len(scheme_options)),
            format_func=lambda i: scheme_labels[i],
            key="chk_single_scheme_sel"
        )
        selected_sch = scheme_options[sel_idx]
        display_sch_name = selected_sch.get('hindi_name') or selected_sch['name']

        # Find if this scheme has an evaluation in session state
        matching_eval = next((e for e in st.session_state.get("evaluated_schemes", []) if e.get("scheme_id") == selected_sch.get("id")), None)
        try:
            single_bytes = generate_single_scheme_pdf(
                st.session_state.get("user_profile"),
                selected_sch,
                eval_result=matching_eval,
                lang=current_lang
            )
            btn_single_label = f"📥 {t('btn_download_single_pdf', current_lang)} ({display_sch_name.split('(')[0].strip()})"
            st.download_button(
                label=btn_single_label,
                data=single_bytes,
                file_name=f"{selected_sch.get('id', 'Scheme')}_Checklist_{current_lang}.pdf",
                mime="application/pdf",
                key="btn_chk_single_dl"
            )
        except Exception as pdf_err:
            st.error(f"⚠️ Could not generate scheme checklist: {pdf_err}")

    st.markdown("<br/>", unsafe_allow_html=True)

    categories = checklist_data.get("categories", {})
    if not categories:
        st.warning("कोई दस्तावेज़ वर्तमान में आवश्यक नहीं है।" if current_lang == "hi" else "No documents currently required as no schemes are marked as potentially eligible. Check your profile details.")
    else:
        for cat_name, doc_items in categories.items():
            st.markdown(f"#### 📂 {cat_name}")
            for item in doc_items:
                doc_name = item["document"]
                schemes_str = ", ".join(item["schemes"])
                c_box, c_txt = st.columns([0.05, 0.95])
                with c_box:
                    st.checkbox("", key=f"chk_{doc_name}", label_visibility="collapsed")
                with c_txt:
                    st.markdown(f"**{doc_name}**")
                    st.caption(f"{'आवश्यकता:' if current_lang == 'hi' else 'Required by:'} *{schemes_str}*")
            st.markdown("---")

    st.info(f"💡 {t('pro_tip', current_lang)}")

# -----------------------------------------------------------------------------
# 9. View 6: AI Assistant
# -----------------------------------------------------------------------------
elif selected_nav == "ai_assistant":
    st.subheader(f"🤖 {t('nav_ai_assistant', current_lang)}")
    st.write("सरकारी योजनाओं के नियम, पात्रता, आवश्यक दस्तावेज़ और आवेदन प्रक्रिया के बारे में कोई भी प्रश्न पूछें।" if current_lang == "hi" else "Ask natural language questions about scheme rules, eligibility status, documentation, and application procedures.")

    # Explanation generator button
    st.markdown(f"#### ⚡ {'त्वरित कार्य' if current_lang == 'hi' else 'Quick Actions'}")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    with quick_col1:
        if st.button(t("btn_explain_fit", current_lang), use_container_width=True):
            top_pot = [s for s in st.session_state["evaluated_schemes"] if s["status"] == "Potentially Eligible"]
            if top_pot:
                best = top_pot[0]
                explanation = explain_scheme_fit(best["scheme_name"], best, lang=current_lang)
                st.session_state["chat_history"].append({"role": "assistant", "content": explanation})
            else:
                st.session_state["chat_history"].append({"role": "assistant", "content": "वर्तमान में कोई योजना संभावित रूप से पात्र नहीं है। कृपया अपनी प्रोफ़ाइल अपडेट करें।" if current_lang == "hi" else "No schemes are currently marked Potentially Eligible to explain. Try updating your profile."})
            st.rerun()

    with quick_col2:
        if st.button(t("btn_summarize_checklist", current_lang), use_container_width=True):
            chk_data = aggregate_document_checklist(st.session_state["evaluated_schemes"])
            summary = explain_checklist_summary(chk_data, lang=current_lang)
            st.session_state["chat_history"].append({"role": "assistant", "content": summary})
            st.rerun()

    with quick_col3:
        if st.button(t("btn_clear_chat", current_lang), use_container_width=True):
            st.session_state["chat_history"] = []
            st.toast("बातचीत का इतिहास साफ़ किया गया" if current_lang == "hi" else "Chat history cleared")
            st.rerun()

    st.markdown("---")

    # Display chat conversation
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

    # User input
    user_query = st.chat_input(t("chat_placeholder", current_lang))
    if user_query:
        # Append user message
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        # Generate response using AI Assistant module
        with st.spinner("Analyzing verified scheme database..."):
            reply = ask_ai_assistant(
                user_query,
                st.session_state["user_profile"],
                st.session_state["evaluated_schemes"],
                lang=current_lang
            )
            st.session_state["chat_history"].append({"role": "assistant", "content": reply})
            st.chat_message("assistant").markdown(reply)

# -----------------------------------------------------------------------------
# 10. View 7: About the Project
# -----------------------------------------------------------------------------
elif selected_nav == "about":
    st.subheader("ℹ️ About the Project: Government Scheme Navigator")
    st.markdown(
        """
        ### 🎯 Problem Statement & Mission
        India operates some of the world's most progressive social welfare programs. However, millions of eligible citizens
        fail to access their entitled benefits due to complex documentation, information fragmentation, and confusion
        regarding eligibility criteria.
        
        The **Government Scheme Navigator** is an open-source civic tech innovation designed for college hackathons to empower
        citizens with transparent, deterministic, and accessible scheme discovery.

        ---

        ### ⚙️ Technical Architecture
        - **Frontend & Interaction:** Streamlit 1.51 with responsive styling, bilingual UI (English & Hindi), and instant feedback.
        - **Rule Engine:** 100% deterministic, transparent Python rule evaluator. It checks age boundaries, income ceilings,
          geographic residency, farmer landholding, and explicit disqualifiers without relying on opaque black-box AI.
        - **AI Assistant:** Dual-mode assistant featuring a zero-cost deterministic grounded fallback engine that strictly
          cites the loaded scheme dataset, plus optional Google Gemini REST API support.
        - **Document Synthesis & PDF Export:** ReportLab-powered document checklist generator creating printable, multi-page civic reports.
        - **Data Integrity:** 20 verified Indian government schemes across central ministries and state governments (myScheme, PM-KISAN, NHA, PMAY, NSAP, MUDRA).

        ---

        ### 🛡️ Responsible AI & Civic Safeguards
        1. **Deterministic Grounding:** Decisions are made by the verifiable rule engine, NOT by probabilistic LLMs.
        2. **Zero Fabrication:** The system never invents schemes, benefits, deadlines, or application links.
        3. **No Private Identifiers:** We strictly do not collect Aadhaar numbers, PAN, bank account numbers, or OTPs.
        4. **Transparent Verification:** State schemes are clearly distinguished from Central programs, and verification dates are published for every record.
        """
    )

# -----------------------------------------------------------------------------
# 11. Global Civic Disclaimer & Responsible AI Footer
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="app-footer">
        <p><strong>Civic Notice & Disclaimer:</strong> {t('disclaimer_text', current_lang)}</p>
        <p style="margin-top: 0.5rem;">
            National Government Portals: 
            <a href="https://www.myscheme.gov.in/" target="_blank">myScheme.gov.in</a> &bull; 
            <a href="https://india.gov.in/" target="_blank">india.gov.in</a> &bull; 
            <a href="https://scholarships.gov.in/" target="_blank">National Scholarship Portal</a> &bull; 
            <a href="https://pmkisan.gov.in/" target="_blank">PM-KISAN</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
