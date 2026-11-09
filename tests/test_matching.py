from analyzer.matching_engine import analyze_match

def test_match_score_and_skills():
    result = analyze_match(
        "Python Flask SQL developer with Git",
        "Looking for Python Flask developer with Docker and SQL",
        ["python", "flask", "sql", "git"],
        ["python", "flask", "sql", "docker"]
    )
    assert 0 <= result["score"] <= 100
    assert set(result["matched_skills"]) == {"python", "flask", "sql"}
    assert result["missing_skills"] == ["docker"]

def test_empty_job_skills_does_not_crash():
    result = analyze_match("Python developer", "A role with general duties", ["python"], [])
    assert 0 <= result["score"] <= 100
