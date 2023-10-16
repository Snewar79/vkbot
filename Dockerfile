FROM python:3.11

WORKDIR app
COPY . .
RUN python3 -m pip install -r requirements.txt