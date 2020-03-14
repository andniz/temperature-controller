FROM python:3.8

WORKDIR /srv/temperature-controller

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./dummy_main.py"]
