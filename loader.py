import pygame
from config import display

pygame.init()
print(display.width_window)
window = pygame.display.set_mode((display.width_window, display.height_window))

pygame.display.set_caption("Лабіринт")
