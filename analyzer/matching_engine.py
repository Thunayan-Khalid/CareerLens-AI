
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Personalized learning recommendations
LEARNING_ACTIONS = {
    "python": "Build a Python project using clean functions, error handling, and automated tests.",
    "java": "Build a Java application demonstrating OOP, collections, exception handling, and clean code.",
    "javascript": "Create an interactive web application using JavaScript and modern ES6 features.",
    "typescript": "Build an application using TypeScript types, interfaces, and modules.",
    "c++": "Practice C++ programming, memory management, data structures, and algorithms.",
    "c#": "Build a C# application using classes, interfaces, and exception handling.",

    "object-oriented programming": "Practice encapsulation, inheritance, polymorphism, and abstraction in a small application.",
    "data structures": "Practice arrays, linked lists, stacks, queues, trees, and hash maps.",
    "algorithms": "Solve algorithmic problems and analyze time and space complexity.",
    "debugging": "Practice debugging applications using breakpoints, logs, and error analysis.",

    "spring boot": "Build a Spring Boot REST application with controllers, services, and database integration.",
    "spring framework": "Learn dependency injection and build an application using Spring Framework.",
    "flask": "Build a Flask application with input validation, database integration, and documented routes.",
    "django": "Create a Django application using models, views, forms, and authentication.",
    "fastapi": "Build a FastAPI service with validation and documented API endpoints.",
    "react": "Create a React application using reusable components, hooks, and state management.",
    "node.js": "Build a Node.js backend with REST endpoints and database integration.",

    "rest api": "Build and document a REST API with CRUD operations, validation, and HTTP status codes.",
    "software testing": "Create test cases for application features and automate them using a testing framework.",
    "api testing": "Test REST API endpoints, status codes, response data, and error cases.",
    "unit testing": "Write unit tests for individual functions and application components.",
    "pytest": "Create automated Python tests using pytest fixtures and assertions.",
    "junit": "Write Java unit tests using JUnit and organize tests into meaningful test cases.",
    "selenium": "Automate browser workflows using Selenium and create reliable UI tests.",

    "mysql": "Practice SQL queries, joins, constraints, indexes, and relational database design using MySQL.",
    "postgresql": "Build an application connected to PostgreSQL and practice database queries.",
    "sqlite": "Create a database-backed application using SQLite and parameterized queries.",
    "sql": "Practice SELECT, JOIN, GROUP BY, subqueries, and database design.",

    "git": "Demonstrate branching, commits, merging, and pull requests in a Git project.",
    "github": "Publish a documented project on GitHub with a clear commit history.",
    "docker": "Containerize an application and document how to build and run its Docker image.",
    "kubernetes": "Learn Kubernetes basics by deploying a small containerized application.",
    "aws": "Deploy a small application using an AWS service and document the process.",
    "azure": "Deploy a small application using Microsoft Azure.",
    "linux": "Practice Linux commands, file permissions, processes, and shell scripting.",

    "machine learning": "Build and evaluate a supervised machine learning model and explain its metrics.",
    "deep learning": "Build a small neural network and evaluate its performance.",
    "scikit-learn": "Train and evaluate a machine learning model using Scikit-learn pipelines.",
    "pandas": "Analyze a dataset using Pandas and present useful findings.",
    "numpy": "Practice numerical computing and array operations using NumPy.",
    "tensorflow": "Build and train a simple neural network using TensorFlow.",
    "pytorch": "Build and train a neural network using PyTorch.",
    "data analysis": "Analyze a real dataset, clean the data, and communicate findings.",
    "data visualization": "Create charts and a dashboard to communicate data insights.",
    "power bi": "Build a Power BI dashboard with data transformations and KPIs.",
    "tableau": "Create a Tableau dashboard using a real-world dataset.",
    "excel": "Practice formulas, pivot tables, data cleaning, and charts in Excel.",
    "nlp": "Build a text-processing project using NLP techniques.",
    "computer vision": "Build an image-processing project using computer vision.",
    "opencv": "Create an image-processing application using OpenCV.",

    "teamwork": "Demonstrate teamwork through a collaborative project with documented contributions.",
    "communication": "Practice presenting technical projects and documenting decisions clearly.",
    "problem solving": "Demonstrate problem-solving through practical coding challenges.",
    "project management": "Organize a project using milestones, tasks, and priorities.",
    "agile": "Practice Agile workflows using user stories and sprint planning.",
    "cybersecurity": "Learn security fundamentals and practice identifying common vulnerabilities.",
    "networking": "Study TCP/IP, DNS, HTTP, and basic network troubleshooting.",
    "database design": "Design a relational database with normalized tables, keys, and relationships."
}


def calculate_text_similarity(resume_text, job_description):
    """Calculate lexical similarity using TF-IDF and cosine similarity."""

    if not resume_text or not job_description:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform([
            resume_text,
            job_description
        ])

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return float(similarity)

    except ValueError:
        return 0.0


def generate_recommendations(missing, resume_skills, resume_text):
    """Generate recommendations based on detected skill gaps."""

    recommendations = []

    if missing:
        recommendations.append(
            "Priority skill gaps: " + ", ".join(missing[:8]) + "."
        )

        for skill in missing[:5]:
            action = LEARNING_ACTIONS.get(skill)

            if action:
                recommendations.append(
                    f"{skill.title()}: {action}"
                )

    if not resume_skills:
        recommendations.append(
            "Add a clear technical skills section to your resume."
        )

    if len(resume_text.split()) < 120:
        recommendations.append(
            "Add more detail about your projects, experience, "
            "responsibilities, and measurable achievements."
        )

    if not recommendations:
        recommendations.append(
            "Your resume covers the detected job skills. "
            "Strengthen your application with specific project "
            "examples and measurable achievements."
        )

    return recommendations


def analyze_match(resume_text, job_description, resume_skills, job_skills):
    """
    Compare resume skills and text with job requirements.

    Score formula:
    75% skill coverage + 25% text similarity.

    If no job skills are detected, the score uses text similarity
    only and includes a warning in the result.
    """

    resume_text = resume_text or ""
    job_description = job_description or ""

    resume_set = set(resume_skills or [])
    job_set = set(job_skills or [])

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    extra = sorted(resume_set - job_set)

    # Calculate skill coverage
    if job_set:
        skill_coverage = len(matched) / len(job_set)
    else:
        skill_coverage = 0.0

    # Calculate text similarity
    text_similarity = calculate_text_similarity(
        resume_text,
        job_description
    )

    # Calculate overall score
    if job_set:
        score = (
            0.75 * skill_coverage
            + 0.25 * text_similarity
        ) * 100

        score_note = (
            "Score combines detected skill coverage (75%) "
            "and text similarity (25%)."
        )
    else:
        score = text_similarity * 100

        score_note = (
            "No recognized job skills were detected. "
            "This score is based on text similarity only "
            "and should be interpreted cautiously."
        )

    score = max(0, min(100, round(score)))

    # Assessment level
    if score >= 75:
        level = "Strong alignment"
    elif score >= 45:
        level = "Moderate alignment"
    else:
        level = "Needs improvement"

    # Generate personalized recommendations
    recommendations = generate_recommendations(
        missing,
        resume_set,
        resume_text
    )

    return {
        "score": score,
        "level": level,
        "matched_skills": matched,
        "missing_skills": missing,
        "additional_skills": extra,
        "resume_skill_count": len(resume_set),
        "job_skill_count": len(job_set),
        "text_similarity": round(text_similarity * 100, 1),
        "skill_coverage": round(skill_coverage * 100, 1),
        "recommendations": recommendations,
        "score_note": score_note,
        "disclaimer": (
            "This score is an indicative text and skill alignment "
            "assessment, not a prediction of hiring success."
        )
    }
