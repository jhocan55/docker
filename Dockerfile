# Base stage
FROM python:3.9-slim AS base
WORKDIR /deps
COPY requirements.txt .
RUN apt-get update && apt-get install -y curl && \
    pip install -r requirements.txt --target=/deps

# Test Authentication stage
FROM python:3.9-slim AS auth_test
WORKDIR /app
COPY --from=base /deps /app
ENV PYTHONPATH=/app
RUN apt-get update && apt-get install -y curl
COPY test_authentication.py .
CMD ["python", "test_authentication.py"]

# Test Authorization stage
FROM python:3.9-slim AS authz_test
WORKDIR /app
COPY --from=base /deps /app
ENV PYTHONPATH=/app
RUN apt-get update && apt-get install -y curl
COPY test_authorization.py .
CMD ["python", "test_authorization.py"]

# Test Content stage
FROM python:3.9-slim AS content_test
WORKDIR /app
COPY --from=base /deps /app
ENV PYTHONPATH=/app
RUN apt-get update && apt-get install -y curl
COPY test_content.py .
CMD ["python", "test_content.py"]
