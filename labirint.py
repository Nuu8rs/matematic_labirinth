import pygame
import random
from utils import start_point_generate, finish_point_generate, transition_choice
from config import color_finish, color_start, color_wall

class Labyrinth:
    def __init__(self, width, height, width_line, width_walls, border,
                 color_way=(255, 255, 255), color_wall=(0, 0, 0),
                 color_start=(0, 255, 0), color_finish=(255, 0, 0)):

        self.width = width
        self.height = height
        self.width_line = width_line
        self.width_walls = width_walls
        self.border = border
        self.colors = {
            "way": color_way,
            "wall": color_wall,
            "start": color_start,
            "finish": color_finish
        }
        self.reach_matrix = []
        self.transition_matrix = []
        self.wall_image = pygame.image.load("static/back_plate_1.png")
        self.wall_image_resized = pygame.transform.scale(self.wall_image, (width_line, width_line))

    def generate(self):
        n, m = self.width, self.height 
        for i in range(n):
            self.reach_matrix.append([])  
            for j in range(m):
                self.reach_matrix[i].append(False) 
        for i in range(n * 2 - 1):
            self.transition_matrix.append([])
            for j in range(m * 2 - 1):
                if i % 2 == 0 and j % 2 == 0: 
                    self.transition_matrix[i].append(True) 
                else:
                    self.transition_matrix[i].append(False)
        self.start = start_point_generate(n, m)  
        self.finish = finish_point_generate(self.start, n, m) 

        list_transition = [self.start]

        x, y = self.start  


        self.reach_matrix[x][y] = True  


        x, y, tx, ty = transition_choice(x, y, self.reach_matrix)

        # Основний цикл генерації лабіринту
        for i in range(1, m * n):  
            # Повернення до попередньої клітинки, якщо поточна недосяжна
            while not (x >= 0 and y >= 0):  
                x, y = list_transition[-1]  
                list_transition.pop()  
                x, y, tx, ty = transition_choice(x, y, self.reach_matrix)

            # Відмітка поточної клітинки як досяжної
            self.reach_matrix[x][y] = True  

            # Додавання поточної клітинки до списку переходів
            list_transition.append((x, y))  

            # Видалення стінки (створення переходу)
            self.transition_matrix[tx][ty] = True  

            # Вибір наступного переходу
            x, y, tx, ty = transition_choice(x, y, self.reach_matrix) 

    def is_wall_between(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        dx = x2 - x1
        dy = y2 - y1

        if dx == 1: 
            return not self.transition_matrix[x1 * 2 + 1][y1 * 2]  
        elif dx == -1:  
            return not self.transition_matrix[x1 * 2 - 1][y1 * 2]
        elif dy == 1: 
            return not self.transition_matrix[x1 * 2][y1 * 2 + 1]
        elif dy == -1:  
            return not self.transition_matrix[x1 * 2][y1 * 2 - 1]
        else:
            return False  

    
    
        
    def draw(self, window):
        for i in range(len(self.transition_matrix)):
            for j in range(len(self.transition_matrix[0])):
                x = self.border + (i // 2) * (self.width_line + self.width_walls) + (i % 2) * self.width_line
                y = self.border + (j // 2) * (self.width_line + self.width_walls) + (j % 2) * self.width_line
                if self.transition_matrix[i][j] == 1:
                    window.blit(self.wall_image_resized, (x, y))
                else:
                    pygame.draw.rect(window, color_wall, (x, y, self.width_line, self.width_line))
                    
        pygame.draw.rect(window, color_start, (
            self.border + self.start[0] * (self.width_line + self.width_walls), self.border + self.start[1] * (self.width_line + self.width_walls), self.width_line,
            self.width_line))
        pygame.draw.rect(window, color_finish, (
            self.border + self.finish[0] * (self.width_line + self.width_walls), self.border + self.finish[1] * (self.width_line + self.width_walls), self.width_line,
            self.width_line))

       
    def clear(self, window, entity_position: list[int, int], background_color=(0, 0, 0)):
        """Очищает ячейку, на которой находится сущность."""
        x = self.border + entity_position[0] * (self.width_line + self.width_walls)
        y = self.border + entity_position[1] * (self.width_line + self.width_walls)

        # Проверяем, является ли ячейка путем или стеной
        if self.transition_matrix[entity_position[0] * 2][entity_position[1] * 2]:
            window.blit(self.wall_image_resized, (x, y))  # Если стена, рисуем стену
        else:
            pygame.draw.rect(window, background_color, (x, y, self.width_line, self.width_line))  # Если путь, заливаем цветом фона
    