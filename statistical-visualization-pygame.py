import pygame
import random
import numpy as np
from scipy.stats import chi2_contingency



# Initialisation de Pygame
pygame.init()

# Paramètres
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
RECT_WIDTH, RECT_HEIGHT = 10, 10
GRID_WIDTH = WINDOW_WIDTH // RECT_WIDTH
GRID_HEIGHT = WINDOW_HEIGHT // RECT_HEIGHT

# Couleurs
COLORS = [
    (255, 0, 0),    # Rouge
    (0, 255, 0),    # Vert
    (0, 0, 255),    # Bleu
    (255, 255, 0),  # Jaune
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 128, 128),# Gris
    (255, 128, 0)   # Orange
]

# Création de la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Visualisation statistique")

# Fonction pour générer le quadrillage
def generate_grid(num_colors):
    return [[random.randint(0, num_colors-1) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Fonction pour dessiner le quadrillage
def draw_grid(grid):
    for y, row in enumerate(grid):
        for x, color_index in enumerate(row):
            pygame.draw.rect(screen, COLORS[color_index], (x*RECT_WIDTH, y*RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT))

# Fonction pour dessiner les grands rectangles
def draw_large_rectangles(rect1, rect2):
    pygame.draw.rect(screen, (255, 255, 255), rect1, 2)
    pygame.draw.rect(screen, (255, 255, 255), rect2, 2)

# Fonction pour compter les couleurs dans un rectangle
def count_colors(grid, rect, num_colors):
    x, y, w, h = rect
    counts = [0] * num_colors
    for i in range(y, y+h):
        for j in range(x, x+w):
            if 0 <= i < GRID_HEIGHT and 0 <= j < GRID_WIDTH:
                counts[grid[i][j]] += 1
    return counts

# Fonction pour effectuer le test du chi2
def perform_chi2_test(counts1, counts2):
    observed = np.array([counts1, counts2])
    chi2, p_value, dof, expected = chi2_contingency(observed)
    return p_value

# Boucle principale
def main():
    num_colors = 4  # Nombre de couleurs à utiliser
    grid = generate_grid(num_colors)
    rect1 = pygame.Rect(50, 50, 300, 200)
    rect2 = pygame.Rect(450, 350, 300, 200)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid = generate_grid(num_colors)
        
        screen.fill((0, 0, 0))
        draw_grid(grid)
        draw_large_rectangles(rect1, rect2)
        
        counts1 = count_colors(grid, rect1, num_colors)
        counts2 = count_colors(grid, rect2, num_colors)
        p_value = perform_chi2_test(counts1, counts2)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"p-value: {p_value:.4f}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
