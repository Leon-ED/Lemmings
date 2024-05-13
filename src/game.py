"""
Ce module implémente un simple jeu de Lemmings en utilisant Pygame.

Fonctions :
- ChargeSerieSprites(id) : Charge et découpe des sprites à partir d'une feuille de sprites en fonction de l'ID donné.
- crop_surface(surf) : Découpe une surface pour supprimer les bordures noires environnantes.
- remove_columns(sprite_list) : Supprime les colonnes noires d'une liste de sprites.
- actionMarche(lemming) : Effectue l'action de marche pour un lemming.
- actionChute(lemming) : Effectue l'action de chute pour un lemming.
- actionFloater(lemming) : Effectue l'action de flottement pour un lemming.
- actionBomber(lemming) : Effectue l'action de bombardement pour un lemming.
- actionDead(lemming) : Effectue l'action de mort pour un lemming.
- actionStop(lemming) : Effectue l'action d'arrêt pour un lemming.
- actionCreuser(lemming) : Effectue l'action de creuser pour un lemming.
- actionCreuserHorizontal(lemming) : Effectue l'action de creuser horizontalement pour un lemming.
- creerLemming() : Crée un nouveau lemming et l'ajoute au jeu.
- draw_Action_button(screen, action) : Dessine le bouton d'action sur l'écran.
- check_click_on_lemming(x, y) : Vérifie si un événement de clic s'est produit sur un lemming.
- check_collision_lemming_stopped(lemming) : Vérifie si un lemming est en collision avec un lemming arrêté.
- check_collision_lemming_wall(lemming) : Vérifie si un lemming est en collision avec un mur.
- check_if_lemming_can_fall(x, y, lemming) : Vérifie si un lemming peut tomber à sa position actuelle.
- is_on_exit(x, y, lemming) : Vérifie si un lemming est sur la sortie.
- draw_hitbox(screen, lemming) : Dessine la boîte de collision d'un lemming sur l'écran.
- show_stats() : Affiche les statistiques du jeu sur l'écran.

Constantes :
- BLACK : Un tuple représentant la couleur noire.
- RED : Un tuple représentant la couleur rouge.
- WHITE : Un tuple représentant la couleur blanche.

Variables :
- WINDOW_SIZE : Une liste représentant la taille de la fenêtre de jeu.
- screen : L'objet d'écran Pygame.
- done : Un drapeau booléen indiquant si la boucle de jeu doit continuer.
- clock : Objet d'horloge Pygame pour contrôler le taux d'images par seconde.
- lemmingsLIST : Une liste contenant les lemmings actuellement dans le jeu.
- compteur_creation : Un entier comptant le nombre de lemmings créés.
- nb_lemmings : Le nombre total de lemmings à créer.
- nb_lemmings_arrived : Le nombre de lemmings qui ont atteint la sortie.
- start_actions : Un tuple représentant la position de départ des boutons d'action.
- size_of_actions : La taille de chaque bouton d'action.
- height_of_actions : La hauteur des boutons d'action.
- nb_of_actions : Le nombre de boutons d'action disponibles.
- action_button_choose : Le bouton d'action actuellement sélectionné.
- action_button_etat : Une liste contenant l'état correspondant à chaque bouton d'action.
- EtatMarche, EtatChute, EtatStop, EtatDead, EtatMiner, EtatMinerHorizontal, EtatFloater, EtatBomber : Constantes représentant différents états d'un lemming.
"""

import random
try:
    import pygame
except ImportError:
    print("Pygame ne semble pas installé sur le système")
    print("Veuillez l'installer en utilisant la commande suivante :")
    print("pip install pygame")
    print("Si pygame est déjà installé, assurez vous d'utiliser la bonne version de l'intepréteur python")
    exit(1)
import os, inspect
from time import sleep



def ChargeSerieSprites(id):
    """
    Charge et découpe des sprites en fonction de l'ID donné.

    Paramètres :
    - id : Un entier représentant l'ID de la série de sprites à charger.

    Retourne :
    Une liste de surfaces représentant les sprites de la série chargée.
    """
    sprite = []
    for i in range(18):
        spr = planche_sprites.subsurface((LARG * i, LARG * id, LARG, LARG))
        test = spr.get_at((10, 10))
        if test != RED:
            spr = crop_surface(spr)
            sprite.append(spr)

    # Remove all the columns of black pixels
    #  sprite = remove_columns(sprite)

    # Remove all the rows of black pixels
    #  sprite = remove_rows(sprite)

    return sprite


def crop_surface(surf):
    """
    Découpe une surface pour supprimer les bordures noires environnantes.

    Paramètres :
    - surf : Une surface Pygame à découper.

    Retourne :
    Une nouvelle surface Pygame sans les bordures noires.
    """
    # Trouver les dimensions de l'image
    width = surf.get_width()
    height = surf.get_height()

    # Initialiser les coordonnées des bords
    left_border = width
    right_border = 0

    # Parcourir chaque ligne de l'image pour trouver les bords noirs
    for y in range(height):
        for x in range(width):
            pixel_color = surf.get_at((x, y))
            # Si la couleur du pixel n'est pas noire, mettre à jour les bords
            if pixel_color != BLACK:
                left_border = min(left_border, x)
                right_border = max(right_border, x)

    # Découper l'image en fonction des bords trouvés
    if left_border < right_border:
        cropped_surf = surf.subsurface((left_border, 0, right_border - left_border + 1, height))
    else:
        cropped_surf = surf.copy()  # Pas de bordures noires détectées, renvoyer une copie non modifiée

    return cropped_surf



def remove_columns(sprite_list):
    """
    Supprime les colonnes noires d'une liste de sprites.

    Paramètres :
    - sprite_list : Une liste de surfaces Pygame représentant les sprites.

    Retourne :
    Une liste de surfaces Pygame sans les colonnes noires.
    """
    if not sprite_list:
        return sprite_list

    # Get the width of the first sprite
    sprite_width = sprite_list[0].get_width()

    # Iterate through each column
    for col in range(sprite_width):
        column_empty = True
        # Check if the entire column is black in each sprite
        for sprite in sprite_list:
            if sprite.get_at((col, 0)) != BLACK:
                column_empty = False
                break
        # If the column is entirely black, remove it from all sprites
        if column_empty:
            for sprite in sprite_list:
                sprite_list[sprite_list.index(sprite)] = sprite.subsurface(
                    (0, 0, col, sprite.get_height())
                )
    return sprite_list


def actionMarche(lemming):
    """
    Effectue l'action de marche pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    lemming["x"] += lemming["vx"] * 1


def actionChute(lemming):
    """
    Effectue l'action de chute pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    lemming["y"] += 1
    lemming["fallcount"] += 1
    
def actionFloater(lemming):
    """
    Effectue l'action de flottement pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    lemming["y"] += 1

def actionBomber(lemming):
    """
    Effectue l'action de bombardement pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    # Effacer du décor autour du lemming en sphère
    if not lemming["dead_no_anim"]:
        return
    x_middle = lemming["x"] + lemming["surface"].get_width() // 2
    y_middle = lemming["y"] + lemming["surface"].get_height() // 2
    radius = 30
    for i in range(-radius, radius+1):
        for j in range(-radius, radius +1):
            if i ** 2 + j ** 2 <= radius ** 2:    # Vérifie si le point (i, j) est dans le rayon autour du centre (0, 0)
                fond.set_at((x_middle + i, y_middle + j), BLACK)
    lemming["etat"] = EtatDead
    
def actionDead(lemming):
    """
    Effectue l'action de mort pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    pass


def actionStop(lemming):
    """
    Effectue l'action d'arrêt pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    pass

def actionSpeeder(lemming):
    """
    Effectue l'action de vitesse pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    global currentActiveSpeeders
    # # print(currentActiveSpeeders)
    if currentActiveSpeeders < MAX_LEMMING_ACTIVE_SPEED_STATE or "inSpeed" in lemming.keys():
        if "inSpeed" not in lemming.keys():
            currentActiveSpeeders += 1
        lemming["inSpeed"] = True
        lemming["x"] += lemming["vx"] * 3
    else:
        lemming["etat"] = EtatMarche
        no_sound.play()


# Ajouter l'état Creuser et la logique d'animation
def actionCreuser(lemming):
    """
    Effectue l'action de creuser verticalement pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    lemming["creuser_timer"] += 1
    if lemming["creuser_timer"] % 10 == 0:  # Toutes les 0.5 secondes
        # Effacer du décor sous le lemming
        for i in range(20):
            fond.set_at((lemming["x"] + i, lemming["y"] + lemming["surface"].get_height()), BLACK)
        lemming["y"] += 1  # Descendre d'un pixel pour continuer à creuser
      
def  actionCreuserDiagonal(lemming):
    """ 
    Effectue l'action de creuser en diagonale pour un lemming.
    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    
    lemming["creuser_timer"] += 1
    if lemming["creuser_timer"] % 20 == 0:  # Toutes les 1 secondes
        # Effacer du décor sous le lemming
        for i in range(40):
            fond.set_at((lemming["x"] + i, lemming["y"] + lemming["surface"].get_height()), BLACK)
        lemming["y"] += 1  # Descendre d'un pixel pour continuer à creuser
        lemming["x"] += lemming["vx"]  # Déplacer le lemming en diagonale
        
        
def actionCreuserHorizontal(lemming):
    """
    Effectue l'action de creuser horizontalement pour un lemming.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    lemming["creuser_timer"] += 1
    # Effacer du décor devant le lemming en fonction de sa direction
    if lemming["vx"] == 1:
        # Si le lemming va vers la droite, creuser à droite
        for j in range(2):
            for i in range(lemming["surface"].get_height()):
                fond.set_at((lemming["x"] + lemming["surface"].get_width() +j, lemming["y"] +i), BLACK)
    else:
        # Sinon, le lemming va vers la gauche, creuser à gauche
        for j in range(2):
            for i in range(lemming["surface"].get_height()):
                fond.set_at((lemming["x"] - j, lemming["y"] + i), BLACK)
                
    if lemming["creuser_timer"] % 5 == 0:  # Toutes les 0.25 secondes
        # Déplacer le lemming dans la direction où il a creusé
        lemming["x"] += lemming["vx"]




# Fonction pour créer un nouveau lemming
def creerLemming():
    """
    Crée un nouveau lemming et l'ajoute au jeu.
    """
    new_lemming = {
        "x": 256,
        "y": 125,
        "vx": 1,
        "etat": EtatChute,
        "fallcount": 0,
        "decal": random.randint(0, 10),
        "dead_no_anim": False,
        "creuser_timer": 0,
        "surface": tombe[0],
    }
    lemmingsLIST.append(new_lemming)



def draw_Action_button(screen, action):
    """
    Dessine le bouton d'action sur l'écran.

    Paramètres :
    - screen : L'objet d'écran Pygame.
    - action : L'index de l'action à dessiner.
    """
    pygame.draw.rect(
        screen,
        WHITE,
        (
            start_actions[0] + action * size_of_actions,
            start_actions[1],
            size_of_actions,
            height_of_actions,
        ),
        2,
    )


def check_click_on_lemming(x, y):
    """
    Vérifie si un événement de clic s'est produit sur un lemming.

    Paramètres :
    - x : La position x du clic.
    - y : La position y du clic.

    Retourne :
    Un tuple (bool, int) où le booléen indique si le clic s'est produit sur un lemming et l'entier représente l'index du lemming dans la liste.
    """
    for onelemming in lemmingsLIST:
        xx = onelemming["x"]
        yy = onelemming["y"]
        surface = onelemming["surface"]
        # loop each pixel and check if the click is on the lemming and not on a black pixel of the lemming
        for i in range(surface.get_width()):
            for j in range(surface.get_height()):
                if xx + i == x and yy + j == y:
                    return True, lemmingsLIST.index(onelemming)
    return False, None


def check_collision_lemming_stopped(lemming):
    """
    Vérifie si un lemming est en collision avec un lemming arrêté.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.

    Retourne :
    Un booléen indiquant s'il y a collision avec un lemming arrêté.
    """
    for onelemming in lemmingsLIST:
        if onelemming["etat"] == EtatStop and onelemming != lemming:
            # Get the surface of the lemming sprite
            lemming_rect = pygame.Rect(onelemming["x"], onelemming["y"], onelemming["surface"].get_width(), onelemming["surface"].get_height())

            # Get the surface of the other lemming
            other_lemming_rect = pygame.Rect(lemming["x"], lemming["y"], lemming["surface"].get_width(), lemming["surface"].get_height())

            # Check if the two lemmings are in collision
            if lemming_rect.colliderect(other_lemming_rect):
                # print("collision with lemming")

                # Get the area of intersection
                intersection_rect = lemming_rect.clip(other_lemming_rect)
                #  draw the intersection rectangle
                # pygame.draw.rect(screen, (255,0,255), intersection_rect, 2)
                return True

                # Iterate through the pixels in the intersection area
                # for x in range(intersection_rect.left, intersection_rect.right):
                #    for y in range(intersection_rect.top, intersection_rect.bottom):
                #       # Get the color of the pixel
                #       color = screen.get_at((x, y))
                #       # screen.set_at((x, y), (255,0,255))
                #       # Check if the pixel is not black
                #       if color == BLACK:
                #          return True  # Collision with non-black pixels detected
                #          # color the pixel collided in PURPLE

    return False  # No collision with non-black pixels detected


def check_collision_lemming_wall(lemming):
    """
    Vérifie si un lemming est en collision avec un mur.

    Paramètres :
    - lemming : Un dictionnaire représentant les informations d'un lemming.

    Retourne :
    Un booléen indiquant s'il y a collision avec un mur.
    """
    for i in range(lemming["surface"].get_height()):
        if lemming["vx"] == -1:
            if fond.get_at((lemming["x"] - 1, lemming["y"] + i)) != BLACK:
                # print("coliision with wall")
                return True
        else:
            if fond.get_at((lemming["x"] + lemming["surface"].get_width() + 1, lemming["y"] + i)) != BLACK:
                # print("coliision with wall")

                return True
    return False


def check_if_lemming_can_fall(x, y, lemming):
    """
    Vérifie si un lemming peut tomber à sa position actuelle.

    Paramètres :
    - x : La position x du lemming.
    - y : La position y du lemming.
    - lemming : Un dictionnaire représentant les informations d'un lemming.

    Retourne :
    La couleur du pixel situé en dessous du lemming.
    """
    lemming_height = lemming["surface"].get_height()
    lemmint_width = lemming["surface"].get_width()
    for i in range(lemmint_width):
        if screen.get_at((x + i, y + lemming_height)) != BLACK:
            return screen.get_at((x + i, y + lemming_height))
    return BLACK


def is_on_exit(x, y, lemming):
    """
    Vérifie si un lemming est sur la sortie.

    Paramètres :
    - x : La position x du lemming.
    - y : La position y du lemming.
    - lemming : Un dictionnaire représentant les informations d'un lemming.

    Retourne :
    Un booléen indiquant si le lemming est sur la sortie.
    """
    exit_rect = pygame.Rect(646, 250, sortie.get_width(), sortie.get_height())
    lemming_rect = pygame.Rect(x, y, lemming["surface"].get_width(), lemming["surface"].get_height())
    
    # Check if the lemming's rectangle is entirely inside the exit's rectangle
    if exit_rect.contains(lemming_rect):
        return True
    else:
        return False


def draw_hitbox(screen, lemming):
    """
    Dessine la boîte de collision d'un lemming sur l'écran.

    Paramètres :
    - screen : L'objet d'écran Pygame.
    - lemming : Un dictionnaire représentant les informations d'un lemming.
    """
    return
    xx = lemming["x"]
    yy = lemming["y"]
    width = lemming["surface"].get_width()  # Utiliser la largeur réelle de la surface
    height = lemming["surface"].get_height()  # Hauteur de la surface du lemming
    pygame.draw.rect(screen, (255, 0, 0), (xx, yy, width, height), 1)


def show_stats():
    """
    Affiche les statistiques du jeu sur l'écran.
    """
    font = pygame.font.Font(None, 36)
    percentage_text = font.render("IN {:.0f}%".format((nb_lemmings_arrived / nb_lemmings) * 100), True, WHITE)
    percentage_rect = percentage_text.get_rect()
    percentage_rect.topleft = (80, WINDOW_SIZE[1] - 40)  # Position en bas à gauche
    screen.blit(percentage_text, percentage_rect)
    
    nb_lemmings_text = font.render("OUT {}".format(len(lemmingsLIST)), True, WHITE)
    nb_lemmings_rect = nb_lemmings_text.get_rect()
    nb_lemmings_rect.topleft = (WINDOW_SIZE[0] -150, WINDOW_SIZE[1] - 40)  # Position en bas à droite
    screen.blit(nb_lemmings_text, nb_lemmings_rect)
    
    # Show the time format : MINUTES-SECONDS left
    time_left = 120 +1 - (pygame.time.get_ticks() / 1000) # 120 seconds
    minutes = int(time_left / 60)
    seconds = int(time_left % 60)
    time_text = font.render("TIME {:01d}-{:02d}".format(minutes, seconds), True, WHITE)
    time_rect = time_text.get_rect()
    time_rect.topleft = (WINDOW_SIZE[0] -170, 20)  # Position en haut à droite
    screen.blit(time_text, time_rect)

def draw_selected_state(screen, selected_state):
    font = pygame.font.Font(None, 36)
    state_text = font.render("State: {}".format(selected_state), True, WHITE)
    state_rect = state_text.get_rect()
    state_rect.topleft = (30, WINDOW_SIZE[1] - 80)  # Position en bas au centre
    screen.blit(state_text, state_rect)


# recherche du répertoire de travail
scriptPATH = os.path.abspath(
    inspect.getsourcefile(lambda: 0)
)  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"..", "assets")
imgs = os.path.join(assets, "img")
audio = os.path.join(assets, "audio")
fond = pygame.image.load(os.path.join(imgs,"map.png"))
sortie = pygame.image.load(os.path.join(imgs, "sortie.png"))
planche_sprites = pygame.image.load(os.path.join(imgs, "planche.png"))
planche_sprites.set_colorkey((0, 0, 0))

BLACK = (0, 0, 0, 255)
RED = (255, 0, 0, 255)
WHITE = (255, 255, 255, 255)

LARG = 30




###################################################################################

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Sounds and music
no_sound = pygame.mixer.Sound(os.path.join(audio, "no.mp3"))
no_sound.set_volume(100)
die_sound = pygame.mixer.Sound(os.path.join(audio, "die.mp3"))
click_sound = pygame.mixer.Sound(os.path.join(audio, "click.mp3"))
click_sound.set_volume(100)
action_sound = pygame.mixer.Sound(os.path.join(audio, "action.mp3"))
action_sound.set_volume(100)
win_sound = pygame.mixer.Sound(os.path.join(audio, "win.mp3"))
win_sound.set_volume(100)
loose_sound = pygame.mixer.Sound(os.path.join(audio, "loose.mp3"))
loose_sound.set_volume(100)
escaped_sound = pygame.mixer.Sound(os.path.join(audio, "escaped.mp3"))
escaped_sound.set_volume(100)
music = pygame.mixer.Sound(os.path.join(audio, "background_music.mp3"))
music.set_volume(0.3)
currentActiveSpeeders = 0
MAX_LEMMING_ACTIVE_SPEED_STATE = 4
# Play background music in a loop
music.play(-1)  # -1 will loop the music indefinitely

# Set title of screen
pygame.display.set_caption("LEMMINGS")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# liste des etats
EtatMarche = "Marche"
EtatChute = "Chute"
EtatStop = "Arrêt"
EtatDead = "Tuer"
EtatMiner = "Miner vers le bas"
EtatMinerHorizontal = "Minage Verticalement"
EtatSpeeder = "Vélocité Accrue (max " + str(MAX_LEMMING_ACTIVE_SPEED_STATE) + ") lemmings"
EtatMinerDiagonal = "Minage Diagonale"
EtatFloater = "Flotter"
EtatBomber = "Kamizake"

# liste des lemmins en cours de jeu

lemmingsLIST = []
compteur_creation = 0
nb_lemmings = 15
nb_lemmings_arrived = 0

start_actions = (190, 343)
size_of_actions = 48
height_of_actions = 56
nb_of_actions = 9

action_button_choose = None
action_button_etat = [
    EtatSpeeder,
    EtatDead,
    EtatStop,
    EtatFloater,
    EtatMinerDiagonal,
    EtatDead,
    EtatMinerHorizontal,
    EtatMiner,
    EtatBomber,
]




# -------- Main Program Loop -----------

marche = ChargeSerieSprites(0)
marche_flipped = [
    pygame.transform.flip(marche[i], True, False) for i in range(len(marche))
]
tombe = ChargeSerieSprites(1)
tombe_flipped = [
    pygame.transform.flip(tombe[i], True, False) for i in range(len(tombe))
]
dead = ChargeSerieSprites(10)
dead_flipped = [pygame.transform.flip(dead[i], True, False) for i in range(len(dead))]
stop = ChargeSerieSprites(4)
stop_flipped = [pygame.transform.flip(stop[i], True, False) for i in range(len(stop))]
miner = ChargeSerieSprites(9)
miner_flipped = [
    pygame.transform.flip(miner[i], True, False) for i in range(len(miner))
]
floater = ChargeSerieSprites(3)
floater_flipped = [ 
    pygame.transform.flip(floater[i], True, False) for i in range(len(floater))
]
bomber = ChargeSerieSprites(5)
bomber_flipped = [
    pygame.transform.flip(bomber[i], True, False) for i in range(len(bomber))
]




ActionToPerform = {
    EtatSpeeder: actionSpeeder,
    EtatMarche: actionMarche,
    EtatChute: actionChute,
    EtatDead: actionDead,
    EtatStop: actionStop,
    EtatMiner: actionCreuser,
    EtatFloater: actionFloater,
    EtatMinerHorizontal: actionCreuserHorizontal,
    EtatMinerDiagonal: actionCreuserDiagonal,
    EtatBomber: actionBomber,
}


pygame.mouse.set_visible(1)

while not done:
    event = pygame.event.Event(pygame.USEREVENT)  # Remise à zero de la variable event

    time = int(pygame.time.get_ticks() / 100)

    # draw background
    screen.blit(fond, (0, 0))
    # Positionate the sortie
    screen.blit(sortie, (646, 250))

    if action_button_choose != None:
        draw_Action_button(screen, action_button_choose)

    # # Draw REd square arround each action button for debug
    # for i in range(nb_of_actions):
    #    pygame.draw.rect(screen, (255,0,0), (start_actions[0] + i*size_of_actions, start_actions[1], size_of_actions, height_of_actions), 2)

    # creation des lemmings : 1 lemming toutes les 1,5 secondes
    if (compteur_creation < nb_lemmings) and ((time + compteur_creation) % 30 == 0):
        compteur_creation += 1
        creerLemming()

    # gestion des évènements

    for event in pygame.event.get():  # User did something

        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        # pygame.draw.line(screen, (255,255,255),(x-5,y),(x+5,y))
        # pygame.draw.line(screen, (255,255,255),(x,y-5),(x,y+5))
        # print("Click - Grid coordinates: ", x, y)

        # Check if click is on one of the lemmins
        if action_button_choose != None:
            click_on_lemming, lemming_id = check_click_on_lemming(x, y)
            if click_on_lemming:
                lemming_clicked = lemmingsLIST[lemming_id]
                # print("Click on lemming: ", lemming_id, action_button_etat[action_button_choose])
                if action_button_etat[action_button_choose] in ActionToPerform.keys():
                    lemming_clicked["etat"] = action_button_etat[action_button_choose]
                    action_sound.play()
                
                # if action_button_etat[action_button_choose] == EtatStop:
                #     if lemming_clicked["etat"] == EtatMarche:
                #         lemming_clicked["etat"] = EtatStop
                # elif action_button_etat[action_button_choose] == EtatDead:
                #     lemming_clicked["etat"] = EtatDead

                # elif action_button_etat[action_button_choose] == EtatMiner:
                #     lemming_clicked["etat"] = EtatMiner
                    
                # elif action_button_etat[action_button_choose] == EtatFloater:
                #     lemming_clicked["etat"] = EtatFloater
                # elif action_button_etat[action_button_choose] == EtatBomber:
                #     lemming_clicked["etat"] = EtatBomber
                # elif action_button_etat[action_button_choose] == EtatMinerDiagonal:
                #     lemming_clicked["etat"] = EtatMinerDiagonal
                # elif action_button_etat[action_button_choose] == EtatMinerHorizontal:
                #     lemming_clicked["etat"] = EtatMinerHorizontal

        # Check if click is on the action bar
        if (
            x >= start_actions[0]
            and x <= start_actions[0] + nb_of_actions * size_of_actions
            and y >= start_actions[1]
            and y <= start_actions[1] + height_of_actions
        ):
            action_button_choose = (x - start_actions[0]) // size_of_actions
            # print("Action: ", action_button_etat[action_button_choose])
            click_sound.play()

    # ETAPE 1 : gestion des transitions

    for onelemming in lemmingsLIST:
        xx = onelemming["x"]
        yy = onelemming["y"]

        if is_on_exit(xx, yy, onelemming):
            lemmingsLIST.remove(onelemming)
            nb_lemmings_arrived += 1
            escaped_sound.play()
            continue

        pixel_under_lemming = check_if_lemming_can_fall(xx, yy, onelemming)
        
        if onelemming["etat"] == EtatDead:
            lemmingsLIST.remove(onelemming)
            
        if onelemming["etat"] == EtatStop:
            continue

        elif onelemming["etat"] == EtatChute or onelemming["etat"] == EtatFloater:
            if pixel_under_lemming != BLACK:
                if onelemming["fallcount"] > 100 and onelemming["etat"] == EtatChute:
                    onelemming["etat"] = EtatDead
                    #play the dead sound
                    die_sound.play()
                else:
                    onelemming["etat"] = EtatMarche
                    onelemming["fallcount"] = 0
        elif onelemming["etat"] == EtatMarche or onelemming["etat"] == EtatSpeeder:
            if pixel_under_lemming == BLACK:
                onelemming["etat"] = EtatChute
            if check_collision_lemming_stopped(
                onelemming
            ) or check_collision_lemming_wall(onelemming):
                # Changer de direction
                onelemming["vx"] = -onelemming["vx"]

        elif onelemming["etat"] == EtatMiner or onelemming["etat"] == EtatMinerHorizontal or onelemming["etat"] == EtatMinerDiagonal:
            if pixel_under_lemming == BLACK:
                onelemming["etat"] = EtatChute

        # ETAPE 2 : gestion des actions
        ActionToPerform[onelemming["etat"]](onelemming)

    # ETAPE 3 : affichage des lemmings
    for onelemming in lemmingsLIST:
        xx = onelemming["x"]
        yy = onelemming["y"]
        state = onelemming["etat"]
        random_decal = onelemming["decal"]
        dead_no_anim = onelemming["dead_no_anim"]
        if dead_no_anim:
            continue

        anim_to_use = [marche, tombe, dead, stop, miner, floater, bomber]
        if (onelemming["vx"]) == 1:
            anim_to_use = [
                marche_flipped,
                tombe_flipped,
                dead_flipped,
                stop_flipped,
                miner_flipped,
                floater_flipped,
                bomber_flipped,
            ]

        if state == EtatChute:
            screen.blit(anim_to_use[1][(time + random_decal) % len(tombe)], (xx, yy))
            onelemming["surface"] = anim_to_use[1][(time + random_decal) % len(tombe)]

        if state == EtatMarche:
            screen.blit(anim_to_use[0][(time + random_decal) % len(marche)], (xx, yy))
            onelemming["surface"] = anim_to_use[0][(time + random_decal) % len(marche)]

        if state == EtatDead:
            screen.blit(anim_to_use[2][(time) % len(dead)], (xx, yy))
            onelemming["surface"] = anim_to_use[2][(time) % len(dead)]
            if (time) % len(dead) == len(dead) - 1:
                onelemming["dead_no_anim"] = True

        if state == EtatStop:
            screen.blit(anim_to_use[3][(time + random_decal) % len(stop)], (xx, yy))
            onelemming["surface"] = anim_to_use[3][(time + random_decal) % len(stop)]

        if state == EtatMiner or state == EtatMinerHorizontal:
            screen.blit(anim_to_use[4][(time + random_decal) % len(miner)], (xx, yy))
            onelemming["surface"] = anim_to_use[4][(time + random_decal) % len(miner)]
            
        if state == EtatFloater:
            screen.blit(anim_to_use[5][(time + random_decal) % len(floater)], (xx, yy))
            onelemming["surface"] = anim_to_use[5][(time + random_decal) % len(floater)]
        if state == EtatMinerDiagonal:
            screen.blit(anim_to_use[4][(time + random_decal) % len(miner)], (xx, yy))
            onelemming["surface"] = anim_to_use[4][(time + random_decal) % len(miner)]
        if state == EtatBomber:
            screen.blit(anim_to_use[6][(time + random_decal) % len(bomber)], (xx, yy))
            onelemming["surface"] = anim_to_use[6][(time + random_decal) % len(bomber)]
            if (time + random_decal) % len(bomber) == len(bomber) - 1:
                onelemming["dead_no_anim"] = True
        if state == EtatSpeeder:
            screen.blit(anim_to_use[0][(time + random_decal) % len(marche)], (xx, yy))
            onelemming["surface"] = anim_to_use[0][(time + random_decal) % len(marche)]
        

        # sHOW HITBOX
        draw_hitbox(screen, onelemming)
        
    # Afficher les stats
    show_stats()
        
    # Check if all lemmings are gone or dead and if more than 2/3 of the lemmings have arrived
    if len(lemmingsLIST) == 0 and nb_lemmings_arrived > nb_lemmings * 2 / 3:
        font = pygame.font.Font(None, 100)
        text = font.render("WIN", True, (0, 255, 0))
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        screen.blit(text, text_rect)
        print("WIN. Vous avez gagné ! Fin du jeu.")
        pygame.display.flip()
        
        # play the win sound
        win_sound.play()
        sleep(5)  # Pause for 5 seconds before quitting
        done = True

    elif (len(lemmingsLIST) == 0 and compteur_creation > 0 and compteur_creation == nb_lemmings) or (pygame.time.get_ticks() / 1000) >= 120:
        font = pygame.font.Font(None, 100)
        text = font.render("LOOSE", True, (255, 0, 0))
        print("LOOSE. Vous avez perdu, fin du jeu.")
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        # play the loose sound
        loose_sound.play()
        sleep(5)
        done = True
        
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    draw_selected_state(screen, action_button_etat[action_button_choose] if action_button_choose is not None else "None")
    pygame.display.flip()

pygame.quit()