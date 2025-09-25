FROM python:3.12

RUN mkdir /tgbot

WORKDIR /tgbot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]




