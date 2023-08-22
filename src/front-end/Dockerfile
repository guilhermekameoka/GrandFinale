FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "application.py"]