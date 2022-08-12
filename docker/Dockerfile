FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

WORKDIR /app

COPY . .

RUN pip3 install requests pyyaml Flask-Session xlsxwriter openpyxl
RUN pip3 install -r requirements.txt

ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"
