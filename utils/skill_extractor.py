import re


# List of technical skills
SKILLS = [
    "Python",
    "Java",
    "SQL",
    "MySQL",
    "HTML",
    "CSS",
    "AWS",
    "EC2",
    "Amazon EBS",
    "Linux",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Jenkins",
    "Terraform",
    "PySpark",
    "Apache Spark",
    "Pandas",
    "Matplotlib",
    "Data Engineering",
    "Data Analysis",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Generative AI",
    "Agentic AI",
    "LLMs",
    "RAG",
    "Semantic Search",
    "REST APIs",
    "SDLC",
    "DBMS",
    "Data Structures",
    "OOP",
    "Streamlit",
    "MCP"
]


def extract_skills(text):
    """
    Extract technical skills from text.
    """

    found_skills = []

    for skill in SKILLS:

        # Search for skills without case sensitivity
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills