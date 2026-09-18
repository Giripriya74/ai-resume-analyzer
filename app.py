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



resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Enter Job Description",
    height=500,
    placeholder="Paste the job description here..."
)




if st.button("Analyze Resume"):

    if resume_file is None or not job_description.strip():

        st.warning("Please upload both files.")

    else:

        with st.spinner("Analyzing documents..."):

            
            resume_text = extract_text_from_pdf(resume_file)
            job_text = job_description

           
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_text)

           
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
