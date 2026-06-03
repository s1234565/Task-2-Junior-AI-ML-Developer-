import os
import re
from datetime import date, datetime

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

_EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

CSS = """
<style>
[data-testid="stAppViewContainer"] { background: #0f1117; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1f2e 0%, #141824 100%);
    border-right: 1px solid #2d3748;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
.sidebar-brand { text-align: center; padding: 1.5rem 1rem 1rem; border-bottom: 1px solid #2d3748; margin-bottom: 1rem; }
.sidebar-brand h2 { color: #63b3ed !important; font-size: 1.1rem; font-weight: 700; margin: 0.4rem 0 0.2rem; }
.sidebar-brand p { color: #718096 !important; font-size: 0.75rem; margin: 0; }
.page-header { background: linear-gradient(135deg, #1a365d 0%, #2a4a7f 100%); border-radius: 12px; padding: 1.5rem 2rem; margin-bottom: 1.5rem; border-left: 4px solid #63b3ed; }
.page-header h1 { color: #ebf8ff !important; font-size: 1.6rem; font-weight: 700; margin: 0 0 0.25rem; }
.page-header p { color: #90cdf4 !important; font-size: 0.9rem; margin: 0; }
.metric-card { background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); border: 1px solid #4a5568; border-radius: 12px; padding: 1.25rem 1.5rem; text-align: center; }
.metric-card .metric-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.metric-card .metric-value { font-size: 2.2rem; font-weight: 800; color: #63b3ed; line-height: 1; }
.metric-card .metric-label { font-size: 0.8rem; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; }
.section-card { background: #1a202c; border: 1px solid #2d3748; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }
.section-title { color: #90cdf4; font-size: 1rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #2d3748; }
.prediction-box { background: linear-gradient(135deg, #1a365d 0%, #1e3a5f 100%); border: 1px solid #2b6cb0; border-left: 4px solid #63b3ed; border-radius: 10px; padding: 1.25rem 1.5rem; margin: 1rem 0; }
.prediction-box .pred-header { color: #90cdf4; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }
.prediction-box .pred-text { color: #e2e8f0; font-size: 0.95rem; line-height: 1.6; }
.patient-card { background: #1a202c; border: 1px solid #2d3748; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 1rem; }
.patient-avatar { background: linear-gradient(135deg, #2b6cb0, #3182ce); border-radius: 50%; width: 42px; height: 42px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }
.patient-info .patient-name { color: #e2e8f0; font-weight: 600; font-size: 0.95rem; }
.patient-info .patient-meta { color: #718096; font-size: 0.8rem; margin-top: 0.15rem; }
.patient-info .patient-pred { color: #90cdf4; font-size: 0.82rem; margin-top: 0.4rem; font-style: italic; }
[data-testid="stForm"] { background: #1a202c; border: 1px solid #2d3748; border-radius: 12px; padding: 1.5rem; }
.stTextInput > label, .stNumberInput > label, .stDateInput > label { color: #a0aec0 !important; font-size: 0.85rem !important; font-weight: 500 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
.stTextInput input, .stNumberInput input { background: #2d3748 !important; border: 1px solid #4a5568 !important; border-radius: 8px !important; color: #e2e8f0 !important; }
.stButton > button { background: linear-gradient(135deg, #2b6cb0, #3182ce) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; padding: 0.5rem 1.5rem !important; }
[data-testid="stFormSubmitButton"] > button { background: linear-gradient(135deg, #276749, #38a169) !important; width: 100% !important; padding: 0.65rem !important; font-size: 1rem !important; }
[data-testid="stDataFrame"] { border: 1px solid #2d3748 !important; border-radius: 10px !important; overflow: hidden !important; }
hr { border-color: #2d3748 !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
"""


def validate_patient_input(full_name, email, date_of_birth, glucose, haemoglobin, cholesterol):
    errors = []
    if not full_name.strip():
        errors.append("Name cannot be empty.")
    if not _EMAIL_RE.match(email):
        errors.append("Email must be valid.")
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        if dob > date.today():
            errors.append("Date of birth cannot be a future date.")
    except (ValueError, TypeError):
        pass
    try:
        float(glucose)
    except (ValueError, TypeError):
        errors.append("Glucose must be a numeric value.")
    try:
        float(haemoglobin)
    except (ValueError, TypeError):
        errors.append("Haemoglobin must be a numeric value.")
    try:
        float(cholesterol)
    except (ValueError, TypeError):
        errors.append("Cholesterol must be a numeric value.")
    return errors


def _css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


def _header(title, subtitle):
    import streamlit as st
    st.markdown(f'<div class="page-header"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def render_dashboard():
    import streamlit as st
    import database

    _css()
    _header("📊 Dashboard", "Overview of patient records and recent AI predictions")

    count = database.get_patient_count()
    recent = database.get_recent_patients(limit=5)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-icon">👥</div><div class="metric-value">{count}</div><div class="metric-label">Total Patients</div></div>', unsafe_allow_html=True)
    with c2:
        with_pred = sum(1 for p in recent if p.get("remarks") and "could not" not in p.get("remarks", ""))
        st.markdown(f'<div class="metric-card"><div class="metric-icon">🤖</div><div class="metric-value">{with_pred}</div><div class="metric-label">Recent Predictions</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-icon">📅</div><div class="metric-value">{date.today().strftime("%b %d")}</div><div class="metric-label">Today\'s Date</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown('<div class="section-title">🕐 Recent Patients</div>', unsafe_allow_html=True)
        if not recent:
            st.info("No patients added yet.")
        else:
            for p in recent:
                initials = "".join(w[0].upper() for w in p["full_name"].split()[:2])
                pred_snippet = ""
                if p.get("remarks") and "could not" not in p.get("remarks", ""):
                    snippet = p["remarks"][:80] + ("..." if len(p["remarks"]) > 80 else "")
                    pred_snippet = f'<div class="patient-pred">💡 {snippet}</div>'
                st.markdown(
                    f'<div class="patient-card"><div class="patient-avatar">{initials}</div>'
                    f'<div class="patient-info"><div class="patient-name">{p["full_name"]}</div>'
                    f'<div class="patient-meta">📧 {p["email"]} &nbsp;|&nbsp; 🎂 {p["date_of_birth"]}</div>'
                    f'{pred_snippet}</div></div>',
                    unsafe_allow_html=True,
                )

    with col_right:
        st.markdown('<div class="section-title">🩸 Latest Blood Values</div>', unsafe_allow_html=True)
        if not recent:
            st.info("No data yet.")
        else:
            p = recent[0]
            st.markdown(
                f'<div class="section-card">'
                f'<div style="color:#e2e8f0;font-weight:600;margin-bottom:0.75rem">{p["full_name"]}</div>'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:0.5rem"><span style="color:#a0aec0">🩸 Glucose</span><span style="color:#fc8181;font-weight:600">{p["glucose"]} mg/dL</span></div>'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:0.5rem"><span style="color:#a0aec0">💉 Haemoglobin</span><span style="color:#68d391;font-weight:600">{p["haemoglobin"]} g/dL</span></div>'
                f'<div style="display:flex;justify-content:space-between"><span style="color:#a0aec0">🫀 Cholesterol</span><span style="color:#f6ad55;font-weight:600">{p["cholesterol"]} mg/dL</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if p.get("remarks") and "could not" not in p.get("remarks", ""):
                st.markdown(f'<div class="prediction-box"><div class="pred-header">🤖 AI Prediction</div><div class="pred-text">{p["remarks"]}</div></div>', unsafe_allow_html=True)


def render_add_patient():
    import streamlit as st
    import database
    import ai_service

    _css()
    _header("➕ Add Patient", "Register a new patient and generate an AI health prediction")

    col_form, col_info = st.columns([1.4, 1])

    with col_form:
        with st.form("add_patient_form", clear_on_submit=True):
            st.markdown('<div class="section-title">👤 Patient Information</div>', unsafe_allow_html=True)
            name = st.text_input("Full Name", placeholder="e.g. John Smith")
            email = st.text_input("Email Address", placeholder="e.g. john@example.com")
            dob = st.date_input("Date of Birth", value=date(1990, 1, 1), min_value=date(1900, 1, 1), max_value=date.today())
            st.markdown('<div class="section-title" style="margin-top:1rem">🩸 Blood Test Values</div>', unsafe_allow_html=True)
            g_col, h_col, c_col = st.columns(3)
            with g_col:
                glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=1000.0, step=0.1, value=90.0)
            with h_col:
                haemoglobin = st.number_input("Haemoglobin (g/dL)", min_value=0.0, max_value=25.0, step=0.1, value=13.5)
            with c_col:
                cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, max_value=1000.0, step=0.1, value=180.0)
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🤖 Add Patient & Generate Prediction", use_container_width=True)

        if submitted:
            errors = validate_patient_input(name, email, str(dob), str(glucose), str(haemoglobin), str(cholesterol))
            if errors:
                for e in errors:
                    st.error(f"⚠️ {e}")
            else:
                with st.spinner("Saving patient and generating AI prediction..."):
                    patient_id = database.create_patient(
                        full_name=name, date_of_birth=str(dob), email=email,
                        glucose=glucose, haemoglobin=haemoglobin, cholesterol=cholesterol,
                    )
                    prediction = ai_service.get_health_prediction(glucose, haemoglobin, cholesterol)
                    database.update_patient_remarks(patient_id, prediction)
                st.success(f"✅ Patient **{name}** added successfully! (ID: {patient_id})")
                st.markdown(f'<div class="prediction-box"><div class="pred-header">🤖 AI Health Prediction</div><div class="pred-text">{prediction}</div></div>', unsafe_allow_html=True)

    with col_info:
        st.markdown(
            '<div class="section-card"><div class="section-title">📋 Reference Ranges</div>'
            '<div style="margin-bottom:0.75rem"><div style="color:#a0aec0;font-size:0.8rem;margin-bottom:0.25rem">🩸 GLUCOSE (mg/dL)</div>'
            '<div style="color:#68d391;font-size:0.85rem">Normal: 70 – 99</div>'
            '<div style="color:#f6ad55;font-size:0.85rem">Pre-diabetic: 100 – 125</div>'
            '<div style="color:#fc8181;font-size:0.85rem">Diabetic: ≥ 126</div></div>'
            '<div style="margin-bottom:0.75rem"><div style="color:#a0aec0;font-size:0.8rem;margin-bottom:0.25rem">💉 HAEMOGLOBIN (g/dL)</div>'
            '<div style="color:#68d391;font-size:0.85rem">Men: 13.5 – 17.5</div>'
            '<div style="color:#68d391;font-size:0.85rem">Women: 12.0 – 15.5</div></div>'
            '<div><div style="color:#a0aec0;font-size:0.8rem;margin-bottom:0.25rem">🫀 CHOLESTEROL (mg/dL)</div>'
            '<div style="color:#68d391;font-size:0.85rem">Desirable: &lt; 200</div>'
            '<div style="color:#f6ad55;font-size:0.85rem">Borderline: 200 – 239</div>'
            '<div style="color:#fc8181;font-size:0.85rem">High: ≥ 240</div></div></div>',
            unsafe_allow_html=True,
        )


def render_patient_records():
    import streamlit as st
    import database
    import ai_service

    _css()
    _header("📋 Patient Records", "Search, view, edit and delete patient records")

    search_term = st.text_input("🔍 Search by Name or Email", "", placeholder="Type a name or email...")
    patients = database.search_patients(search_term)

    if not patients:
        st.info("No patients found.")
    else:
        st.markdown(f'<div style="color:#718096;font-size:0.85rem;margin-bottom:0.5rem">{len(patients)} record(s) found</div>', unsafe_allow_html=True)
        import pandas as pd
        df = pd.DataFrame(patients)
        cols = ["id", "full_name", "email", "date_of_birth", "glucose", "haemoglobin", "cholesterol", "created_at"]
        df_display = df[[c for c in cols if c in df.columns]]
        df_display.columns = [c.replace("_", " ").title() for c in df_display.columns]
        st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab_edit, tab_delete, tab_detail = st.tabs(["✏️  Edit Patient", "🗑️  Delete Patient", "🔍  View Details"])

    with tab_edit:
        st.markdown('<div class="section-title">Edit Patient Record</div>', unsafe_allow_html=True)
        patient_id_edit = st.number_input("Patient ID", min_value=1, step=1, key="edit_id")
        if st.button("📂 Load Patient", key="load_btn"):
            loaded = database.get_patient_by_id(int(patient_id_edit))
            if loaded:
                st.session_state["edit_patient"] = loaded
                st.success(f"Loaded: **{loaded['full_name']}**")
            else:
                st.error(f"No patient found with ID {int(patient_id_edit)}.")
                st.session_state.pop("edit_patient", None)

        if "edit_patient" in st.session_state:
            p = st.session_state["edit_patient"]
            with st.form("edit_patient_form"):
                e_name = st.text_input("Full Name", value=p["full_name"])
                e_email = st.text_input("Email", value=p["email"])
                try:
                    e_dob_default = datetime.strptime(str(p["date_of_birth"])[:10], "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    e_dob_default = date(1990, 1, 1)
                e_dob = st.date_input("Date of Birth", value=e_dob_default, min_value=date(1900, 1, 1), max_value=date.today(), key="edit_dob")
                g2, h2, c2 = st.columns(3)
                with g2:
                    e_glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, step=0.1, value=float(p["glucose"]))
                with h2:
                    e_haemo = st.number_input("Haemoglobin (g/dL)", min_value=0.0, step=0.1, value=float(p["haemoglobin"]))
                with c2:
                    e_chol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, step=0.1, value=float(p["cholesterol"]))
                save = st.form_submit_button("💾 Save Changes & Regenerate Prediction", use_container_width=True)

            if save:
                errors = validate_patient_input(e_name, e_email, str(e_dob), str(e_glucose), str(e_haemo), str(e_chol))
                if errors:
                    for e in errors:
                        st.error(f"⚠️ {e}")
                else:
                    with st.spinner("Updating record and regenerating prediction..."):
                        database.update_patient(p["id"], e_name, str(e_dob), e_email, e_glucose, e_haemo, e_chol)
                        prediction = ai_service.get_health_prediction(e_glucose, e_haemo, e_chol)
                        database.update_patient_remarks(p["id"], prediction)
                    st.success("✅ Patient updated successfully!")
                    st.markdown(f'<div class="prediction-box"><div class="pred-header">🤖 Updated Prediction</div><div class="pred-text">{prediction}</div></div>', unsafe_allow_html=True)
                    st.session_state.pop("edit_patient", None)

    with tab_delete:
        st.markdown('<div class="section-title">Delete Patient Record</div>', unsafe_allow_html=True)
        del_id = st.number_input("Patient ID to Delete", min_value=1, step=1, key="delete_id")
        patient_to_del = database.get_patient_by_id(int(del_id))
        if patient_to_del:
            initials = "".join(w[0].upper() for w in patient_to_del["full_name"].split()[:2])
            st.markdown(
                f'<div class="patient-card"><div class="patient-avatar">{initials}</div>'
                f'<div class="patient-info"><div class="patient-name">{patient_to_del["full_name"]}</div>'
                f'<div class="patient-meta">📧 {patient_to_del["email"]} &nbsp;|&nbsp; 🎂 {patient_to_del["date_of_birth"]}</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        st.warning(f"⚠️ This will permanently delete patient ID **{int(del_id)}**.")
        confirmed = st.checkbox("I understand and confirm the deletion")
        if st.button("🗑️ Delete Patient", key="del_btn"):
            if confirmed:
                database.delete_patient(int(del_id))
                st.success("✅ Patient deleted successfully.")
            else:
                st.error("Please check the confirmation box first.")

    with tab_detail:
        st.markdown('<div class="section-title">View Patient Details</div>', unsafe_allow_html=True)
        view_id = st.number_input("Patient ID", min_value=1, step=1, key="view_id")
        if st.button("🔍 View Patient", key="view_btn"):
            p = database.get_patient_by_id(int(view_id))
            if not p:
                st.error(f"No patient found with ID {int(view_id)}.")
            else:
                initials = "".join(w[0].upper() for w in p["full_name"].split()[:2])
                st.markdown(
                    f'<div class="section-card">'
                    f'<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">'
                    f'<div class="patient-avatar" style="width:56px;height:56px;font-size:1.4rem">{initials}</div>'
                    f'<div><div style="color:#e2e8f0;font-size:1.2rem;font-weight:700">{p["full_name"]}</div>'
                    f'<div style="color:#718096;font-size:0.85rem">ID: {p["id"]} &nbsp;|&nbsp; Added: {str(p["created_at"])[:10]}</div></div></div>'
                    f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin-bottom:1rem">'
                    f'<div><div style="color:#a0aec0;font-size:0.75rem;text-transform:uppercase">Email</div><div style="color:#e2e8f0">{p["email"]}</div></div>'
                    f'<div><div style="color:#a0aec0;font-size:0.75rem;text-transform:uppercase">Date of Birth</div><div style="color:#e2e8f0">{p["date_of_birth"]}</div></div>'
                    f'<div><div style="color:#a0aec0;font-size:0.75rem;text-transform:uppercase">Glucose</div><div style="color:#fc8181;font-weight:600">{p["glucose"]} mg/dL</div></div>'
                    f'<div><div style="color:#a0aec0;font-size:0.75rem;text-transform:uppercase">Haemoglobin</div><div style="color:#68d391;font-weight:600">{p["haemoglobin"]} g/dL</div></div>'
                    f'<div><div style="color:#a0aec0;font-size:0.75rem;text-transform:uppercase">Cholesterol</div><div style="color:#f6ad55;font-weight:600">{p["cholesterol"]} mg/dL</div></div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
                if p.get("remarks"):
                    st.markdown(f'<div class="prediction-box"><div class="pred-header">🤖 AI Health Prediction</div><div class="pred-text">{p["remarks"]}</div></div>', unsafe_allow_html=True)


def main():
    import streamlit as st
    import database

    st.set_page_config(page_title="Health Prediction App", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")
    database.init_db()

    st.sidebar.markdown(CSS, unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="sidebar-brand"><div style="font-size:2.5rem">🏥</div><h2>HealthPredict AI</h2><p>Powered by Google Gemini</p></div>',
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio("Navigation", ["📊 Dashboard", "➕ Add Patient", "📋 Patient Records"], label_visibility="collapsed")

    count = database.get_patient_count()
    st.sidebar.markdown("<br>" * 3, unsafe_allow_html=True)
    st.sidebar.markdown(
        f'<div style="text-align:center;padding:1rem;border-top:1px solid #2d3748;color:#718096;font-size:0.78rem">'
        f'<div style="color:#63b3ed;font-size:1.1rem;font-weight:700">{count}</div><div>Total Patients</div></div>',
        unsafe_allow_html=True,
    )

    if page == "📊 Dashboard":
        render_dashboard()
    elif page == "➕ Add Patient":
        render_add_patient()
    elif page == "📋 Patient Records":
        render_patient_records()


if __name__ == "__main__":
    main()

