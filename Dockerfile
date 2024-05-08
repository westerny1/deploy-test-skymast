FROM python:3.12.1

WORKDIR /SkyMast

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]