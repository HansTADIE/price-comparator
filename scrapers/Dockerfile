# Scrapy Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Le point d'entrée sera le shell par défaut, pas scrapy crawl automatiquement
CMD ["bash"]