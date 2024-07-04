Application FastAPI pour la météo
Cette application utilise FastAPI pour interagir avec l'API OpenWeatherMap afin de récupérer et filtrer les données météorologiques pour une ville spécifique.

Configuration requise
Avant de commencer, assurez-vous d'avoir Python installé sur votre système. Vous pouvez télécharger Python depuis python.org.

Installation des dépendances
Clonez ce dépôt GitHub :

Téléchargez le code depuis GitHub ou utilisez Git pour cloner le dépôt :
Installez les dépendances nécessaires :

Utilisez pip pour installer les dépendances requises en exécutant pip install -r requirements.txt.
Configuration de l'API OpenWeatherMap
Assurez-vous d'avoir une clé API valide pour l'API OpenWeatherMap. Remplacez "your_api_key_here" dans le fichier main.py par votre propre clé API.

Démarrage de l'application
Pour démarrer l'application FastAPI, utilisez uvicorn. Exécutez la commande suivante depuis le répertoire racine de votre projet :

Utilisez uvicorn main:app --reload pour démarrer le serveur FastAPI localement, prêt à accepter des requêtes.
Utilisation de l'API
Récupérer les données météorologiques
Pour récupérer les données météorologiques d'une ville spécifique, utilisez l'URL suivante dans votre navigateur ou avec un outil comme curl ou Postman :

Accédez à http://localhost:8000/weather/{city} et remplacez {city} par le nom de la ville pour laquelle vous souhaitez obtenir les données météorologiques.
Filtrer les données météorologiques
Pour filtrer les données météorologiques par un type spécifique (par exemple, température, humidité, vitesse du vent), utilisez l'URL suivante avec le paramètre filter :

Utilisez http://localhost:8000/weather/{city}?filter={type} et remplacez {city} par le nom de la ville et {type} par le type de données que vous souhaitez filtrer (par exemple, temperature, humidity, wind_speed).
Exemples
Pour obtenir les données météorologiques complètes de Lyon :

Accédez à http://localhost:8000/weather/Lyon.
Pour obtenir uniquement la température actuelle de Lyon :

Accédez à http://localhost:8000/weather/Lyon?filter=temperature.
Fonction de sauvegarde des données
Le fichier main.py contient également une fonction pour sauvegarder les données météorologiques dans un fichier JSON local pour une date donnée.

Pour tester la sauvegarde des données météorologiques de Lyon, exécutez la fonction suivante dans le fichier main.py :

Utilisez save_weather_data_to_file(API_KEY, "Lyon") pour créer un fichier JSON avec les données météorologiques de Lyon pour la date actuelle.
