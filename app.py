from flask import Flask, render_template, request

from db import get_connection
from career_engine import get_career_data

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


@app.route("/result", methods=["POST"])
def result():

    name = request.form["name"]
    education = request.form["education"]
    skills = request.form["skills"]
    interests = request.form["interests"]
    goal = request.form["goal"]

    career_data = get_career_data(name, education, skills, interests, goal)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assessments
        (name, education, skills, interests, goal, career, score)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        name,
        education,
        skills,
        interests,
        goal,
        career_data["career"],
        career_data["score"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return render_template(
        "result.html",
        name=name,
        education=education,
        skills=skills,
        interests=interests,
        goal=goal,
        career=career_data["career"],
        score=career_data["score"],
        technologies=career_data["technologies"],
        roadmap=career_data["roadmap"]
    )


@app.route("/history")
def history():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM assessments
        ORDER BY created_at DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("history.html", records=records)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        print("Contact form:", name, email, message)

        return "Message sent successfully!"

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)