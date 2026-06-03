from flask import Flask, render_template, request, redirect
import requests
from database import db, Insight

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///insights.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        repo = request.form["repo"]
        note = request.form["note"]
        priority = request.form["priority"]

        # 🔥 AUTO FETCH FROM GITHUB API
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url)

        if response.status_code != 200:
            return "Repository not found or invalid format"

        data = response.json()

        new_entry = Insight(
            repo_name=repo,
            stars=data["stargazers_count"],
            forks=data["forks_count"],
            open_issues=data["open_issues_count"],
            language=data["language"],
            note=note,
            priority=priority
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect("/insights")

    return render_template("index.html")


@app.route("/insights")
def insights():
    data = Insight.query.order_by(Insight.timestamp.desc()).all()
    return render_template("insights.html", data=data)


@app.route("/delete/<int:id>")
def delete(id):
    item = Insight.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect("/insights")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)