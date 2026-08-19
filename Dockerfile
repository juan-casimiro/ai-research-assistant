FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN python -c "from fastembed import TextEmbedding; from fastembed.rerank.cross_encoder import TextCrossEncoder; TextEmbedding(); TextCrossEncoder(model_name='Xenova/ms-marco-MiniLM-L-6-v2')"

COPY seed_corpus/ ./seed_corpus/

# Forces fastembed to use the weights baked in above — fails loudly on a
# cache-path mismatch instead of silently downloading at runtime. See ADR-003.
ENV HF_HUB_OFFLINE=1

ENV CHROMA_PATH=/data/chroma_db

# Without this, print() output is line-buffered on a non-TTY stdout and
# doesn't reach `docker compose logs` until the buffer flushes. See ADR-003.
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

