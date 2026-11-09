
import re

# Canonical skill names and their recognized aliases
SKILL_ALIASES = {
    # Programming languages
    "python": ["python", "python3"],
    "java": ["java"],
    "javascript": ["javascript", "java script", "js"],
    "typescript": ["typescript"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],

    # Web development
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "flask": ["flask"],
    "django": ["django"],
    "fastapi": ["fastapi", "fast api"],
    "spring boot": ["spring boot", "springboot"],
    "spring framework": ["spring framework"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "node js"],

    # Software engineering
    "object-oriented programming": [
        "object-oriented programming",
        "object oriented programming",
        "oop"
    ],
    "data structures": ["data structures"],
    "algorithms": ["algorithms"],
    "debugging": ["debugging", "debug"],
    "rest api": [
        "rest api", "rest apis", "restful api",
        "restful apis", "rest api development"
    ],
    "software testing": [
        "software testing", "software tests",
        "software test"
    ],
    "api testing": ["api testing"],
    "unit testing": ["unit testing", "unit tests"],
    "pytest": ["pytest"],
    "junit": ["junit", "junit 5"],
    "selenium": ["selenium"],
    "git": ["git"],
    "github": ["github"],
    "agile": ["agile", "scrum"],

    # Databases
    "sql": ["sql"],
    "sqlite": ["sqlite", "sqlite3"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "database design": ["database design"],

    # Cloud and infrastructure
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "linux": ["linux"],
    "networking": ["networking"],
    "cybersecurity": ["cybersecurity", "cyber security"],

    # Artificial intelligence and data
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "excel": ["excel", "microsoft excel"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision"],
    "opencv": ["opencv"],

    # Professional skills
    "problem solving": ["problem solving", "problem-solving"],
    "communication": ["communication", "communication skills"],
    "teamwork": ["teamwork", "team work", "collaboration"],
    "project management": ["project management"],
}


def _contains_skill(text, alias):
    """
    Match a skill or alias without matching it
    inside an unrelated word.
    """
    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(alias)
        + r"(?![a-zA-Z0-9])"
    )

    return re.search(pattern, text, re.IGNORECASE) is not None


def extract_skills(text):
    """
    Extract unique, normalized skills from text.
    """
    if not text:
        return []

    detected = set()

    for skill, aliases in SKILL_ALIASES.items():
        if any(_contains_skill(text, alias) for alias in aliases):
            detected.add(skill)

    return sorted(detected)
