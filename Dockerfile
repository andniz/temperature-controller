FROM python:3.8

WORKDIR /srv/temperature-controller

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./temperature_controller/dummy_main.py"]
