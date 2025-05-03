FROM python:3-slim AS builder

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/python

FROM gcr.io/distroless/python3-debian12

COPY --from=builder /python /python
COPY . /app

WORKDIR /app
ENV PYTHONPATH "/python:/app"
CMD ["/app/main.py"]
