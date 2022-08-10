#!/usr/bin/python3
import requests
import json
import yaml

msel_id='32.02.07'

session = requests.Session()

with open("config.yaml", mode="rt", encoding="utf-8") as file:
    config = yaml.safe_load(file)

session.post('https://3.14.124.94/login', data={"username": config["username"], "password": config["password"]}, verify=False)

msel_r = session.get('https://3.14.124.94/api/measure-evaluations', verify=False)

msel_json = json.loads(msel_r.text)

relevant_grading_opportunity = []

for entry in msel_json:
    if entry['startDay'] == config['day'] and entry["team"] == config["team"]:
        relevant_grading_opportunity.append(entry)

with open(str(config['day']) + ".yaml", mode="a", encoding="utf-8") as file:
    file.write('---\n')
    for entry in relevant_grading_opportunity:
        file.write('- inject_id: ' + entry['mselId'] + "\n")
        file.write('  Inject Title: ' + entry['title'] + "\n")
        file.write('  measure_code: ' + entry['measureCode'] + "\n")
        file.write('  MOP/MOE Description: ' + entry['description'] + "\n")
        file.write('  grade: ' + "\n")
        file.write('  comment: >' + "\n")
        file.write("\n")
