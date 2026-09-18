import re

SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "SQL",
    "MySQL",
    "HTML",
    "CSS",
    "AWS",
    "Amazon Web Services",
    "EC2",
    "S3",
    "VPC",
    "EBS",
    "Linux",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Jenkins",
    "Terraform",
    "Ansible",
    "CI/CD",
    "DevOps",
    "PySpark",
    "Apache Spark",
    "Pandas",
    "Matplotlib",
    "Machine Learning",
    "Artificial Intelligence",
    "Generative AI",
    "LLMs",
    "RAG",
    "REST APIs",
    "Streamlit",
    "Networking",
    "Troubleshooting",
    "Technical Support",
    "Cloud Computing",
    "Data Analysis",
    "Data Engineering",
    "DBMS",
    "OOP",
    "SDLC"
]


def extract_skills(text):
    """
    Extract skills from the given text.
    """

    if not text:
        return []

    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills