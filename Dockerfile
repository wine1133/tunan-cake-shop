# syntax=docker/dockerfile:1

FROM node:20-alpine AS frontend
WORKDIR /workspace/vue-app
COPY vue-app/package.json vue-app/package-lock.json ./
RUN npm ci
COPY vue-app/ ./
RUN npm run build

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app/fastapi-app
COPY fastapi-app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY fastapi-app/ ./
COPY --from=frontend /workspace/vue-app/dist /app/vue-app/dist
EXPOSE 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]