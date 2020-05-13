FROM python:3.8

RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/luizzan/srtlearn.git
WORKDIR srtlearn
RUN pip install --no-cache-dir streamlit

RUN ["streamlit", "run", "app.py"]
