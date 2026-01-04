FROM python:3.11-slim

WORKDIR /app

# Installer dépendances système nécessaires (libmysqlclient + dépendances pour playwright)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libnss3 \
    libx11-6 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer Python packages (incl. scrapy/playwright si listés)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Si vous utilisez Playwright, installer les navigateurs
# (la commande suivante vient du package playwright)
RUN python -m playwright install --with-deps

# Copier l'application
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
