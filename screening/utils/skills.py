import re


# Skills recognized by the resume screening system
SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "html",
    "css",
    "django",
    "flask",
    "sql",
    "mysql",
    "mongodb",
    "rest api",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "natural language processing",
    "data structures",
    "algorithms",
    "aws",
    "object oriented programming",
    "oop",
    "dbms",
    "cloud computing",
    "problem solving",
]


# Convert different names into one standard name
SKILL_ALIASES = {
    "nlp": "natural language processing",
    "natural language processing": "natural language processing",

    "oop": "object oriented programming",
    "object oriented programming": "object oriented programming",
}


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):

            standard_skill = SKILL_ALIASES.get(
                skill,
                skill
            )

            if standard_skill not in found_skills:

                found_skills.append(
                    standard_skill
                )

    return found_skills