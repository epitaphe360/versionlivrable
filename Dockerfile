# ============================================
# Root Dockerfile for Railway - Monorepo setup
# ============================================

FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier TOUT le contexte de build
COPY . .

# Déplacer le contenu du backend vers le répertoire de travail
RUN mv backend/* . && rm -rf backend

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Démarrer l'application avec server.py (fichier à jour)
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}"]
