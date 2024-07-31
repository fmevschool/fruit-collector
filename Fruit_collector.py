import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre du jeu
largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Évite les Bombes et Ramasse les Fruits")

# Définition des couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Chargement des images
image_joueur = pygame.image.load('images/joueur.png')
image_bombe = pygame.image.load('images/bombe.png')
image_fruit = pygame.image.load('images/fruit.png')

# Chargement des sons
son_collision = pygame.mixer.Sound('sons/collision.wav')
son_collecte = pygame.mixer.Sound('sons/collecte.wav')
pygame.mixer.music.load('sons/musique_fond.mp3')
pygame.mixer.music.play(-1)  # Lecture en boucle

# Initialisation des variables du jeu
position_joueur = [largeur_fenetre // 2, hauteur_fenetre - 60]
vitesse_joueur = 5
bombes = []
fruits = []
score = 0

# Fonction pour créer une nouvelle bombe
def ajouter_bombe():
    x = random.randint(0, largeur_fenetre - image_bombe.get_width())
    y = 0  # Les bombes apparaissent au sommet de l'écran
    bombes.append([x, y])

# Fonction pour mettre à jour et afficher les bombes
def afficher_bombes():
    global score
    for bombe in bombes:
        fenetre.blit(image_bombe, bombe)  # Dessine chaque bombe à sa position actuelle
        bombe[1] += 5  # Déplace la bombe vers le bas
        if bombe[1] > hauteur_fenetre:  # Supprime la bombe si elle sort de l'écran
            bombes.remove(bombe)
            # End of game logic or handling can be added here
            if verifier_collision_bombes():
                print("Game Over! Score: ", score)
                pygame.quit()
                exit()

# Fonction pour créer un nouveau fruit
def ajouter_fruit():
    x = random.randint(0, largeur_fenetre - image_fruit.get_width())
    y = 0  # Les fruits apparaissent au sommet de l'écran
    fruits.append([x, y])

# Fonction pour mettre à jour et afficher les fruits
def afficher_fruits():
    global score
    for fruit in fruits:
        fenetre.blit(image_fruit, fruit)  # Dessine chaque fruit à sa position actuelle
        fruit[1] += 5  # Déplace le fruit vers le bas
        if fruit[1] > hauteur_fenetre:  # Supprime le fruit s'il sort de l'écran
            fruits.remove(fruit)

# Fonction pour vérifier les collisions entre le joueur et les bombes
def verifier_collision_bombes():
    global score
    for bombe in bombes:
        if (position_joueur[0] < bombe[0] + image_bombe.get_width() and
            position_joueur[0] + image_joueur.get_width() > bombe[0] and
            position_joueur[1] < bombe[1] + image_bombe.get_height() and
            position_joueur[1] + image_joueur.get_height() > bombe[1]):
            # Collision détectée
            son_collision.play()  # Joue le son de collision
            bombes.remove(bombe)  # Supprime la bombe
            return True  # Indique qu'une collision a eu lieu
    return False

# Fonction pour vérifier les collisions entre le joueur et les fruits
def verifier_collecte_fruits():
    global score
    for fruit in fruits:
        if (position_joueur[0] < fruit[0] + image_fruit.get_width() and
            position_joueur[0] + image_joueur.get_width() > fruit[0] and
            position_joueur[1] < fruit[1] + image_fruit.get_height() and
            position_joueur[1] + image_joueur.get_height() > fruit[1]):
            # Fruit collecté
            son_collecte.play()  # Joue le son de collecte
            fruits.remove(fruit)  # Supprime le fruit
            score += 1  # Augmente le score

# Boucle principale du jeu
clock = pygame.time.Clock()
en_cours = True

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # Gestion des mouvements du joueur
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        position_joueur[0] -= vitesse_joueur
        if position_joueur[0] < 0:
            position_joueur[0] = 0
    if touches[pygame.K_RIGHT]:
        position_joueur[0] += vitesse_joueur
        if position_joueur[0] > largeur_fenetre - image_joueur.get_width():
            position_joueur[0] = largeur_fenetre - image_joueur.get_width()

    # Ajout de bombes et de fruits
    if random.randint(1, 20) == 1:
        ajouter_bombe()
    if random.randint(1, 20) == 1:
        ajouter_fruit()

    # Mise à jour des positions des bombes et des fruits
    afficher_bombes()
    afficher_fruits()

    # Vérification des collisions et des collectes
    if verifier_collision_bombes():
        print("Game Over! Score: ", score)
        pygame.quit()
        exit()

    verifier_collecte_fruits()

    # Mise à jour de l'écran
    fenetre.fill(blanc)  # Efface l'écran en le remplissant de blanc
    fenetre.blit(image_joueur, position_joueur)  # Dessine l'image du joueur à sa position actuelle
    afficher_bombes()
    afficher_fruits()

    # Affichage du score
    font = pygame.font.Font(None, 36)
    texte_score = font.render(f"Score: {score}", True, noir)
    fenetre.blit(texte_score, (10, 10))

    # Rafraîchir l'affichage
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
