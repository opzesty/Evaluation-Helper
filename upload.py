#!/usr/bin/python3
import requests
import json
import yaml
import os


session = requests.Session()

with open("config.yaml", mode="rt", encoding="utf-8") as file:
    config = yaml.safe_load(file)

with open(str(config['day']) + ".yaml", mode="rt", encoding="utf-8") as file:
    evaluations = yaml.safe_load(file)

session.post('https://3.14.124.94/login', data={"username": os.environ["matt_user"], "password": os.environ["matt_password"]}, verify=False)

msel_r = session.get('https://3.14.124.94/api/measure-evaluations', verify=False)

msel_json = json.loads(msel_r.text)

relevant_msel = []

for entry in msel_json:
    for evaluation in evaluations:
        if entry['mselId'] == evaluation["inject_id"] and entry["measureCode"] == evaluation["measure_code"] and entry["team"] == config["team"]:
            response = session.post('https://3.14.124.94/api/measure-evaluations/update', json={"id": entry['id'], "status": evaluation["grade"], "tacticalAssessmentComments": evaluation["comment"], "operationalAssessmentComments": None}, headers={'Content-type': 'application/json; charset=utf-8'}, verify=False)
            print("Observation {} for MSEL {}, measurecode {}, team {} was successfully changed to {}".format(entry['id'], entry['mselId'], entry['measureCode'], entry['team'], evaluation['grade']))
            break
