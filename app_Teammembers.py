from flask import Flask, render_template
import requests

app = Flask(__name__)

SHEET_URL = "https://sheets.googleapis.com/v4/spreadsheets/1Lb0_bYdKoKqF5tQvqgFmHjUUcpRyrO4hSD5pxWWlx-4/values/TeamMembers?key=AIzaSyC2DoCbHup7gqIkogj8Klhvz2G6YPLSOXo"

@app.route('/')
def team():
    response = requests.get(SHEET_URL)
    data = response.json()
    rows = data.get("values", [])

    if not rows:
        return "No data found."

    headers = rows[0]
    members = [dict(zip(headers, row)) for row in rows[1:]]

    # Group by Role (normalize role values to lowercase)
    grouped = {
        "Postdoctoral Fellows": [m for m in members if m.get("Role", "").strip().lower() == "pdf"],
        "PhD Candidates": [m for m in members if m.get("Role", "").strip().lower() == "phd"],
        "Msc Candidates": [m for m in members if m.get("Role", "").strip().lower() == "msc"],
        "Interns": [m for m in members if m.get("Role", "").strip().lower() == "intern"]
    }

    return render_template("Main.html", grouped=grouped)
