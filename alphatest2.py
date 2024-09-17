import pygame
import random
import numpy as np
from scipy.stats import chi2_contingency

# Initialisation de Pygame
pygame.init()

# creation of a clock object:
clock = pygame.time.Clock()
# set the desired FPS / important pour l'affichage des rectangles
fps = 60

# Paramètres
# taille de la fenêtre totale
TOTAL_WINDOWS_WIDTH, TOTAL_WINDOWS_HEIGHT = 1350, 660

# taille de la fenêtre avec le quadrillage
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 660          # largeur et hauteur de la grille
RECT_WIDTH, RECT_HEIGHT = 15, 15                # modulo servant à créer les largeur et hauteur des carreaux en fonction
                                                # de la taille de WINDOW
                                                # 10 permet d'avoir 90 et 66 carreaux
                                                # 15 permet d'avoir 60 et 44 carreaux
                                                # 20 permet d'avoir 45 et 33 carreaux
                                                # 30 permet d'avoir 30 et 22 carreaux

# définition de la taille des rectangles:
rect_largeur = 5
rect_hauteur = 5

# extraction du modulo pour la largeur et la hauteur
RECTANGLE_WIDTH, RECTANGLE_HEIGHT = 0,0

# taille de la grille
GRID_WIDTH = WINDOW_WIDTH // RECT_WIDTH         # nombre de carreaux qu'on peut mettre dans WINDOW_WIDTH 60
GRID_HEIGHT = WINDOW_HEIGHT // RECT_HEIGHT      # nombre de carreaux qu'on peut mettre dans WINDOW_HEIGHT 44

# taille de la fenêtre permettant d'afficher les calculs
SECOND_WINDOW_WIDTH,SECOND_WINDOWS_HEIGHT = WINDOW_WIDTH / 2, WINDOW_HEIGHT

# Couleurs ==> définition de 8 couleurs
COLORS = [
    (0, 0, 0), # Noir
    (0, 0, 255),  # Bleu
    (255, 255, 0),  # Jaune
    (255, 0, 0),  # Rouge
    (0, 255, 0),  # Vert
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 128, 128),  # Gris
    (255, 128, 0)  # Orange
]


# définition du nombre de couleurs utilisées
nombre_de_couleurs = 2


# Création de la fenêtre
screen = pygame.display.set_mode((TOTAL_WINDOWS_WIDTH,TOTAL_WINDOWS_HEIGHT))
pygame.display.set_caption("Simulation alpha/beta")


# Fonction pour générer le quadrillage
"""
Génération d'une matrice de longueur GRID_WIDTH et largeur GRID_HEIGHT remplie de 
chiffres allant de 1 à numbre_de_couleurs.
"""
def generate_grid(num_colors):
    return [[random.randint(1, num_colors) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Génération des coordonnées d'un rectangle depuis des coordonnées spatiales sur WINDOWS:
"""
Cette fonction permet de générer aléatoirement la coordonnée supérieure gauche d'un rectangle 
ainsi que sa taille (largeur x hauteur) en nombre de carreaux
"""
def generate_rect_coords(largeur, hauteur):
    taille = [largeur, hauteur]
    angle_sg = [random.randint(0,GRID_WIDTH-largeur), random.randint(0,GRID_HEIGHT-hauteur)]
    return [angle_sg,taille]


# Fonction pour dessiner le quadrillage
"""
Dessine de la grille avec Pygame où pour une matrice grid donnée, on extrait une colonne y et une ligne row
On extrait ensuite de cette ligne un index de ligne et une valeur dans la matrice correspondant à une couleur.
On assigne ensuite pour chaque valeur de la grille une couleur associée avec la liste COLORS.
La grille est un rectancle 
"""
def draw_grid(grid):
    for y, row in enumerate(grid):
        for x, color_index in enumerate(row):
            pygame.draw.rect(screen, COLORS[color_index], (x * RECT_WIDTH, y * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT))


# Fonction pour dessiner les grands rectangles avec pygame
"""
Fonction qui génère les rectangles noires permettant de délimiter des zones de quadrillage dans lequel il va falloir compter
width est l'épaisseur du dessin et color sa couleur (par défaut noire)
"""
def draw_large_rectangles(rect1, rect2):
    pygame.draw.rect(screen, (0, 0, 0), rect1, 5)
    pygame.draw.rect(screen, (0, 0, 0), rect2, 5)


# Fonction pour compter les couleurs dans un rectangle

def count_colors(grid, rect, num_colors):
    # print("matrice: ", len(grid), "x", len(grid[0]))
    # print("x, y, w ,h du rectangle:", rect)
    # print("nb de couleur:", num_colors)
    x, y  = rect[0]
    w, h =  rect[1]
    counts = [0] * num_colors # définit une liste correspondant au nombre de couleurs utilisées
    # rint("vérification du nombre d'éléments dans la liste counts: ", counts)
    # print("valeurs de GRID_HEIGHT et GRID_WIDTH: ", len(grid), len(grid[0]))
    for i in range(y, y + h): # colonnes
        for j in range(x, x + w): # lignes
            if 0 <= i < len(grid) and 0 <= j < len(grid[i]):
#                print("grid[i][j]): ", grid[i][j]-1)
                counts[grid[i][j]-1] += 1
    return counts


# Fonction pour effectuer le test du chi2
def perform_chi2_test(counts1, counts2):
    """
    Cette fonction permet de prendre les counts des cases colorées de la fonction count_colors pour effectuer
    un test de chi2 et objectiver ainsi le risque alpha à force d'échantillonnage.
    :param counts1: compte du rectangle 1
    :param counts2: compte du rectangle 2
    :return: p-value du test effectué
    """
    # chi2_contingency est une fonction qui permet de travailler à partir d'un tableau de contingence
    # Préparation du tableau de contingence
    observed = np.array([counts1, counts2])
    # Ajouter une petite valeur à chaque cellule pour éviter les zéros
    observed = observed + 0.00001
    try:
        chi2, p_value, dof, expected = chi2_contingency(observed)
        return p_value
    except ValueError:
        return None

# définition de la fonction pause
def pauseMenu(self):
    if self.pause == True:
        self.pause = False
    elif self.pause == False:
        self.pause = True


# Boucle principale
def main():
    num_colors = nombre_de_couleurs  # Nombre de couleurs à utiliser
    grid = generate_grid(num_colors) # Génération d'une grille avec un certain nombre de couleurs
    p_value_list = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
 #               if event.key == pygame.K_p:
 #                   pauseMenu()
                if event.key == pygame.K_SPACE:
                    p_value_list = []
                    grid = generate_grid(num_colors)

        screen.fill((0, 0, 0))

        draw_grid(grid)
        # définition de 2 rectangles aléatoirement de largeur x et hauteur y en nombre de carreaux
        rect_coord1 = generate_rect_coords(rect_largeur, rect_hauteur)
        rect_coord2 = generate_rect_coords(rect_largeur, rect_hauteur)
        # x, y, w, h pour la fonction Rect de Pygame
        rect1 = pygame.Rect(rect_coord1[0][0] * RECT_WIDTH, rect_coord1[0][1] * RECT_HEIGHT,
                            rect_coord1[1][0] * RECT_WIDTH, rect_coord1[1][1] * RECT_HEIGHT)
        rect2 = pygame.Rect(rect_coord2[0][0] * RECT_WIDTH, rect_coord2[0][1] * RECT_HEIGHT,
                            rect_coord2[1][0] * RECT_WIDTH, rect_coord2[1][1] * RECT_HEIGHT)
        # rect2 = pygame.Rect(420, 360, 300, 210)

        draw_large_rectangles(rect1, rect2)


        counts1 = count_colors(grid, rect_coord1, num_colors)
        counts2 = count_colors(grid, rect_coord2, num_colors)
        p_value = perform_chi2_test(counts1, counts2)
        p_value_list = np.append(p_value_list, p_value)
        # p_value_list.append(p_value)
        p_value_list_100der = p_value_list[-100:]

        # écriture de p_value en haut au centre
        pvalue_text = pygame.font.Font(None, 36)
        if p_value is not None:
            text = pvalue_text.render(f"p-value: {p_value:.4f}", True, (255, 255, 255))
        else:
            text = pvalue_text.render("p-value: N/A", True, (255, 255, 255))
        screen.blit(text, (1050, 25))


        # écriture d'une croix avec des couleurs différentes en fonction des p-values calculées
        for p_value in enumerate(p_value_list_100der):
            # initialisation du Font pygame
            list_de_x = pygame.font.Font(None, 54)
            p_index = p_value[0]

            # définition des coordonnées relatives (x,y) du X:
            X_coordX = p_index % 10         # modulo 10 car envie de 10 X par ligne
            X_coordY = p_index // 10        # nb de division par le modulo pour définir la hauteur

            _coordX = 962 + 35 * X_coordX
            _coordY = 75 + 54 * X_coordY


            # définition du X qui change de couleur en fonction du résultat de la p-value
            if float(p_value[1]) > 0.10:
                __text_x = list_de_x.render(f"x", True, (0,255,0))     # Vert
            if 0.05 < float(p_value[1]) <= 0.10:
                __text_x = list_de_x.render(f"x", True, (255,128,0))   # Orange
            if float(p_value[1]) <= 0.05:
                __text_x = list_de_x.render(f"x", True, (255,0,0))     # Rouge
            screen.blit(__text_x, (_coordX, _coordY))

        ## Ecriture en bas des comptes des échantillons < 0.05, entre 0.05 et 0.10 et > 0.10
        # initialisation du Font pygame
        vert_count_pyg = pygame.font.Font(None, 24)
        orange_count_pyg = pygame.font.Font(None, 24)
        rouge_count_pyg = pygame.font.Font(None, 24)

        # définition des coordonnées relatives (x,y) du X:
        _coordX_vert = 950
        _coordX_orange = 1100
        _coordX_rouge = 1250
        _coordY_counts = 625

        # calcul des counts:
        _count_vert = sum(p_value_list > 0.10)
        _count_rouge = sum(p_value_list <= 0.05)
        _count_orange = len(p_value_list) - _count_vert - _count_rouge

        # définition des textes
        text_vert = vert_count_pyg.render(f"{_count_vert} : {_count_vert/len(p_value_list)*100:2.1f}%", True, (0,255,0))     # Vert
        text_orange = orange_count_pyg.render(f"{_count_orange}: {_count_orange/len(p_value_list)*100:2.1f}%", True, (255,128,0))   # Orange
        text_rouge = rouge_count_pyg.render(f"{_count_rouge} : {_count_rouge/len(p_value_list)*100:2.1f}%", True, (255,0,0))     # Rouge

        # affichage des textes
        screen.blit(text_vert, (_coordX_vert, _coordY_counts))
        screen.blit(text_orange, (_coordX_orange, _coordY_counts))
        screen.blit(text_rouge, (_coordX_rouge, _coordY_counts))
        """
        # écriture des x colorés pour la liste de p_value
        font2 = pygame.font.Font(None, 54)
        
        
        for i in range(len(p_value_list), len(p_value_list)-1):
            if i is not None:
                if i > 0.10 :
                    __text = font.render(f"X", True, (0,255,0))
                if 0.05 < i <= 0.10:
                    __text = font.render(f"X", True, (255,128,0))
                else:
                    __text = font.render(f"X", True, (255,0,0))
            else: pass
        screen.blit(__text, (1050, 300))
        """

        pygame.display.flip()

        # limits the FPS by sleeping for the remainder of the frame
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()