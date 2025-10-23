FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
# Use gunicorn for a production-ready WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]