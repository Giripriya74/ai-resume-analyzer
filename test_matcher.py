from utils.matcher import compare_skills



resume_skills = [
    "Python",
    "Java",
    "AWS",
    "Linux",
    "PySpark"
]



job_skills = [
    "Python",
    "AWS",
    "Linux",
    "Docker",
    "Kubernetes"
]



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
