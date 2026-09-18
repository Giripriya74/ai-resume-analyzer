from utils.skill_extractor import extract_skills


# Sample resume text
resume_text = """
I have experience in Python, Java, AWS, Linux,
PySpark, SQL, Docker and Generative AI.
"""


# Extract skills
skills = extract_skills(resume_text)


print("Detected Skills:")

for skill in skills:
    print("-", skill)