import streamlit as st

from utils.pdf_extractor import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.matcher import compare_skills


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and a job description "
    "to compare technical skills."
)


# Upload files
resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_file = st.file_uploader(
    "Upload Job Description (PDF)",
    type=["pdf"]
)


# Analyze button
if st.button("Analyze Resume"):

    if resume_file is None or job_file is None:

        st.warning("Please upload both files.")

    else:

        with st.spinner("Analyzing documents..."):

            # Extract text
            resume_text = extract_text_from_pdf(resume_file)
            job_text = extract_text_from_pdf(job_file)

            # Extract skills
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_text)

            # Compare skills
            matching, missing, percentage = compare_skills(
                resume_skills,
                job_skills
            )

        st.success("Analysis completed!")

        st.subheader("📊 Skill Match Score")

        st.metric(
            "Match Percentage",
            f"{percentage:.2f}%"
        )

        st.subheader("✅ Matching Skills")

        if matching:
            st.write(", ".join(sorted(matching)))
        else:
            st.write("No matching skills found.")

        st.subheader("❌ Missing Skills")

        if missing:
            st.write(", ".join(sorted(missing)))
        else:
            st.write("No missing skills!")