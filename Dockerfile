FROM python:3.10-slim

WORKDIR /app

COPY Classroom-Management-main/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "Classroom-Management-main/main.py"]
