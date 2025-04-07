from flask import Flask, render_template, abort
import requests
import random
import re

app = Flask(__name__)

SHEET_URL = "https://sheets.googleapis.com/v4/spreadsheets/1Lb0_bYdKoKqF5tQvqgFmHjUUcpRyrO4hSD5pxWWlx-4/values/TeamMembers?key=AIzaSyC2DoCbHup7gqIkogj8Klhvz2G6YPLSOXo"

url = "https://sheets.googleapis.com/v4/spreadsheets/1Lb0_bYdKoKqF5tQvqgFmHjUUcpRyrO4hSD5pxWWlx-4/values/Publications?key=AIzaSyC2DoCbHup7gqIkogj8Klhvz2G6YPLSOXo"


def get_members():
    response = requests.get(SHEET_URL)
    data = response.json()
    rows = data.get("values", [])
    if not rows:
        return []
    headers = rows[0]
    print("Headers:", headers)  # Debug: Check headers
    members = [dict(zip(headers, row)) for row in rows[1:]]
    print("Members:", members)  # Debug: Check the actual members list
    return members


def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.strip().lower())


@app.route('/')
def home():
    return "<h1>Welcome to the Team Site!</h1><p>Try /student/avik-mandal</p>"


def fetch_publications():
    response = requests.get(url)
    data = response.json()
    
    # Print out the raw response data to check the structure
    print(data)  # Debugging line to see the raw data from Google Sheets
    
    rows = data.get('values', [])
    
    publications = []
    if len(rows) > 1:
        for row in rows[1:]:  # Skip the header row
            if len(row) >= 9:  # Check if the row has enough columns
                publication = {
                    "href_link": row[0],
                    "image_address": row[1],
                    "pub_index": int(row[2]) if row[2].isdigit() else 0,
                    "pub_title": row[3],
                    "pub_authors": row[4],
                    "pub_journal": row[5],
                    "abstract": row[6],
                    "doi": row[7],
                    "altmetricslink": row[8],
                }
                publications.append(publication)

    return publications


@app.route('/student/<slug>')
def student_profile(slug):
    members = get_members()
    publications = fetch_publications()  # Fetch publications as well
    for member in members:
        full_name = member.get("Full Name", "")
        if slugify(full_name) == slug:
            return render_template("studenttemplate.html", member=member, publications=publications)
    abort(404)  # Not found
def index():
    publications = fetch_publications()  # Fetch publications data from Google Sheets
    return render_template('studenttemplate.html', publications=publications)