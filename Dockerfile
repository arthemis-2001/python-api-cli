FROM python:3.12.0-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /cli_app
COPY . .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e ./cli_app

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
ENTRYPOINT ["pytest", "--verbose"]
