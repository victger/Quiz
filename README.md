# Web full stack

Le but de ce projet est de réaliser une application web proposant un quiz personnalisé. Nous effectuerons pour cela des développements front, des développements back, de la conception et de l’UX/UI Design.

Notre projet se compose de deux parties : La "quiz-api" pour le backend et la "quiz-ui" pour le frontend.

Pour le moment,  nous lançons le projet de cette manière :

On lance l'image Docker de production pour l'API :

docker container run -it --rm -p 5000:5000 --name quiz-prod-api victger/quiz-prod-api

On exécute les commandes suivantes dans le dossier quiz-ui :

npm install
npm run dev


## Procédure de lancement

## Back-Office (quiz-api)

Le backend de notre application fonctionne grâce à la stack Flask sur Python. Flask permet de créer des "routes" sur notre site, le rendant facilement navigable.

Pour simplifier la compréhension du code, nous avons séparé les routes par thèmes, ainsi que les composantes nécessaires à l'exécution de notre code. Typiquement, les routes concernant les questions sont séparées des routes permettant d'accéder aux informations du quiz. La base de données et les modèles permettant l'insertion, l'accès et la modification de notre base de données sont aussi gérés dans des dossiers à part dans ce même but.

La gestion de notre base de données repose sur le schéma suivant :

![Alt text](https://quiz-esiee.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F919b8a92-40f3-4d1e-bdfd-efd7d80c126a%2FUntitled.png?table=block&id=caeaf17e-1c8f-4f8d-b689-ce25a00cc8d8&spaceId=83337b1a-cd84-4ed1-842a-89f35d3d47f1&width=2000&userId=&cache=v2)

Des fonctions de conversion de données ont donc été créées à cet effet dans le fichier models.py.
Par ailleurs, les opérations de modifiation des données sont effectuées dans le fichier db.py et appelées dans le dossier "routes" pour les endpoints concernés.

La base de données est stockée dans le fichier "quiz.db".

METTRE LE SCHEMA DE LA BASE DE DONNEES

## Front-Office (quiz-ui)

Le frontend de notre application fonctionne grâce aux stacks Vue, JavaScript, HTML, CSS.


Ce projet a été réalisé par GHATGHUT Abdelraouf, Victor GERARD et Louis CHAUVIN.
