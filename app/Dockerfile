FROM python:3.13-alpine
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
COPY templates ./templates
RUN adduser -D appuser
USER appuser
EXPOSE 8081
CMD ["sh", "-c", "exec gunicorn --bind ${BINDING_ADDRESS:-0.0.0.0}:${SERVER_PORT:-8081} --workers 2 --access-logfile - app:app"]
