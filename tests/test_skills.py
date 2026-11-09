from analyzer.skills_extractor import extract_skills
from analyzer.job_analyzer import extract_job_skills

def test_extract_known_skills():
    found = extract_skills("I build apps with Python, Flask, SQL and machine learning.")
    assert "python" in found
    assert "flask" in found
    assert "sql" in found
    assert "machine learning" in found

def test_job_skill_extraction():
    found = extract_job_skills("Requirements: JavaScript, React, Docker, AWS")
    assert set(found) == {"javascript", "react", "docker", "aws"}
