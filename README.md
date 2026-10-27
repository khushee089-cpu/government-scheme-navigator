# Government Scheme Navigator 🇮🇳
> *"The Right Government Scheme for Every Citizen."*

An intelligent, deterministic, and civic-first web application designed for hackathons that empowers Indian citizens to discover welfare schemes tailored to their demographic and economic circumstances, understand exact eligibility conditions, review required documentation, and apply safely through verified official government portals.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/pytest-30%20passed-brightgreen.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bilingual](https://img.shields.io/badge/Language-English%20%7C%20%E0%A4%B9%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%80-orange.svg)](#bilingual-support)

---

## 📑 Table of Contents
1. [Project Highlights & Architecture](#-project-highlights--architecture)
2. [Why This Solution? (Hackathon Pitch)](#-why-this-solution-hackathon-pitch)
3. [Technology Stack](#-technology-stack)
4. [Project File Structure](#-project-file-structure)
5. [Windows Quick Start (For Beginners)](#-windows-quick-start-for-beginners)
6. [Interactive Sections Walkthrough](#-interactive-sections-walkthrough)
7. [Deterministic Rule Engine Methodology](#-deterministic-rule-engine-methodology)
8. [AI Assistant: Grounded Fallback vs LLM](#-ai-assistant-grounded-fallback-vs-llm)
9. [Preconfigured Demo Personas](#-preconfigured-demo-personas)
10. [Scheme Dataset & Verification Table](#-scheme-dataset--verification-table)
11. [Running the Automated Test Suite](#-running-the-automated-test-suite)
12. [Responsible AI & Civic Ethics Disclaimers](#-responsible-ai--civic-ethics-disclaimers)

---

## 🌟 Project Highlights & Architecture

- **100% Deterministic Rule Engine:** Evaluates age, annual income ceilings, state domicile, occupation, gender, social category, and landholding. Unlike black-box generative models that hallucinate eligibility, our engine uses strict rule evaluation with complete condition transparency.
- **20 Authentic Verified Schemes:** Curated across central ministries and key state governments covering farmers, students, women entrepreneurs, artisans, senior citizens, and urban street vendors.
- **Bilingual Interface:** Full native support for **English** and **हिन्दी (Hindi)**.
- **Dual-Mode AI Assistant:** Operates seamlessly offline with zero API key required using a deterministic dataset reasoner, with optional Google Gemini LLM API integration.
- **Consolidated Document Checklist & ReportLab PDF Export:** Synthesizes all required documentation across eligible schemes and generates a professional, downloadable multi-page PDF checklist.
- **Strict Privacy by Design:** **Never** asks for Aadhaar numbers, PAN, bank account credentials, or OTPs.

---

## 🎯 Why This Solution? (Hackathon Pitch)

India has hundreds of progressive welfare programs, yet millions of eligible citizens miss out due to:
1. **Information Asymmetry:** Scheme rules are scattered across dozens of ministry portals.
2. **Ambiguous Criteria:** Citizens are unsure if their exact income, age, or landholding qualifies them.
3. **Paperwork Uncertainty:** Not knowing which documents are needed before queuing up at CSC or government offices.

**The Solution:** The Government Scheme Navigator acts as an intelligent civic bridge:
`Citizen Circumstances` ➡️ `Rule-Based Evaluation` ➡️ `Status & Score` ➡️ `Paperwork Checklist` ➡️ `Official Government Portal (.gov.in)`.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit 1.51 | Modern, mobile-responsive dashboard with custom styling |
| **Backend & Rules** | Python 3.10+ | Clean, modular object-oriented architecture |
| **Scheme Database** | Structured JSON | 20 verified schemes with strict schema validation |
| **PDF Generation** | ReportLab | High-resolution multi-page PDF generator with dynamic pagination |
| **Testing** | pytest | 30 comprehensive automated tests |
| **Data Processing** | Pandas | Tabular filtering and search aggregation |
| **AI Integration** | REST / Fallback | Dual-mode: Local Grounded Reasoner + Optional Gemini API |

---

## 📂 Project File Structure

```text
government-scheme-navigator/
│
├── app.py                      # Main Streamlit web application & UI orchestrator
├── schemes.json                # Primary database of 20 verified government schemes
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation & hackathon guide
├── .env.example                # Sample environment configuration (optional LLM API key)
├── .gitignore                  # Git ignore rules for Python, cache, and secrets
│
├── modules/                    # Clean modular backend
│   ├── __init__.py
│   ├── data_loader.py          # JSON schema validation, caching, and retrieval
│   ├── eligibility.py          # Deterministic rule engine & condition breakdowns
│   ├── recommendations.py      # Multi-faceted search filters & document aggregator
│   ├── demo_profiles.py        # 5 pre-built hackathon demo personas
│   ├── translations.py         # Full English & Hindi bilingual dictionary
│   ├── ai_assistant.py         # Dual-mode AI: grounded offline engine + optional LLM
│   └── pdf_generator.py        # ReportLab PDF checklist & evaluation report generator
│
├── tests/                      # Automated test suite (30 passing tests)
│   ├── __init__.py
│   ├── test_eligibility.py     # Age/income boundaries, exclusions, missing data
│   ├── test_data.py            # Dataset schema, URL integrity, required fields
│   ├── test_demo_profiles.py   # Verification of the 5 hackathon personas
│   ├── test_ai_assistant.py    # Fallback mode, Hindi Q&A, grounded responses
│   ├── test_pdf.py             # PDF generation, binary validation, unicode handling
│   └── test_translations.py    # Translation dictionary coverage and fallbacks
│
├── assets/                     # Graphics and static branding
│   ├── logo.svg                # Vector SVG logo emblem
│   └── logo.png                # High-res emblem for Streamlit sidebar
│
└── data/
    └── schemes.json            # Backup copy of scheme database
```

---

## 💻 Windows Quick Start (For Beginners)

### Step 1: Open Terminal in Project Directory
Open **PowerShell** or **Command Prompt** and navigate to your project folder:
```powershell
cd "c:\Users\DELL\Documents\Govt Scheme navigator"
```

### Step 2: Install Dependencies (If needed)
If running on Anaconda (which already has Python, Streamlit, and Pandas):
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Run the Automated Test Suite
Verify that all 30 tests pass:
```powershell
python -m pytest -v
```

### Step 4: Launch the Streamlit Web Application
```powershell
python -m streamlit run app.py
```
Your default web browser will automatically open:
```text
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

*(Press `Ctrl + C` in the terminal when you wish to stop the application).*

---

## 🧭 Interactive Sections Walkthrough

1. **🏠 Home:** Attractive landing page with key statistics, "How It Works" 4-step workflow, and featured welfare programs.
2. **📝 Find My Schemes:** Clean citizen profile form with validation, demographic controls, and 1-click **Demo Persona** loaders.
3. **🔍 Scheme Explorer:** Public catalog to search all 20 schemes by keyword, department, or category without requiring a profile.
4. **📊 Eligibility Results:** Dynamic result cards categorized by:
   - `Potentially Eligible` (Green)
   - `Official Verification Required` (Blue)
   - `More Information Required` (Orange)
   - `Likely Ineligible Under Listed Rules` (Slate)
   Includes exact condition breakdowns (met vs unmet rules) and internal ranking scores.
5. **📋 Document Checklist:** Categorized paperwork tracker (KYC, Banking/DBT, Income, Land/Occupation) with **instant PDF download**.
6. **🤖 AI Assistant:** Chatbot supporting English and Hindi. Explains why you matched or didn't match a scheme, provides document summaries, and cites official links.
7. **ℹ️ About the Project:** Complete architecture, civic technology mission, and verification methodology.

---

## ⚙️ Deterministic Rule Engine Methodology

Unlike generative AI wrappers that guess whether someone is eligible, our rule engine is **100% deterministic, auditable, and transparent**:

```text
User Profile ──► 1. State Domicile (Central vs State Restriction)
                 2. Age Permissibility (min_age <= Age <= max_age)
                 3. Income Ceiling (Income <= max_income)
                 4. Occupation Match (Farmer, Student, Artisan, etc.)
                 5. Gender Targeting (e.g. Women-only schemes)
                 6. Social Category Earmarks (SC/ST/OBC/EWS)
                 7. Disqualifier Check (Income tax, existing LPG, pucca house)
                 │
                 ▼
         Condition Breakdown:
         - Satisfied Conditions (Met)
         - Unsatisfied Conditions (Unmet + specific reason)
         - Information Still Required (Missing fields)
                 │
                 ▼
         Status: Potentially Eligible | Official Verification Needed |
                 More Info Needed | Likely Ineligible
```

### Internal Relevance Score Disclaimer
The relevance score (0–100) is an **internal ranking heuristic** used purely to sort search results based on target demographic alignment. It does **not** represent a mathematical probability of government approval.

---

## 🤖 AI Assistant: Grounded Fallback vs LLM

The application is engineered with a **fail-safe dual architecture**:

### 1. Grounded Offline Fallback Engine (Default)
- **Zero Cost & Offline:** Does not require an internet connection or any API key.
- **Zero Hallucination:** Directly parses the structured `schemes.json` dataset to extract benefits, rules, required paperwork, and official portal links.
- **Bilingual:** Fully supports questions in both English and Hindi.

### 2. Optional Google Gemini LLM API
- If a `GEMINI_API_KEY` is provided in `.env`, the assistant passes query context to Google Gemini with strict prompt guardrails forbidding the invention of schemes, deadlines, or false promises.

---

## 👥 Preconfigured Demo Personas

The sidebar and profile form include 5 preconfigured, realistic, fictional user personas for instant hackathon evaluation:

| Persona | Demographics | Key Circumstances | Primary Expected Matches |
| :--- | :--- | :--- | :--- |
| **1. Ramesh Patel** | 44, Male, Uttarakhand | Small farmer, 1.2 ha land, ₹1,40,000 income | PM-KISAN, PMMSY, PMSBY, APY |
| **2. Priya Sharma** | 19, Female, Maharashtra | Undergraduate SC student, ₹1,80,000 income | Post-Matric SC/ST Scholarship, NAPS, PMKVY 4.0 |
| **3. Sunita Devi** | 32, Female, Uttar Pradesh | Rural woman entrepreneur & artisan, ₹1,20,000 | Stand-Up India, PMMY Mudra, PMUY Ujjwala 2.0 |
| **4. Manoj Kumar** | 28, Male, Delhi | Urban street food vendor, ₹95,000 income | PM SVANidhi, PMMY Shishu, PMSBY, APY |
| **5. Ram Lal** | 66, Male, Rajasthan | Low-income senior citizen, ₹48,000 income | IGNOAPS Old Age Pension, Ayushman Bharat PM-JAY |

---

## 📋 Scheme Dataset & Verification Table

All 20 schemes are verified against official government portals:

| ID | Scheme Name | Department / Ministry | Level | Verification Portal |
| :--- | :--- | :--- | :--- | :--- |
| `SCHEME-001` | PM-KISAN | Agriculture & Farmers Welfare | Central | https://pmkisan.gov.in/ |
| `SCHEME-002` | Ayushman Bharat (PM-JAY) | National Health Authority (MoHFW) | Central | https://nha.gov.in/ |
| `SCHEME-003` | PMAY-G (Gramin Housing) | Ministry of Rural Development | Central | https://pmayg.nic.in/ |
| `SCHEME-004` | PMAY-U 2.0 (Urban Housing) | Housing & Urban Affairs | Central | https://pmay-urban.gov.in/ |
| `SCHEME-005` | PMUY 2.0 (Ujjwala LPG) | Petroleum & Natural Gas | Central | https://www.pmuy.gov.in/ |
| `SCHEME-006` | PMMY (Mudra Loan) | Financial Services, Ministry of Finance | Central | https://www.mudra.org.in/ |
| `SCHEME-007` | PM Vishwakarma | Ministry of MSME | Central | https://pmvishwakarma.gov.in/ |
| `SCHEME-008` | PM SVANidhi (Street Vendors) | Housing & Urban Affairs | Central | https://pmsvanidhi.mohua.gov.in/ |
| `SCHEME-009` | IGNOAPS (NSAP Pension) | Ministry of Rural Development | Central | https://nsap.nic.in/ |
| `SCHEME-010` | Post-Matric SC/ST Scholarship | Social Justice & Tribal Affairs | Central | https://scholarships.gov.in/ |
| `SCHEME-011` | Stand-Up India | Financial Services / SIDBI | Central | https://www.standupmitra.in/ |
| `SCHEME-012` | Atal Pension Yojana (APY) | PFRDA / Ministry of Finance | Central | https://www.npscra.nsdl.co.in/ |
| `SCHEME-013` | PM Suraksha Bima (PMSBY) | Financial Services, Ministry of Finance | Central | https://www.jansuraksha.gov.in/ |
| `SCHEME-014` | Sukanya Samriddhi Yojana (SSY) | Dept of Posts / Ministry of Finance | Central | https://www.indiapost.gov.in/ |
| `SCHEME-015` | PMKVY 4.0 (Skill India) | Skill Development & MSDE / NSDC | Central | https://www.pmkvyofficial.org/ |
| `SCHEME-016` | PM Matsya Sampada (PMMSY) | Department of Fisheries | Central | https://pmmsy.dof.gov.in/ |
| `SCHEME-017` | NAPS (Apprenticeship) | Skill Development & MSDE | Central | https://www.apprenticeshipindia.gov.in/ |
| `SCHEME-018` | Mukhyamantri Kanya Sumangala | Women & Child Development, UP | State | https://mksy.up.gov.in/ |
| `SCHEME-019` | Kalaignar Magalir Urimai | Special Programmes, Tamil Nadu | State | https://kmut.tn.gov.in/ |
| `SCHEME-020` | Yuva Sambal Yojana | Skill & Employment, Rajasthan | State | https://employment.livelihoods.rajasthan.gov.in/ |

---

## 🧪 Running the Automated Test Suite

We follow strict test-driven quality assurance. Run all 30 tests via:

```powershell
python -m pytest -v
```

Expected test execution output:
```text
============================= test session starts =============================
collected 30 items

tests/test_ai_assistant.py::test_missing_api_key_safe_fallback PASSED    [  3%]
tests/test_ai_assistant.py::test_scheme_query_in_hindi PASSED            [  6%]
tests/test_ai_assistant.py::test_explain_scheme_fit PASSED               [ 10%]
tests/test_ai_assistant.py::test_explain_checklist_summary PASSED        [ 13%]
tests/test_data.py::test_scheme_count PASSED                             [ 16%]
tests/test_data.py::test_scheme_required_fields PASSED                   [ 20%]
tests/test_data.py::test_official_urls PASSED                            [ 23%]
tests/test_data.py::test_central_and_state_schemes PASSED                [ 26%]
tests/test_data.py::test_documents_non_empty PASSED                      [ 30%]
tests/test_data.py::test_data_loader_corrupted_file PASSED               [ 33%]
tests/test_data.py::test_data_loader_missing_file PASSED                 [ 36%]
tests/test_demo_profiles.py::test_persona_1_ramesh_patel_farmer PASSED   [ 40%]
tests/test_demo_profiles.py::test_persona_2_priya_sharma_student PASSED  [ 43%]
tests/test_demo_profiles.py::test_persona_3_sunita_devi_woman_entrepreneur PASSED [ 46%]
tests/test_demo_profiles.py::test_persona_4_manoj_kumar_street_vendor PASSED [ 50%]
tests/test_demo_profiles.py::test_persona_5_ram_lal_senior_citizen PASSED [ 53%]
tests/test_eligibility.py::test_pm_kisan_eligible_profile PASSED         [ 56%]
tests/test_eligibility.py::test_pm_kisan_tax_payer_ineligible PASSED     [ 60%]
tests/test_eligibility.py::test_pm_kisan_missing_landholding PASSED      [ 63%]
tests/test_age_boundary_conditions PASSED           [ 66%]
tests/test_income_boundary_conditions PASSED        [ 70%]
tests/test_state_specific_restrictions PASSED       [ 73%]
tests/test_gender_restriction PASSED                [ 76%]
tests/test_completely_empty_profile_does_not_crash PASSED [ 80%]
tests/test_evaluate_all_schemes_sorting PASSED      [ 83%]
tests/test_pdf.py::test_pdf_generation_basic PASSED                      [ 86%]
tests/test_pdf.py::test_pdf_generation_hindi_mode PASSED                 [ 90%]
tests/test_pdf.py::test_clean_text_for_pdf PASSED                        [ 93%]
tests/test_translations.py::test_translation_keys_completeness PASSED    [ 96%]
tests/test_translations.py::test_t_function_helper PASSED                [100%]

============================= 30 passed in 0.54s ==============================
```

---

## ⚖️ Responsible AI & Civic Ethics Disclaimers

1. **Independent Civic Project:** The *Government Scheme Navigator* is an independent educational and civic assistance application developed for hackathons. It is **not** an official agency of the Government of India or any State Government.
2. **No Guarantee of Benefits:** This application does **not** guarantee eligibility, benefits approval, loan sanction, or monetary disbursement.
3. **Dynamic Government Guidelines:** Scheme rules, budget outlays, income criteria, and application windows are revised periodically by relevant government ministries. Citizens must verify all requirements on the respective official portals (`.gov.in` / `.nic.in`) before applying.
4. **Data Privacy:** This application does **not** store personal identifiable records or transmit sensitive citizen records to third parties.

---

**Developed for College Hackathon Excellence** 🇮🇳
Made with Python, Streamlit & ReportLab.
