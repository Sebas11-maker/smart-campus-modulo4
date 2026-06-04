FROM python:3.10-slim

WORKDIR /app

COPY academic-risk-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY academic-risk-service/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]