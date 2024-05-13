try:
    from src.game import *
except ImportError:
    print("Erreur lors de l'importation du module src.game")
    print("Vérifiez que le fichier src/game.py existe bien")
    exit(1)
    