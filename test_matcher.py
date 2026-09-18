from utils.matcher import compare_skills


# Resume skills
resume_skills = [
    "Python",
    "Java",
    "AWS",
    "Linux",
    "PySpark"
]


# Job description skills
job_skills = [
    "Python",
    "AWS",
    "Linux",
    "Docker",
    "Kubernetes"
]


# Compare skills
matching, missing, percentage = compare_skills(
    resume_skills,
    job_skills
)


print("================================")
print("       SKILL COMPARISON")
print("================================")

print("\nMatching Skills:")

for skill in matching:
    print("-", skill)

print("\nMissing Skills:")

for skill in missing:
    print("-", skill)

print(f"\nSkill Match: {percentage:.2f}%")