import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

from utils.pdf_extractor import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.matcher import compare_skills


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, #24104f 0%, transparent 30%),
            radial-gradient(circle at 90% 20%, #102c55 0%, transparent 30%),
            linear-gradient(135deg, #050510, #0d0820 55%, #050510);
        color: #ffffff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #100b25, #05050d);
        border-right: 1px solid #5931a8;
    }

    /* Headings */
    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 900;
        color: #ffffff;
        text-shadow:
            0 0 8px #7c3aed,
            0 0 20px #2563eb;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #a5b4fc;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        color: #c4b5fd;
        font-size: 25px;
        font-weight: bold;
        margin: 20px 0 15px 0;
    }

    /* Cards */
    .glass-card {
        background: rgba(19, 13, 42, 0.92);
        border: 1px solid #4c1d95;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.35),
            0 0 18px rgba(124, 58, 237, 0.12);
        transition: 0.3s;
    }

    .glass-card:hover {
        border-color: #818cf8;
        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.45),
            0 0 25px rgba(99, 102, 241, 0.3);
    }

    .card-title {
        color: #c4b5fd;
        font-size: 19px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #17102f, #0b1024);
        border: 1px solid #4338ca;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        min-height: 140px;
        box-shadow: 0 0 18px rgba(99, 102, 241, 0.18);
    }

    .metric-label {
        color: #a5b4fc;
        font-size: 15px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 34px;
        font-weight: bold;
        margin-top: 10px;
        text-shadow: 0 0 12px #6366f1;
    }

    /* Skill tags */
    .skill {
        display: inline-block;
        padding: 8px 14px;
        margin: 5px;
        border-radius: 20px;
        color: white;
        background: linear-gradient(90deg, #2563eb, #9333ea);
        box-shadow: 0 0 10px rgba(96, 165, 250, 0.35);
        font-size: 14px;
    }

    /* Status box */
    .success-box {
        padding: 18px;
        border-radius: 15px;
        text-align: center;
        color: #d1fae5;
        background: rgba(6, 78, 59, 0.35);
        border: 1px solid #10b981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.25);
        font-size: 20px;
        font-weight: bold;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        border: 1px solid #818cf8;
        border-radius: 13px;
        padding: 14px;
        color: white;
        font-size: 17px;
        font-weight: bold;
        background: linear-gradient(90deg, #2563eb, #9333ea);
        box-shadow: 0 0 18px rgba(139, 92, 246, 0.45);
        transition: 0.3s;
    }

    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(96, 165, 250, 0.8);
    }

    /* Text */
    p, label {
        color: #e5e7eb !important;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def display_skill_tags(skills):
    """Display skills as colorful tags."""
    if skills:
        html = "".join(
            f'<span class="skill">{skill}</span>'
            for skill in sorted(skills)
        )
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No skills found.")


def create_circular_score(score):
    """Create a circular score meter using HTML and CSS."""

    score = max(0, min(100, float(score)))

    html = f"""
    <div style="
        background: rgba(12, 8, 30, 0.95);
        border: 1px solid #6366f1;
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 30px rgba(99,102,241,0.25);
    ">

        <div style="
            color: #c4b5fd;
            font-size: 24px;
            font-weight: bold;
        ">
            🎯 RESUME MATCH SCORE
        </div>

        <div style="
            width: 230px;
            height: 230px;
            border-radius: 50%;
            margin: 25px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            background: conic-gradient(
                #8b5cf6 {score}%,
                #242044 {score}% 100%
            );
            box-shadow: 0 0 35px rgba(139,92,246,0.6);
        ">

            <div style="
                width: 180px;
                height: 180px;
                border-radius: 50%;
                background: #090719;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            ">

                <div style="
                    font-size: 42px;
                    font-weight: bold;
                    color: #a78bfa;
                ">
                    {score:.1f}%
                </div>

                <div style="color: #c4b5fd;">
                    Match Score
                </div>

            </div>
        </div>
    </div>
    """

    components.html(html, height=370)


def create_report(
    resume_name,
    match_percentage,
    resume_skills,
    job_skills,
    matching,
    missing
):
    """Create a downloadable text report."""

    report = f"""
AI RESUME ANALYZER REPORT
=========================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Resume File:
{resume_name}

Resume Match Percentage:
{match_percentage:.2f}%

Total Resume Skills:
{len(resume_skills)}

Total Job Skills:
{len(job_skills)}

Matching Skills:
{len(matching)}

Missing Skills:
{len(missing)}

MATCHING SKILLS
---------------
{", ".join(sorted(matching)) if matching else "None"}

MISSING SKILLS
--------------
{", ".join(sorted(missing)) if missing else "None"}

SUMMARY
-------
Your resume matches {match_percentage:.2f}% of the
skills identified in the job description.

This report was generated by AI Resume Analyzer.
"""

    return report


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🤖 AI CONTROL PANEL")
    st.markdown("---")

    st.markdown("### Navigation")

    page = st.radio(
        "Select a page",
        [
            "🏠 Dashboard",
            "📄 Resume Analyzer",
            "📊 Analytics",
            "ℹ️ About Project"
        ]
    )

    st.markdown("---")

    st.markdown("### ⚡ System Status")
    st.success("AI Engine Ready")
    st.info("Resume Analyzer Online")

    st.markdown("---")
    st.caption("AI Resume Analyzer v1.0")


# =========================================================
# DASHBOARD PAGE
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🤖 AI RESUME ANALYZER</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Futuristic resume analysis and intelligent skill matching'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">
        <div class="card-title">🚀 Welcome to the AI Dashboard</div>
        <p>
        Analyze your resume against a job description and discover
        your matching and missing technical skills.
        </p>
        <p>
        Navigate to <b>Resume Analyzer</b> from the sidebar to begin.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">📄 Resume Analysis</div>
            <div class="metric-value">READY</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🧠 Skill Matching</div>
            <div class="metric-value">ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">⚡ AI Engine</div>
            <div class="metric-value">ONLINE</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🔒 System</div>
            <div class="metric-value">SECURE</div>
        </div>
        """, unsafe_allow_html=True)



# =========================================================
# RESUME ANALYZER PAGE
# =========================================================

if page == "📄 Resume Analyzer":

    st.markdown(
        '<div class="main-title">📄 RESUME ANALYZER</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Upload your resume and compare it with a job description</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Upload Resume")

        resume_file = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"],
            key="resume_uploader"
        )

    with col2:
        st.markdown("### 📋 Job Description")

        job_description = st.text_area(
            "Paste the job description",
            height=250,
            placeholder="Paste the job description here...",
            key="job_description_input"
        )

        st.caption(
            f"Characters entered: {len(job_description)}"
        )

    if st.button("🚀 Analyze Resume", key="analyze_button"):

        if resume_file is None or not job_description.strip():

            st.warning(
                "Please upload your resume and enter a job description."
            )

        else:

            try:

                with st.spinner(
                    "🧠 AI engine is analyzing your resume..."
                ):

                    # Extract resume text
                    resume_text = extract_text_from_pdf(resume_file)

                    # Extract skills
                    resume_skills = extract_skills(resume_text)
                    job_skills = extract_skills(job_description)

                    # Compare skills
                    matching, missing, percentage = compare_skills(
                        resume_skills,
                        job_skills
                    )

                    # Save results
                    st.session_state["analysis_done"] = True
                    st.session_state["resume_name"] = resume_file.name
                    st.session_state["resume_skills"] = resume_skills
                    st.session_state["job_skills"] = job_skills
                    st.session_state["matching"] = matching
                    st.session_state["missing"] = missing
                    st.session_state["percentage"] = percentage

                    st.success("✅ Analysis completed successfully!")

                    st.info(
                        "Open the 📊 Analytics page to view your results."
                    )

            except Exception as error:

                st.error(
                    f"An error occurred during analysis: {error}"
                )


# =========================================================
# ANALYTICS PAGE
# =========================================================

if page == "📊 Analytics":

    st.markdown(
        '<div class="main-title">📊 ANALYTICS DASHBOARD</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Detailed resume analysis results</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.get("analysis_done", False):

        st.info(
            "No analysis results available. "
            "Please analyze a resume first from the Resume Analyzer page."
        )

    else:

        # Get saved results
        resume_name = st.session_state["resume_name"]
        resume_skills = st.session_state["resume_skills"]
        job_skills = st.session_state["job_skills"]
        matching = st.session_state["matching"]
        missing = st.session_state["missing"]
        percentage = st.session_state["percentage"]

        st.markdown(
            '<div class="section-title">📊 Analysis Overview</div>',
            unsafe_allow_html=True
        )

        # Metric cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🎯 Match Percentage",
                f"{float(percentage):.1f}%"
            )

        with col2:
            st.metric(
                "✅ Matching Skills",
                len(matching)
            )

        with col3:
            st.metric(
                "❌ Missing Skills",
                len(missing)
            )

        with col4:
            st.metric(
                "🧠 Total Job Skills",
                len(job_skills)
            )

        st.markdown("---")

        # Score and summary
        score_col, summary_col = st.columns(2)

        with score_col:

            st.markdown(
                '<div class="section-title">🎯 Resume Match Score</div>',
                unsafe_allow_html=True
            )

            create_circular_score(percentage)

        with summary_col:

            st.markdown(
                '<div class="section-title">📝 Analysis Summary</div>',
                unsafe_allow_html=True
            )

            st.write(f"**Resume:** {resume_name}")
            st.write(f"**Resume skills detected:** {len(resume_skills)}")
            st.write(f"**Job skills detected:** {len(job_skills)}")
            st.write(f"**Matching skills:** {len(matching)}")
            st.write(f"**Missing skills:** {len(missing)}")

            st.progress(
                min(max(float(percentage) / 100, 0.0), 1.0)
            )

        st.markdown("---")

        # Matching skills
        st.markdown(
            '<div class="section-title">✅ Matching Skills</div>',
            unsafe_allow_html=True
        )

        display_skill_tags(matching)

        # Missing skills
        st.markdown(
            '<div class="section-title">❌ Missing Skills</div>',
            unsafe_allow_html=True
        )

        display_skill_tags(missing)

        st.markdown("---")

        # Comparison table
        st.markdown(
            '<div class="section-title">📋 Skill Comparison Table</div>',
            unsafe_allow_html=True
        )

        all_skills = sorted(
            set(resume_skills).union(set(job_skills))
        )

        table_data = []

        for skill in all_skills:

            in_resume = skill in resume_skills
            in_job = skill in job_skills

            if in_resume and in_job:
                status = "✅ Matching"

            elif in_job and not in_resume:
                status = "❌ Missing"

            else:
                status = "📄 Resume Only"

            table_data.append({
                "Skill": skill,
                "In Resume": "Yes" if in_resume else "No",
                "In Job Description": "Yes" if in_job else "No",
                "Status": status
            })

        if table_data:

            table_df = pd.DataFrame(table_data)

            st.dataframe(
                table_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No skills were detected.")

        # Download report
        st.markdown("---")

        report = create_report(
            resume_name,
            percentage,
            resume_skills,
            job_skills,
            matching,
            missing
        )

        st.download_button(
            label="📥 Download Analysis Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )


# =========================================================
# ABOUT PROJECT PAGE
# =========================================================

if page == "ℹ️ About Project":

    st.markdown(
        '<div class="main-title">ℹ️ ABOUT PROJECT</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">

    ### 🤖 AI Resume Analyzer

    This project analyzes a resume and compares its skills
    with the skills mentioned in a job description.

    ### 🚀 Main Features

    - Upload a resume in PDF format
    - Extract resume text
    - Detect technical skills
    - Compare resume skills with job requirements
    - Display matching skills
    - Display missing skills
    - Calculate resume match percentage
    - Download an analysis report

   

    - Python
    - Streamlit
    - Pandas
    - PDF Text Extraction
    - Git and GitHub

    </div>
    """, unsafe_allow_html=True)