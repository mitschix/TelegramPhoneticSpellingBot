FROM python:3.14-alpine

WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
COPY src/ .
CMD ["python", "bot.py"]
