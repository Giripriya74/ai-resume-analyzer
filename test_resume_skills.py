from utils.pdf_extractor import extract_text_from_pdf
from utils.skill_extractor import extract_skills



with open("sample_resume.pdf", "rb") as file:

   
    resume_text = extract_text_from_pdf(file)



skills = extract_skills(resume_text)


print("\nDetected Skills in Your Resume:\n")

for skill in skills:
    print("-", skill)