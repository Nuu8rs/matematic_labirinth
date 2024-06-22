import pygame
from loader import window
import time
from labirint import Labyrinth
from config import display, width, height, width_line, width_walls, border
from Entity import Player,WeekEnemy
from fight import Fight
import sys
import random

class Game:
    def __init__(self, 
                labyrinth: Labyrinth, 
                player: Player, 
                enemies: list[WeekEnemy]):
        
        self.labyrinth = labyrinth
        self.player = player
        self.enemies = enemies
        self.running = True
        self.trace = False
        self.start_time = time.time()
        self.record_time = 9999
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.player.handle_movement(event, self.labyrinth)
                if event.key == pygame.K_q:
                    self.toggle_trace()
                    
    def check_proximity(self):
        for enemy in self.enemies:
            if self.player.position == enemy.position:
                enemy.position = enemy.old_position.copy() 
                return True, "collision", enemy
            if (abs(self.player.position[0] - enemy.position[0]) + 
                abs(self.player.position[1] - enemy.position[1]) == 1 and
                not self.labyrinth.is_wall_between(self.player.position, enemy.position)):
                return True, "proximity", enemy
        return False, None, None

    def toggle_trace(self):
        self.trace = not self.trace


    def draw_game_info(self):
        font = pygame.font.Font(None, 25)
        heart_color = (255, 0, 0)
        empty_heart_color = (128, 128, 128)
        heart_width = 20
        heart_height = 15
        x_offset = 5
        y_offset = 5
        info_rect = pygame.Rect(0, window.get_height() - 70, display.width_window, 70)
        pygame.draw.rect(window, (0, 0, 0), info_rect)
        time_text = f"Час проходження лабіринту: {int(time.time() - self.start_time)}"
        text = font.render(time_text, True, (255, 255, 255))
        text_rect = text.get_rect(bottomleft=(5, info_rect.bottom - 5))  
        pygame.draw.rect(window, (0, 0, 0), text_rect) 
        window.blit(text, text_rect)
        for i in range(self.player.max_health):
            x = info_rect.right - (i + 1) * (heart_width + x_offset)
            y = info_rect.top + y_offset

            if i < self.player.health:
                color = heart_color
            else:
                color = empty_heart_color

            pygame.draw.polygon(window, color, [
                (x, y + heart_height // 2),
                (x + heart_width // 2, y + heart_height),
                (x + heart_width, y + heart_height // 2),
                (x + heart_width // 2, y)
            ])
    def update(self):
        if not self.player.is_alive:
            pygame.quit()
            sys.exit()
            return
        if self.player.moved:
            for enemy in self.enemies:
                enemy.move(self.labyrinth)
            self.player.moved = False
        is_near_or_collision, type_of_interaction, enemy = self.check_proximity()
        if is_near_or_collision:
            if type_of_interaction == "collision":
                print("Столкновение!")  
            elif type_of_interaction == "proximity":
                fight = Fight(
                    hero=self.player,
                    enemy=enemy
                ) 
                fight.start()
                print("FIGHT!")  
                
        for enemy in self.enemies:
            if not enemy.is_alive:
                self.enemies.remove(enemy)
                self.labyrinth.clear(window, enemy.position)
    
    def draw(self, window):
        self.labyrinth.clear(window, self.player.old_position) 
        for enemy in self.enemies:
            self.labyrinth.clear(window, enemy.old_position)  

        self.player.draw(window, self.labyrinth)
        for enemy in self.enemies:
            enemy.draw(window, self.labyrinth)

        self.draw_game_info()
        pygame.display.flip()  
        
    def run(self, window):
        self.labyrinth.draw(window)
        while self.running:
            self.handle_events()
            self.update()
            self.draw(window)
            pygame.display.flip()  

            
            
labyrinth = Labyrinth(width=width,height=height,width_line=width_line,width_walls=width_walls, border=border)
labyrinth.generate()

player = Player(list(labyrinth.start))

enemy_count = 5
enemies = []
for _ in range(enemy_count):
    while True:
        enemy_x = random.randint(0, width - 1)
        enemy_y = random.randint(0, height - 1)
        if labyrinth.transition_matrix[enemy_x][enemy_y]:
            enemies.append(WeekEnemy([enemy_x,enemy_y]))
            break   
enemies.append(WeekEnemy([player.position[0],player.position[1]]))

game = Game(labyrinth, player, enemies)
game.run(window)