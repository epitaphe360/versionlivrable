# ============================================
# Dockerfile - Backend Only (Railway)
# ============================================
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier tout le contenu du backend
COPY . .

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Démarrer l'application avec server.py (fichier à jour)
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]

