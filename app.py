
import os
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from analyzer.resume_parser import extract_pdf_text
from analyzer.skills_extractor import extract_skills
from analyzer.job_analyzer import extract_job_skills
from analyzer.matching_engine import analyze_match
from database.db import init_db, save_analysis, get_history


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}

# Initialize the database
init_db()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        flash("Please upload a PDF resume.")
        return redirect(url_for("index"))

    file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if not file or not file.filename:
        flash("Please choose a resume file.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Only PDF files are supported.")
        return redirect(url_for("index"))

    if not job_description:
        flash("Please paste a job description.")
        return redirect(url_for("index"))

    if len(job_description) > 20000:
        flash("The job description is too long. Please shorten it.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename) or "resume.pdf"

    # Process the resume in memory without saving it to disk.
    pdf_bytes = file.read()

    if not pdf_bytes:
        flash("The uploaded file is empty.")
        return redirect(url_for("index"))

    try:
        resume_text = extract_pdf_text(pdf_bytes)
    except ValueError as exc:
        flash(str(exc))
        return redirect(url_for("index"))

    if len(resume_text.strip()) < 30:
        flash(
            "Not enough readable text was found. "
            "Please upload a text-based PDF instead of a scanned image."
        )
        return redirect(url_for("index"))

    resume_skills = extract_skills(resume_text)
    job_skills = extract_job_skills(job_description)

    result = analyze_match(
        resume_text,
        job_description,
        resume_skills,
        job_skills
    )

    analysis_id = save_analysis(filename, result)

    return render_template(
        "results.html",
        result=result,
        filename=filename,
        analysis_id=analysis_id
    )


@app.route("/history")
def history():
    records = get_history()
    return render_template("history.html", records=records)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.errorhandler(413)
def file_too_large(error):
    flash("File is too large. Maximum allowed size is 5 MB.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
