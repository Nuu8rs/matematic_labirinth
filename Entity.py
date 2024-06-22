from pygame import image, transform
from config import width_line
from labirint import Labyrinth
from abc import ABC
import pygame
import random

class EntityObject(ABC):
    path_to_image:image
    max_health:int
    health:int

    def __init__(self, position:list[int,int]) -> None:
        self.position = position
        self.image = image.load(self.path_to_image)
        self.image_resize = transform.scale(self.image, (width_line,width_line))
        self.old_position = self.position.copy()

    @property
    def is_alive(self):
        return self.health > 0
        
    def draw(self, window, labyrinth:Labyrinth):
        x = labyrinth.border + self.position[0] * (labyrinth.width_line + labyrinth.width_walls) + labyrinth.width_line // 2 - self.image_resize.get_width() // 2
        y = labyrinth.border + self.position[1] * (labyrinth.width_line + labyrinth.width_walls) + labyrinth.width_line // 2 - self.image_resize.get_height() // 2

        window.blit(self.image_resize, (x, y))
           

    
class WeekEnemy(EntityObject):
    max_health = 3
    health = 3
    
    path_to_image = "static/week_enemy.png"
    
    def __init__(self, position: list[int]) -> None:
        super().__init__(position)

    def move(self, labyrinth):
        x, y = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

        random.shuffle(directions) 

        for dx, dy in directions:  
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < labyrinth.width and 0 <= new_y < labyrinth.height and
                    labyrinth.transition_matrix[new_x * 2][new_y * 2] and  
                    labyrinth.transition_matrix[x * 2 + dx][y * 2 + dy]):  
                self.old_position = self.position.copy()  
                self.position[0] += dx 
                self.position[1] += dy
                return  
        
class Player(EntityObject):
    max_health = 5         # Максимальний запас здоров'я гравця
    health = 5             # Поточне здоров'я гравця
    path_to_image = "static/hero-image.jpeg"  # Шлях до зображення героя
    moved = False          # Чи гравець зробив хід під час поточного оновлення

    def __init__(self, position: list[int]) -> None:
        super().__init__(position)  # Ініціалізуємо батьківський клас (EntityObject)

    def handle_movement(self, event, labyrinth):
        """Обробляє рух гравця на основі натискань клавіш."""

        dx, dy = 0, 0  # Зміни по осі X та Y (спочатку руху немає)

        # Визначаємо напрямок руху залежно від натиснутої клавіші
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            dx = 1   # Рух вправо
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            dx = -1  # Рух вліво
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            dy = 1   # Рух вниз
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            dy = -1  # Рух вгору

        # Розраховуємо нові координати в матриці переходів лабіринту
        new_x, new_y = self.position[0] * 2 + dx, self.position[1] * 2 + dy

        # Перевіряємо, чи можна переміститися на нові координати:
        # 1. Чи не виходять вони за межі лабіринту
        # 2. Чи є прохід (True) у матриці переходів на нових координатах
        if (0 <= new_x < len(labyrinth.transition_matrix) and 
            0 <= new_y < len(labyrinth.transition_matrix[0]) and
            labyrinth.transition_matrix[new_x][new_y]):
            
            self.old_position = self.position.copy()  # Зберігаємо попередню позицію ПЕРЕД оновленням
            self.position[0] += dx  # Оновлюємо позицію гравця
            self.position[1] += dy
            self.moved = True       # Позначаємо, що гравець зробив хід
        else:
            self.moved = False      # Гравець не зміг зробити хід
