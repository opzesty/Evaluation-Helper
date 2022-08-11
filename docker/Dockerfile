FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install requests pyyaml

ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"

CMD ["python3", "upload.py"] 
