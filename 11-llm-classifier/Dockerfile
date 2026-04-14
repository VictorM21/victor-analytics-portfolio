FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# SQLite DB stored in a named volume at runtime
ENV DB_PATH=/data/predictions.db
ENV CONFIDENCE_THRESHOLD=0.75
ENV OPENAI_MODEL=gpt-4o-mini

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
