# ============================================
# Dockerfile - Frontend (React)
# ============================================

# Stage 1: Build
FROM node:18-alpine AS build

WORKDIR /app

# Copier package files
COPY package*.json ./

# Installer les dépendances
RUN npm ci --include=dev

# Copier le reste des fichiers
COPY . .

# Build l'application
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

WORKDIR /app

# Installer serve
RUN npm install -g serve

# Copier le build depuis l'étape précédente
COPY --from=build /app/build ./build

# Expose port
EXPOSE 3000

# Démarrer serve
CMD ["sh", "-c", "serve -s build -l ${PORT:-3000}"]
