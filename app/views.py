from app import app
from flask import render_template, request, session, redirect
from flask_session import Session
import os

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    if not session.get("user"):
        return redirect("/login")
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method =='POST':
        session["user"] = request.form.get("user")
        session["password"] = request.form.get("password")
        return redirect("/")
    return render_template('login.html')

@app.route('/pull_day', methods = ['POST'])
def pull_daily_observations():
    import requests
    import json
    import yaml

    session["team"] = request.form.get("team")
    session["day"] = request.form.get("day")
    print("team: " + session["team"])
    print("day: " + session["day"])

    r_session = requests.Session()

    r_session.post('https://3.14.124.94/login', data={"username": session.get("user"), "password": session.get("password")}, verify=False)

    msel_r = r_session.get('https://3.14.124.94/api/measure-evaluations', verify=False)
    msel_json = json.loads(msel_r.text)

    relevant_grading_opportunity = []
    for entry in msel_json:
        if entry["startDay"] == int(session["day"]) and entry["team"] == session["team"]:
            relevant_grading_opportunity.append(entry)
    print(relevant_grading_opportunity)

    matt_responses = []
    matt_responses.append('---\n')
    for entry in relevant_grading_opportunity:
        matt_responses.append('- inject_id: ' + entry['mselId'] + "\n")
        matt_responses.append('  Inject Title: ' + entry['title'] + "\n")
        matt_responses.append('  measure_code: ' + entry['measureCode'] + "\n")
        matt_responses.append('  MOP/MOE Description: ' + entry['description'] + "\n")
        matt_responses.append('  grade: ' + "\n")
        matt_responses.append('  comment: >' + "\n")
        matt_responses.append("\n")

    return render_template('observation_results.html', matt_responses = matt_responses)

@app.route('/update_msel', methods = ['POST'])
def send_observations():
    import requests
    import json
    import yaml

    r_session = requests.Session()

    with open("config.yaml", mode="rt", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    with open(str(config['day']) + ".yaml", mode="rt", encoding="utf-8") as file:
        evaluations = yaml.safe_load(file)

    r_session.post('https://3.14.124.94/login', data={"username": session.get("user"), "password": session.get("password")}, verify=False)

    msel_r = r_session.get('https://3.14.124.94/api/measure-evaluations', verify=False)

    msel_json = json.loads(msel_r.text)

    matt_responses = []

    for entry in msel_json:
        for evaluation in evaluations:
            if entry['mselId'] == evaluation["inject_id"] and entry["measureCode"] == evaluation["measure_code"] and entry["team"] == config["team"]:
                response = r_session.post('https://3.14.124.94/api/measure-evaluations/update', json={"id": entry['id'], "status": evaluation["grade"], "tacticalAssessmentComments": evaluation["comment"], "operationalAssessmentComments": None}, headers={'Content-type': 'application/json; charset=utf-8'}, verify=False)
                matt_responses.append("Observation {} for MSEL {}, measurecode {}, team {} was successfully changed to {}".format(entry['id'], entry['mselId'], entry['measureCode'], entry['team'], evaluation['grade']))
                break

    return render_template('observation_results.html', matt_responses = matt_responses)
