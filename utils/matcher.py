def compare_skills(resume_skills, job_skills):
    """
    Compare resume skills with job description skills.
    """

    # Convert skills to lowercase for comparison
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    # Find matching skills
    matching_skills = resume_set.intersection(job_set)

    # Find missing skills
    missing_skills = job_set - resume_set

    # Calculate match percentage
    if len(job_set) > 0:
        match_percentage = (
            len(matching_skills) / len(job_set)
        ) * 100
    else:
        match_percentage = 0

    return matching_skills, missing_skills, match_percentage