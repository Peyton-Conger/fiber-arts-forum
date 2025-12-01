FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=src.wsgi:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.wsgi:app"]
