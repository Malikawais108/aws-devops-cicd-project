FROM python:3.11-slim

WORKDIR /app

COPY app/flask-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/flask-app/ .

ENV ENV=production

EXPOSE 5000

CMD ["python", "app.py"]

