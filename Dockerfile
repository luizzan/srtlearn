FROM python:3.8

RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/umairnow/LocalizableGenerator.git

RUN ["streamlit", "run", "app.py"]
