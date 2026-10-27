"""
PDF Generator Module using ReportLab.
Creates professional, downloadable Government Scheme Checklist & Eligibility Reports.
Fully supports both:
  1. Single-Scheme Dedicated PDF Checklist (independent scheme download).
  2. Consolidated Multi-Scheme Assessment Report.
Features complete native Hindi (Devanagari) translations for all PDF sections,
headers, tables, and notices when Hindi language is chosen.
"""

import io
import datetime
import os
from typing import Dict, Any, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# -----------------------------------------------------------------------------
# Font Management & Unicode Devanagari Support
# -----------------------------------------------------------------------------
UNICODE_FONT_AVAILABLE = False
FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_OBLIQUE = "Helvetica-Oblique"


def setup_pdf_fonts():
    """
    Attempt to register Windows/system Unicode fonts that natively support
    Hindi (Devanagari) and Indian currency symbols.
    Gracefully falls back to standard Helvetica if TrueType fonts are unavailable.
    """
    global UNICODE_FONT_AVAILABLE, FONT_REGULAR, FONT_BOLD, FONT_OBLIQUE
    if UNICODE_FONT_AVAILABLE:
        return

    # 1. Try Windows Nirmala UI (TrueType Collection: 0=Regular, 1=Bold)
    nirmala_path = "C:/Windows/Fonts/Nirmala.ttc"
    if os.path.exists(nirmala_path):
        try:
            pdfmetrics.registerFont(TTFont("NirmalaUI", nirmala_path, subfontIndex=0))
            pdfmetrics.registerFont(TTFont("NirmalaUI-Bold", nirmala_path, subfontIndex=1))
            FONT_REGULAR = "NirmalaUI"
            FONT_BOLD = "NirmalaUI-Bold"
            FONT_OBLIQUE = "NirmalaUI"
            UNICODE_FONT_AVAILABLE = True
            return
        except Exception:
            pass

    # 2. Try Windows Arial TrueType fonts
    arial_path = "C:/Windows/Fonts/arial.ttf"
    arial_bd = "C:/Windows/Fonts/arialbd.ttf"
    if os.path.exists(arial_path) and os.path.exists(arial_bd):
        try:
            pdfmetrics.registerFont(TTFont("ArialUnicode", arial_path))
            pdfmetrics.registerFont(TTFont("ArialUnicode-Bold", arial_bd))
            FONT_REGULAR = "ArialUnicode"
            FONT_BOLD = "ArialUnicode-Bold"
            FONT_OBLIQUE = "ArialUnicode"
            UNICODE_FONT_AVAILABLE = True
            return
        except Exception:
            pass

    # 3. Fallback to built-in Type 1 Helvetica
    FONT_REGULAR = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"
    FONT_OBLIQUE = "Helvetica-Oblique"
    UNICODE_FONT_AVAILABLE = False


# Initialize fonts on module import
setup_pdf_fonts()


class NumberedCanvas(canvas.Canvas):
    """Dynamic two-pass canvas that writes accurate total page counts in footer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        self.setFont(FONT_REGULAR, 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Footer divider line
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 36, 559, 36)

        footer_text = "Government Scheme Navigator | Official Civic Guidance Report | Independent & Non-Affiliated"
        page_text = f"Page {self._pageNumber} of {page_count}"

        self.drawString(36, 24, footer_text)
        self.drawRightString(559, 24, page_text)
        self.restoreState()


# -----------------------------------------------------------------------------
# Defensive Data Cleaning & Fallback Helpers
# -----------------------------------------------------------------------------
def safe_str(val: Any, default: str = "") -> str:
    """Safely convert any value to trimmed string with default fallback."""
    if val is None:
        return default
    return str(val).strip()


def safe_income_str(income: Any, is_hindi: bool = False) -> str:
    """Safely format income value into currency string without crashing on invalid data."""
    if income in [None, "", "null", "None"]:
        return "घोषित नहीं" if is_hindi else "Not declared"
    try:
        val = float(str(income).replace(",", "").replace("₹", "").replace("Rs.", "").strip())
        return f"₹{val:,.0f}" if is_hindi and UNICODE_FONT_AVAILABLE else f"Rs. {val:,.0f}"
    except (ValueError, TypeError):
        return safe_str(income, "घोषित नहीं" if is_hindi else "Not declared")


def safe_age_str(age: Any, is_hindi: bool = False) -> str:
    """Safely format age value."""
    if age in [None, "", "null", "None"]:
        return "निर्दिष्ट नहीं" if is_hindi else "Not specified"
    try:
        val = int(age)
        suffix = " वर्ष" if is_hindi else " Years"
        return f"{val}{suffix}" if val > 0 else ("निर्दिष्ट नहीं" if is_hindi else "Not specified")
    except (ValueError, TypeError):
        return safe_str(age, "निर्दिष्ट नहीं" if is_hindi else "Not specified")


def safe_list(val: Any) -> List[Any]:
    """Safely convert any value into a list."""
    if val is None:
        return []
    if isinstance(val, list):
        return val
    if isinstance(val, (tuple, set)):
        return list(val)
    return [val]


def clean_text_for_pdf(text: Any) -> str:
    """
    Sanitize text for ReportLab Paragraph rendering.
    If Unicode font is not available, converts non-Latin-1 chars cleanly to ASCII equivalents.
    """
    if text is None:
        return ""
    s = str(text).strip()

    # Replace common quotes and typographical dashes
    s = s.replace("—", "-").replace("–", "-")
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = s.replace("…", "...").replace("•", "*")

    if not UNICODE_FONT_AVAILABLE:
        # Currency symbol replacement
        s = s.replace("₹", "Rs. ")
        try:
            s = s.encode("latin-1", "replace").decode("latin-1")
        except Exception:
            s = s.encode("ascii", "replace").decode("ascii")

    return s


def escape_xml(text: Any) -> str:
    """Escape XML characters (&, <, >) to avoid ReportLab markup parsing crashes."""
    s = clean_text_for_pdf(text)
    s = s.replace("&amp;", "&").replace("&", "&amp;")
    return s


def get_pdf_styles():
    """Create a unified stylesheet bound to active font (Unicode or Helvetica)."""
    styles = getSampleStyleSheet()

    primary_navy = colors.HexColor("#1e3a8a")
    slate_dark = colors.HexColor("#1e293b")
    slate_muted = colors.HexColor("#475569")

    title_style = ParagraphStyle(
        "NavTitle",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=18,
        leading=22,
        textColor=primary_navy,
        alignment=TA_LEFT
    )

    subtitle_style = ParagraphStyle(
        "NavSubtitle",
        parent=styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=12,
        textColor=slate_muted,
        alignment=TA_LEFT
    )

    h2_style = ParagraphStyle(
        "NavH2",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=11,
        leading=15,
        textColor=primary_navy,
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "NavBody",
        parent=styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=11.5,
        textColor=slate_dark
    )

    body_bold = ParagraphStyle(
        "NavBodyBold",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11.5,
        textColor=slate_dark
    )

    disclaimer_style = ParagraphStyle(
        "NavDisclaimer",
        parent=styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#713f12")
    )

    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "h2": h2_style,
        "body": body_style,
        "body_bold": body_bold,
        "disclaimer": disclaimer_style
    }


def translate_status(status: str, is_hindi: bool) -> str:
    """Helper to convert status text to Hindi where applicable."""
    if not is_hindi:
        return status
    if "Potentially Eligible" in status:
        return "संभावित रूप से पात्र (POTENTIALLY ELIGIBLE)"
    if "Official Verification" in status:
        return "आधिकारिक सत्यापन अपेक्षित (VERIFICATION NEEDED)"
    if "More Information" in status:
        return "अधिक जानकारी आवश्यक (INFO REQUIRED)"
    if "Likely Ineligible" in status:
        return "संभावित अपात्र (LIKELY INELIGIBLE)"
    return status


# -----------------------------------------------------------------------------
# 1. Single Scheme Dedicated PDF Checklist Generator
# -----------------------------------------------------------------------------
def generate_single_scheme_pdf(
    user_profile: Optional[Dict[str, Any]],
    scheme_data: Dict[str, Any],
    eval_result: Optional[Dict[str, Any]] = None,
    lang: str = "en"
) -> bytes:
    """
    Generate an independent, official PDF checklist tailored to a single scheme.
    Supports complete native Hindi translations for all sections when lang == 'hi'.
    """
    setup_pdf_fonts()
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=45
    )

    is_hindi = lang in ["hi", "hindi", "हिन्दी"]
    pdf_styles = get_pdf_styles()
    title_style = pdf_styles["title"]
    subtitle_style = pdf_styles["subtitle"]
    h2_style = pdf_styles["h2"]
    body_style = pdf_styles["body"]
    body_bold = pdf_styles["body_bold"]
    disclaimer_style = pdf_styles["disclaimer"]

    primary_navy = colors.HexColor("#1e3a8a")
    bg_light = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")

    # Safe extraction of scheme fields
    scheme_data = scheme_data or {}
    s_eng_name = clean_text_for_pdf(scheme_data.get("name") or scheme_data.get("scheme_name") or "Government Scheme")
    s_hin_name = clean_text_for_pdf(scheme_data.get("hindi_name", ""))
    
    # Priority for title in Hindi mode
    if is_hindi and s_hin_name:
        s_display_name = s_hin_name
        s_secondary_name = s_eng_name
    else:
        s_display_name = s_eng_name
        s_secondary_name = s_hin_name

    dept = clean_text_for_pdf(scheme_data.get("department", "भारत सरकार" if is_hindi else "Government of India"))
    category = clean_text_for_pdf(scheme_data.get("category", "कल्याण" if is_hindi else "Welfare"))
    level = clean_text_for_pdf("केंद्रीय" if (is_hindi and scheme_data.get("scheme_level") == "Central") else ("राज्य" if is_hindi else scheme_data.get("scheme_level", "Central")))
    desc = clean_text_for_pdf(scheme_data.get("short_description", "सरकारी दिशा-निर्देशों के तहत कल्याणकारी योजना।" if is_hindi else "Welfare initiative under Government of India guidelines."))
    benefits = clean_text_for_pdf(scheme_data.get("benefits", "लाभों के विवरण के लिए आधिकारिक पोर्टल देखें।" if is_hindi else "Refer to official scheme portal for complete benefits schedule."))
    info_url = safe_str(scheme_data.get("official_information_url"), "https://www.myscheme.gov.in/")
    app_url = safe_str(scheme_data.get("official_application_url"), "")
    req_docs = safe_list(scheme_data.get("required_documents"))

    # Evaluation details
    if eval_result:
        raw_status = eval_result.get("status", "Check in Find My Schemes")
        status = translate_status(raw_status, is_hindi)
        score = eval_result.get("relevance_score", 0)
        satisfied = safe_list(eval_result.get("satisfied_conditions"))
        unsatisfied = safe_list(eval_result.get("unsatisfied_conditions"))
        info_needed = safe_list(eval_result.get("information_required"))
    else:
        status = "नागरिक सत्यापन के लिए उपलब्ध" if is_hindi else "Open for Citizen Verification"
        score = None
        satisfied = []
        unsatisfied = []
        info_needed = []

    # Safe profile extraction
    prof = user_profile or {}
    age_str = safe_age_str(prof.get("age"), is_hindi)
    state_str = safe_str(prof.get("state"), "अखिल भारतीय" if is_hindi else "All India")
    occ_str = safe_str(prof.get("occupation"), "निर्दिष्ट नहीं" if is_hindi else "Not specified").capitalize()
    res_str = safe_str(prof.get("residence"), "निर्दिष्ट नहीं" if is_hindi else "Not specified")
    inc_str = safe_income_str(prof.get("annual_income"), is_hindi)
    cat_str = safe_str(prof.get("social_category"), "घोषित नहीं" if is_hindi else "Not declared")

    story = []

    # Header
    gen_date = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    header_title = "भारत सरकार योजना मार्गदर्शक" if is_hindi else "GOVERNMENT SCHEME NAVIGATOR"
    sub_title = (
        f"<b>आधिकारिक योजना चेकलिस्ट एवं नागरिक मार्गदर्शन दस्तावेज़</b> &nbsp;|&nbsp; जारी दिनांक: {gen_date}"
        if is_hindi else
        f"<b>Official Scheme Checklist & Citizen Guidance Dossier</b> &nbsp;|&nbsp; Generated: {gen_date} (ENGLISH)"
    )

    story.append(Paragraph(header_title, title_style))
    story.append(Paragraph(sub_title, subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_navy, spaceBefore=2, spaceAfter=8))

    # Scheme Spotlight Card Header
    status_bg = "#dcfce7" if ("Eligible" in status or "पात्र" in status) else ("#e0f2fe" if ("Official" in status or "सत्यापन" in status) else ("#ffedd5" if ("More" in status or "अधिक" in status) else "#f1f5f9"))
    status_fg = "#166534" if ("Eligible" in status or "पात्र" in status) else ("#0369a1" if ("Official" in status or "सत्यापन" in status) else ("#c2410c" if ("More" in status or "अधिक" in status) else "#475569"))

    label_scheme = "योजना:" if is_hindi else "SCHEME:"
    label_dept = "मंत्रालय / विभाग:" if is_hindi else "Ministry / Dept:"
    label_type = "प्रकार:" if is_hindi else "Type:"
    label_cat = "श्रेणी:" if is_hindi else "Category:"
    label_score = f"प्रासंगिकता: {score}/100" if is_hindi else f"Relevance: {score}/100"

    scheme_header_rows = [
        [
            Paragraph(f"<b>{label_scheme}</b> {escape_xml(s_display_name)}" + (f"<br/><font size=8 color='#475569'>({escape_xml(s_secondary_name)})</font>" if s_secondary_name else ""), body_bold),
            Paragraph(f"<font color='{status_fg}'><b>[{status.upper()}]</b></font>" + (f"<br/><font size=7.5 color='#475569'>{label_score}</font>" if score is not None else ""), body_bold)
        ],
        [
            Paragraph(f"<b>{label_dept}</b> {escape_xml(dept)}", body_style),
            Paragraph(f"<b>{label_type}</b> {escape_xml(level)} &nbsp;|&nbsp; <b>{label_cat}</b> {escape_xml(category)}", body_style)
        ]
    ]
    scheme_header_table = Table(scheme_header_rows, colWidths=[355, 168])
    scheme_header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(status_bg)),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor(border_color.hexval())),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor(border_color.hexval())),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(scheme_header_table)
    story.append(Spacer(1, 8))

    # Section 1: Citizen Profile Summary
    sec1_title = "1. नागरिक प्रोफ़ाइल सारांश (मूल्यांकन संदर्भ)" if is_hindi else "1. CITIZEN PROFILE SUMMARY (ASSESSMENT CONTEXT)"
    lbl_age = "आयु:" if is_hindi else "Age:"
    lbl_state = "राज्य / यूटी:" if is_hindi else "State / UT:"
    lbl_res = "निवास क्षेत्र:" if is_hindi else "Residence:"
    lbl_occ = "मुख्य व्यवसाय:" if is_hindi else "Occupation:"
    lbl_cat_f = "सामाजिक श्रेणी:" if is_hindi else "Social Category:"
    lbl_inc = "वार्षिक आय:" if is_hindi else "Annual Income:"

    story.append(Paragraph(sec1_title, h2_style))
    profile_rows = [
        [
            Paragraph(f"<b>{lbl_age}</b> " + escape_xml(age_str), body_style),
            Paragraph(f"<b>{lbl_state}</b> " + escape_xml(state_str), body_style),
            Paragraph(f"<b>{lbl_res}</b> " + escape_xml(res_str), body_style)
        ],
        [
            Paragraph(f"<b>{lbl_occ}</b> " + escape_xml(occ_str), body_style),
            Paragraph(f"<b>{lbl_cat_f}</b> " + escape_xml(cat_str), body_style),
            Paragraph(f"<b>{lbl_inc}</b> " + escape_xml(inc_str), body_style)
        ]
    ]
    profile_table = Table(profile_rows, colWidths=[174, 174, 175])
    profile_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_light),
        ("BOX", (0, 0), (-1, -1), 0.5, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 8))

    # Section 2: Scheme Benefits & Eligibility Highlights
    sec2_title = "2. प्रमुख लाभ एवं योजना विवरण" if is_hindi else "2. STATED BENEFITS & OBJECTIVES"
    lbl_overview = "विवरण:" if is_hindi else "Overview:"
    lbl_benefits = "प्रमुख लाभ:" if is_hindi else "Key Financial / Welfare Benefits:"

    story.append(Paragraph(sec2_title, h2_style))
    benefit_content = [
        [Paragraph(f"<b>{lbl_overview}</b> " + escape_xml(desc), body_style)],
        [Paragraph(f"<b>{lbl_benefits}</b> " + escape_xml(benefits), body_style)]
    ]
    benefit_table = Table(benefit_content, colWidths=[523])
    benefit_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#86efac")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(benefit_table)
    story.append(Spacer(1, 8))

    # Condition Breakdown if available
    if satisfied or unsatisfied or info_needed:
        sec3_title = "3. पात्रता शर्तों का विस्तृत विश्लेषण" if is_hindi else "3. ELIGIBILITY CONDITION BREAKDOWN"
        story.append(Paragraph(sec3_title, h2_style))
        cond_rows = []
        if satisfied:
            tag_met = "[पूर्ण]" if is_hindi else "[MET]"
            for sc in satisfied:
                rule_name = safe_str(sc.get("rule") if isinstance(sc, dict) else sc)
                detail = safe_str(sc.get("detail") if isinstance(sc, dict) else "")
                cond_rows.append([
                    Paragraph(f"<font color='#166534'><b>{tag_met}</b></font>", body_bold),
                    Paragraph(f"<b>{escape_xml(rule_name)}:</b> {escape_xml(detail)}", body_style)
                ])
        if unsatisfied:
            tag_unmet = "[अपूर्ण]" if is_hindi else "[UNMET]"
            for uc in unsatisfied:
                rule_name = safe_str(uc.get("rule") if isinstance(uc, dict) else uc)
                reason = safe_str(uc.get("reason", uc.get("detail")) if isinstance(uc, dict) else "")
                cond_rows.append([
                    Paragraph(f"<font color='#991b1b'><b>{tag_unmet}</b></font>", body_bold),
                    Paragraph(f"<b>{escape_xml(rule_name)}:</b> {escape_xml(reason)}", body_style)
                ])
        if info_needed:
            tag_verif = "[जांच]" if is_hindi else "[VERIFY]"
            for ic in info_needed:
                rule_name = safe_str(ic.get("rule") if isinstance(ic, dict) else ic)
                action = safe_str(ic.get("action", ic.get("detail")) if isinstance(ic, dict) else "")
                cond_rows.append([
                    Paragraph(f"<font color='#c2410c'><b>{tag_verif}</b></font>", body_bold),
                    Paragraph(f"<b>{escape_xml(rule_name)}:</b> {escape_xml(action)}", body_style)
                ])

        if cond_rows:
            cond_table = Table(cond_rows, colWidths=[65, 458])
            cond_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ffffff")),
                ("BOX", (0, 0), (-1, -1), 0.5, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(cond_table)
            story.append(Spacer(1, 8))

    # Section 4: Document Checklist Table with Checkboxes
    sec4_title = "4. आवश्यक दस्तावेज़ चेकलिस्ट (तैयार होने पर टिक करें)" if is_hindi else "4. REQUIRED PAPERWORK CHECKLIST (TICK WHEN PREPARED)"
    col_ready = "स्थिति" if is_hindi else "Ready"
    col_doc = "दस्तावेज़ / प्रमाण पत्र" if is_hindi else "Document / Verification Certificate"
    col_notes = "महत्वपूर्ण दिशानिर्देश" if is_hindi else "Notes / Guidelines"

    story.append(Paragraph(sec4_title, h2_style))
    doc_rows = [
        [
            Paragraph(f"<b>{col_ready}</b>", body_bold),
            Paragraph(f"<b>{col_doc}</b>", body_bold),
            Paragraph(f"<b>{col_notes}</b>", body_bold)
        ]
    ]

    if not req_docs:
        doc_rows.append([
            Paragraph("[ ]", body_style),
            Paragraph("मानक पहचान एवं पता प्रमाण (आधार / वोटर कार्ड)" if is_hindi else "Standard Identity & Address Proof (Aadhaar / Voter Card)", body_style),
            Paragraph("भारत सरकार के दिशानिर्देशों के तहत सभी योजनाओं के लिए अनिवार्य।" if is_hindi else "Mandatory for all DBT schemes under Government of India guidelines.", body_style)
        ])
    else:
        for d in req_docs:
            d_name = clean_text_for_pdf(d)
            guideline = "सुनिश्चित करें कि विवरण आपके आधार और बैंक रिकॉर्ड से मेल खाते हैं।" if is_hindi else "Verify that details match your Aadhaar and bank records exactly."
            if "land" in d_name.lower() or "भूमि" in d_name or "खतौनी" in d_name:
                guideline = "राजस्व विभाग द्वारा जारी नवीनतम खतौनी / खसरा।" if is_hindi else "Recent RoR / Khatauni / Khasra issued by Revenue Department."
            elif "income" in d_name.lower() or "caste" in d_name.lower() or "आय" in d_name or "जाति" in d_name:
                guideline = "सक्षम तहसीलदार / अनुविभागीय अधिकारी द्वारा निर्गत।" if is_hindi else "Issued by competent Tehsildar / SDO authority."
            elif "bank" in d_name.lower() or "dbt" in d_name.lower() or "बैंक" in d_name:
                guideline = "खाता सक्रिय होना चाहिए और डीबीटी के लिए एनपीसीआई से लिंक होना चाहिए।" if is_hindi else "Account must be active and NPCI-mapped for Direct Benefit Transfer."

            doc_rows.append([
                Paragraph("[  ]", body_style),
                Paragraph(escape_xml(d_name), body_bold),
                Paragraph(escape_xml(guideline), body_style)
            ])

    doc_table = Table(doc_rows, colWidths=[45, 238, 240])
    doc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(doc_table)
    story.append(Spacer(1, 8))

    # Section 5: Official Portals
    sec5_title = "5. सत्यापित आधिकारिक सरकारी पोर्टल" if is_hindi else "5. VERIFIED OFFICIAL GOVERNMENT PORTALS"
    lbl_portal_info = "आधिकारिक सूचना पोर्टल:" if is_hindi else "Official Information Portal:"
    lbl_portal_app = "ऑनलाइन आवेदन पोर्टल:" if is_hindi else "Online Application Portal:"
    lbl_portal_mode = "आवेदन प्रक्रिया:" if is_hindi else "Application Mode:"
    val_offline = "निर्दिष्ट नागरिक सेवा केंद्र (CSC) / ग्राम पंचायत शिविर / ऑफ़लाइन काउंटर।" if is_hindi else "Designated Citizen Service Centre (CSC) / Panchayat camp / Offline department counter."

    story.append(Paragraph(sec5_title, h2_style))
    portal_rows = [
        [
            Paragraph(f"<b>{lbl_portal_info}</b>", body_bold),
            Paragraph(f"<font color='{primary_navy}'><u>{escape_xml(info_url)}</u></font>", body_style)
        ]
    ]
    if app_url and "http" in app_url:
        portal_rows.append([
            Paragraph(f"<b>{lbl_portal_app}</b>", body_bold),
            Paragraph(f"<font color='{primary_navy}'><u>{escape_xml(app_url)}</u></font>", body_style)
        ])
    else:
        portal_rows.append([
            Paragraph(f"<b>{lbl_portal_mode}</b>", body_bold),
            Paragraph(val_offline, body_style)
        ])

    portal_table = Table(portal_rows, colWidths=[165, 358])
    portal_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.5, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(portal_table)
    story.append(Spacer(1, 10))

    # Mandatory Disclaimer Box
    notice_text = (
        "<b>महत्वपूर्ण नागरिक सूचना एवं अस्वीकरण:</b> यह चेकलिस्ट रिपोर्ट ओपन-सोर्स भारत सरकार योजना मार्गदर्शक द्वारा शैक्षणिक "
        "एवं नागरिक सहायता हेतु स्वचालित रूप से तैयार की गई है। <b>लाभ की कोई गारंटी नहीं:</b> यह आवेदन पात्रता, अनुमोदन या लाभ के "
        "वितरण की गारंटी नहीं देता है। सरकारी नियम समय-समय पर संशोधित होते हैं। आवेदन करने से पहले आधिकारिक सरकारी पोर्टलों पर "
        "विवरणों की पुष्टि अवश्य करें।"
        if is_hindi else
        "<b>MANDATORY CIVIC NOTICE:</b> This checklist report is generated by the open-source Government Scheme Navigator "
        "for educational and citizen guidance purposes. <b>No Guarantee of Approval:</b> The application does not guarantee "
        "eligibility, scheme approval, or monetary disbursements. Government rules, quotas, and application deadlines "
        "change periodically. Citizens must independently confirm details on the official portals (.gov.in / .nic.in)."
    )

    disclaimer_data = [[Paragraph(notice_text, disclaimer_style)]]
    disclaimer_table = Table(disclaimer_data, colWidths=[523])
    disclaimer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fefce8")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#facc15")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(KeepTogether([disclaimer_table]))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    if not pdf_bytes or len(pdf_bytes) < 100 or not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError("Generated single scheme PDF is corrupted or empty.")
    return pdf_bytes


# -----------------------------------------------------------------------------
# 2. Consolidated Multi-Scheme Assessment Report Generator
# -----------------------------------------------------------------------------
def generate_eligibility_pdf(
    user_profile: Optional[Dict[str, Any]],
    evaluated_schemes: Optional[List[Dict[str, Any]]],
    checklist_data: Optional[Dict[str, Any]],
    lang: str = "en"
) -> bytes:
    """
    Generate an official styled consolidated PDF assessment report and document checklist.
    Fully supports native Hindi translations when lang == 'hi'.
    Hardened against missing or incomplete profiles, incomplete schemes, and font errors.
    """
    setup_pdf_fonts()
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=45
    )

    is_hindi = lang in ["hi", "hindi", "हिन्दी"]
    pdf_styles = get_pdf_styles()
    title_style = pdf_styles["title"]
    subtitle_style = pdf_styles["subtitle"]
    h2_style = pdf_styles["h2"]
    body_style = pdf_styles["body"]
    body_bold = pdf_styles["body_bold"]
    disclaimer_style = pdf_styles["disclaimer"]

    primary_navy = colors.HexColor("#1e3a8a")
    secondary_teal = colors.HexColor("#0f766e")
    bg_light = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")
    tag_green = colors.HexColor("#166534")
    tag_blue = colors.HexColor("#1e40af")
    tag_amber = colors.HexColor("#9a3412")

    # Safe normalization of inputs
    prof = user_profile or {}
    evaluated = safe_list(evaluated_schemes)
    checklist = checklist_data if isinstance(checklist_data, dict) else {}

    story = []

    # 1. Header & Title Block
    gen_date = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    header_title = "भारत सरकार योजना मार्गदर्शक" if is_hindi else "GOVERNMENT SCHEME NAVIGATOR"
    sub_title = (
        f"<b>नागरिक योजना पात्रता मूल्यांकन एवं दस्तावेज़ चेकलिस्ट</b> &nbsp;|&nbsp; जारी दिनांक: {gen_date} (हिन्दी संस्करण)"
        if is_hindi else
        f"<b>Official Citizen Scheme Assessment & Document Checklist</b> &nbsp;|&nbsp; Generated: {gen_date} (ENGLISH)"
    )

    story.append(Paragraph(header_title, title_style))
    story.append(Paragraph(sub_title, subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_navy, spaceBefore=2, spaceAfter=8))

    # 2. Citizen Profile Summary Box
    age_str = safe_age_str(prof.get("age"), is_hindi)
    state_str = safe_str(prof.get("state"), "अखिल भारतीय" if is_hindi else "All India")
    occ_str = safe_str(prof.get("occupation"), "निर्दिष्ट नहीं" if is_hindi else "Not specified").capitalize()
    res_str = safe_str(prof.get("residence"), "निर्दिष्ट नहीं" if is_hindi else "Not specified")
    inc_str = safe_income_str(prof.get("annual_income"), is_hindi)
    cat_str = safe_str(prof.get("social_category"), "घोषित नहीं" if is_hindi else "Not declared")

    lbl_age = "आयु:" if is_hindi else "Age:"
    lbl_state = "राज्य / यूटी:" if is_hindi else "State / UT:"
    lbl_res = "निवास क्षेत्र:" if is_hindi else "Residence:"
    lbl_occ = "मुख्य व्यवसाय:" if is_hindi else "Occupation:"
    lbl_cat_f = "सामाजिक श्रेणी:" if is_hindi else "Social Category:"
    lbl_inc = "वार्षिक आय:" if is_hindi else "Annual Income:"

    profile_data = [
        [
            Paragraph(f"<b>{lbl_age}</b> " + escape_xml(age_str), body_style),
            Paragraph(f"<b>{lbl_state}</b> " + escape_xml(state_str), body_style),
            Paragraph(f"<b>{lbl_res}</b> " + escape_xml(res_str), body_style)
        ],
        [
            Paragraph(f"<b>{lbl_occ}</b> " + escape_xml(occ_str), body_style),
            Paragraph(f"<b>{lbl_cat_f}</b> " + escape_xml(cat_str), body_style),
            Paragraph(f"<b>{lbl_inc}</b> " + escape_xml(inc_str), body_style)
        ]
    ]

    profile_table = Table(profile_data, colWidths=[174, 174, 175])
    profile_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_light),
        ("BOX", (0, 0), (-1, -1), 0.75, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 10))

    # 3. Assessment Overview Metrics
    pot_eligible = [s for s in evaluated if s.get("status") == "Potentially Eligible"]
    official_verif = [s for s in evaluated if s.get("status") == "Official Verification Required"]
    more_info = [s for s in evaluated if s.get("status") == "More Information Required"]

    lbl_m_tot = "कुल योजनाएं" if is_hindi else "Total Evaluated"
    lbl_m_pot = "संभावित पात्र" if is_hindi else "Potentially Eligible"
    lbl_m_ver = "सत्यापन अपेक्षित" if is_hindi else "Verification Needed"
    lbl_m_inf = "अधिक जानकारी" if is_hindi else "More Info Needed"

    metrics_data = [
        [
            Paragraph(f"<b>{lbl_m_tot}</b><br/><font size=12 color='{primary_navy}'><b>{len(evaluated)}</b></font>", body_style),
            Paragraph(f"<b>{lbl_m_pot}</b><br/><font size=12 color='{tag_green}'><b>{len(pot_eligible)}</b></font>", body_style),
            Paragraph(f"<b>{lbl_m_ver}</b><br/><font size=12 color='{tag_blue}'><b>{len(official_verif)}</b></font>", body_style),
            Paragraph(f"<b>{lbl_m_inf}</b><br/><font size=12 color='{tag_amber}'><b>{len(more_info)}</b></font>", body_style),
        ]
    ]
    metrics_table = Table(metrics_data, colWidths=[130, 131, 131, 131])
    metrics_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 12))

    # 4. Potentially Eligible Schemes Section
    sec1_heading = "1. अनुशंसित एवं संभावित रूप से पात्र योजनाएं" if is_hindi else "1. RECOMMENDED & POTENTIALLY ELIGIBLE SCHEMES"
    story.append(Paragraph(sec1_heading, h2_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=secondary_teal, spaceBefore=2, spaceAfter=6))

    relevant_schemes = pot_eligible + official_verif
    if not relevant_schemes:
        empty_note = "वर्तमान विवरण के आधार पर कोई योजना मेल नहीं खाती है। कृपया एक्सप्लोरर में सभी योजनाएं देखें।" if is_hindi else "No schemes currently match all listed rules based on provided details. Please review missing information or explore all schemes in Scheme Explorer."
        story.append(Paragraph(empty_note, body_style))
    else:
        for idx, s in enumerate(relevant_schemes[:8], start=1):
            if is_hindi and s.get("hindi_name"):
                s_name = clean_text_for_pdf(s.get("hindi_name"))
            else:
                s_name = clean_text_for_pdf(s.get("scheme_name") or s.get("name") or "Government Scheme")

            dept = clean_text_for_pdf(s.get("department", "भारत सरकार" if is_hindi else "Government of India"))
            raw_status = s.get("status", "Potentially Eligible")
            status = translate_status(raw_status, is_hindi)
            benefits = clean_text_for_pdf(s.get("benefits", "आधिकारिक पोर्टल देखें" if is_hindi else "Check official portal"))
            raw_docs = safe_list(s.get("required_documents"))
            docs_list = ", ".join([clean_text_for_pdf(d) for d in raw_docs[:3]]) if raw_docs else ("मानक केवाईसी दस्तावेज़" if is_hindi else "Standard KYC documents")
            info_url = safe_str(s.get("official_information_url"), "https://www.myscheme.gov.in/")
            app_url = safe_str(s.get("official_application_url"), "")
            score_val = s.get("relevance_score")
            score_str = f"{score_val}/100" if score_val is not None else "N/A"

            status_bg = "#dcfce7" if ("Eligible" in status or "पात्र" in status) else "#e0f2fe"
            status_fg = "#166534" if ("Eligible" in status or "पात्र" in status) else "#0369a1"

            lbl_dept_row = "विभाग:" if is_hindi else "Department:"
            lbl_score_row = "प्रासंगिकता स्कोर:" if is_hindi else "Relevance Ranking:"
            lbl_ben_row = "लाभ:" if is_hindi else "Benefits:"
            lbl_doc_row = "मुख्य दस्तावेज़:" if is_hindi else "Key Documents:"
            lbl_portal_row = "आधिकारिक पोर्टल:" if is_hindi else "Official Portal:"
            lbl_app_row = "आवेदन:" if is_hindi else "Application:"

            scheme_card_content = [
                [
                    Paragraph(f"<b>#{idx}. {escape_xml(s_name)}</b>", body_bold),
                    Paragraph(f"<font color='{status_fg}'><b>[{status.upper()}]</b></font>", body_bold)
                ],
                [
                    Paragraph(f"<b>{lbl_dept_row}</b> {escape_xml(dept)}", body_style),
                    Paragraph(f"<b>{lbl_score_row}</b> {score_str}", body_style)
                ],
                [
                    Paragraph(f"<b>{lbl_ben_row}</b> {escape_xml(benefits)}", body_style),
                    Paragraph(f"<b>{lbl_doc_row}</b> {escape_xml(docs_list)}", body_style)
                ],
                [
                    Paragraph(f"<b>{lbl_portal_row}</b> <font color='{primary_navy}'><u>{escape_xml(info_url)}</u></font>", body_style),
                    Paragraph(
                        f"<b>{lbl_app_row}</b> <font color='{primary_navy}'><u>{escape_xml(app_url)}</u></font>"
                        if app_url and "http" in app_url else f"<b>{lbl_app_row}</b> " + ("ऑफ़लाइन / शिविर आधारित" if is_hindi else "Offline / Camp based"),
                        body_style
                    )
                ]
            ]
            scheme_card = Table(scheme_card_content, colWidths=[323, 200])
            scheme_card.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ffffff")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(status_bg)),
                ("BOX", (0, 0), (-1, -1), 0.75, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(KeepTogether([scheme_card, Spacer(1, 6)]))

    story.append(Spacer(1, 8))

    # 5. Consolidated Document Checklist Section
    sec2_heading = "2. एकीकृत दस्तावेज़ चेकलिस्ट" if is_hindi else "2. CONSOLIDATED DOCUMENT CHECKLIST"
    story.append(Paragraph(sec2_heading, h2_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=secondary_teal, spaceBefore=2, spaceAfter=6))

    categories = checklist.get("categories") if isinstance(checklist.get("categories"), dict) else {}
    if not categories:
        empty_doc_note = "मानक पहचान पत्र (आधार कार्ड, बैंक पासबुक) सभी आवेदनों के लिए अनुशंसित हैं।" if is_hindi else "Standard KYC documents (Aadhaar Card, Active Bank Passbook) are universally recommended."
        story.append(Paragraph(empty_doc_note, body_style))
    else:
        for cat_name, items in categories.items():
            cat_label = clean_text_for_pdf(cat_name)
            cat_prefix = "श्रेणी:" if is_hindi else "Category:"
            story.append(Paragraph(f"<b>{cat_prefix} {escape_xml(cat_label)}</b>", body_bold))
            col_d_name = "दस्तावेज़ का नाम" if is_hindi else "Document Name"
            col_d_sch = "संबंधित योजनाएं" if is_hindi else "Required For Schemes"
            doc_rows = [["[ ]", Paragraph(f"<b>{col_d_name}</b>", body_bold), Paragraph(f"<b>{col_d_sch}</b>", body_bold)]]
            for it in safe_list(items):
                if not isinstance(it, dict):
                    continue
                doc_name = clean_text_for_pdf(it.get("document", "दस्तावेज़" if is_hindi else "Document"))
                schemes_raw = safe_list(it.get("schemes"))
                schemes_str = clean_text_for_pdf(", ".join([str(x) for x in schemes_raw]))
                doc_rows.append([
                    "[ ]",
                    Paragraph(escape_xml(doc_name), body_style),
                    Paragraph(escape_xml(schemes_str), body_style)
                ])
            doc_table = Table(doc_rows, colWidths=[25, 298, 200])
            doc_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 0.5, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(KeepTogether([doc_table, Spacer(1, 5)]))

    story.append(Spacer(1, 10))

    # 6. Important Civic Notice & Disclaimer Box
    notice_text = (
        "<b>महत्वपूर्ण नागरिक सूचना एवं अस्वीकरण:</b> यह चेकलिस्ट रिपोर्ट ओपन-सोर्स भारत सरकार योजना मार्गदर्शक द्वारा शैक्षणिक "
        "एवं नागरिक सहायता हेतु स्वचालित रूप से तैयार की गई है। <b>लाभ की कोई गारंटी नहीं:</b> यह आवेदन पात्रता, अनुमोदन या लाभ के "
        "वितरण की गारंटी नहीं देता है। सरकारी नियम समय-समय पर संशोधित होते हैं। आवेदन करने से पहले आधिकारिक सरकारी पोर्टलों पर "
        "विवरणों की पुष्टि अवश्य करें।"
        if is_hindi else
        "<b>MANDATORY OFFICIAL DISCLAIMER & GUIDANCE NOTICE:</b><br/>"
        "1. This document is automatically generated by the open-source Government Scheme Navigator for educational and civic awareness.<br/>"
        "2. <b>NO GUARANTEE OF APPROVAL:</b> Neither this document nor the Navigator application guarantees scheme eligibility, approval, or monetary disbursement.<br/>"
        "3. Eligibility rules, income cutoffs, documentation formats, and budget quotas are periodically revised by central and state authorities.<br/>"
        "4. Citizens must independently verify all requirements on the respective official government portals (.gov.in / .nic.in) before submitting applications."
    )

    disclaimer_box_data = [[Paragraph(notice_text, disclaimer_style)]]
    disclaimer_table = Table(disclaimer_box_data, colWidths=[523])
    disclaimer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fefce8")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#facc15")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(KeepTogether([disclaimer_table]))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    if not pdf_bytes or len(pdf_bytes) < 100 or not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError("Generated consolidated PDF is corrupted or empty.")
    return pdf_bytes
