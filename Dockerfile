FROM continuumio/miniconda3:4.9.2-alpine

COPY requirements.txt requirements.txt
COPY main.py main.py

RUN pip install -r requirements.txt
ENTRYPOINT ["start.sh"]
CMD ["0.0.0.0", "80"]
