# Image de l'API basée sur une image python
FROM python:3.9-alpine

# Création et positionnement du répertoire par défaut dans le container
WORKDIR /app

# Installer sqlite3 et les dépendances nécessaires
RUN apk add --no-cache sqlite sqlite-dev

# Copie du fichier requirements local (machine hôte) vers le container 
COPY requirements.txt requirements.txt

# Installation des dépendances dans le container
RUN pip install -r requirements.txt

# Copie de l'ensemble du code + dépendances
COPY . .

# Variables d'environnement de production
ENV FLASK_DEBUG=0
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# Ajoute ce script dans le conteneur
COPY init_db.py /app/init_db.py

# Exécute le script pour créer la base de données si elle n'existe pas
RUN python /app/init_db.py

# Informations sur l'image
LABEL maintainer="Nom Prénom <nom.prénom@esiee.fr>" \
    version="1.0"

# Commande de démarrage du serveur gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--log-level", "info", "--error-logfile", "-", "--access-logfile", "-"]