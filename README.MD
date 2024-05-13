# Lemmings Game
E3FI 1I - 2023 - 2024

## Auteurs
- **Nom**: DELMAS Denis
- **Nom**: EDMEE Léon

## Description
Ce projet est une implémentation du célèbre jeu vidéo "Lemmings". Le joueur doit guider une tribu de lemmings à travers divers obstacles et dangers jusqu'à la sortie.

## Stack Technique
- **Langage**: Python 3.10.X
- **Bibliothèque graphique**: Pygame 2.5.X

## Prérequis
- Python 3.x installé sur votre système
- Pygame installé. Vous pouvez l'installer en exécutant la commande suivante :

## Comment lancer le jeu
1. Clonez ce dépôt sur votre machine locale.
2. Assurez-vous d'avoir respecté les prérequis ci-dessus.
3. Ouvrez un terminal et accédez au répertoire du projet.
4. Exécutez le fichier principal du jeu en utilisant la commande suivante : 

    `python main.py` ou `python3 main.py`

## Fonctionnalités supplémentaires
- Boîte de collision calculée en temps réel par rapport au sprite et à l'animation
- Cut dynamique des Bitmaps (suppression de barres noires) afin que les sprites soient plus réalistes et que les collisions soient plus précises et plus rapides
- Affichage des scores
- Affichage du temps
- Fin de partie à la fin de du temps imparti
- Sons
### Actions supplémentaires
- Minage vertical
- Minage en diagonale
- Destruction d'un lemming
- Lemming Kamizake (destruction de zone et du lemming)
- Chute amortie (parachute) (feather falling)
- Vitesse Accrue d'un Lemming (max 4)
