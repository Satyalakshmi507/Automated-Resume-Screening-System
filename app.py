from flask import Flask, render_template, request
import PyPDF2
import os
from reportlab.pdfgen import canvas

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("resume")

    if file is None or file.filename == "":
        return "Please upload a PDF file."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    try:
        with open(filepath, "rb") as pdf:
            reader = PyPDF2.PdfReader(pdf)

            resume_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text

    except Exception:
        return "Invalid PDF File."

    resume_text = resume_text.lower().replace(" ", "")
    job_description = request.form["jobdescription"].lower().replace(" ", "")

    skills = [
        "python",
        "java",
        "html",
        "css",
        "sql",
        "c",
        "c++",
        "javascript",
        "ai",
        "machinelearning"
    ]

    matched = []
    missing = []

    for skill in skills:
        if skill in job_description:
            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

    total = len(matched) + len(missing)

    if total == 0:
        score = 0
    else:
        score = int((len(matched) / total) * 100)

    if score >= 80:
        rating = "Excellent ⭐⭐⭐⭐⭐"
        suggestion = "Your resume matches the job description very well."

    elif score >= 60:
        rating = "Good ⭐⭐⭐⭐"
        suggestion = "Your resume is good. Add more relevant skills to improve further."

    elif score >= 40:
        rating = "Average ⭐⭐⭐"
        suggestion = "Improve your resume by adding more technical skills."

    else:
        rating = "Needs Improvement ⭐⭐"
        suggestion = "Update your resume with relevant skills and certifications."

    return render_template(
        "result.html",
        score=score,
        matched=matched,
        missing=missing,
        rating=rating,
        suggestion=suggestion
    )


@app.route("/download")
def download():

    pdf = canvas.Canvas("Resume_Result.pdf")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(150, 800, "Resume Screening Report")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 760, "This PDF was generated successfully.")

    pdf.drawString(100, 740, "Thank you for using the Resume Screening System.")

    pdf.drawString(100, 720, "Developed using Python, Flask and PyPDF2.")

    pdf.save()

    return "PDF Generated Successfully. Check your ResumeScreeningSystem folder."


if __name__ == "__main__":
    app.run(debug=True)