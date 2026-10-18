FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY briefbot ./briefbot
ENV OLLAMA_HOST=http://host.docker.internal:11434
EXPOSE 8000
USER nobody
CMD ["python", "-m", "uvicorn", "briefbot.api:app", "--host", "0.0.0.0", "--port", "8000"]