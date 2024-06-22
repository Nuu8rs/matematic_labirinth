import pygame
from pygame.locals import *
from typing import Tuple
import random
from config import display
import operator

class Fight:
    def __init__(self, hero, enemy):
        # Ініціалізація бою: встановлення учасників, екрану, шрифтів та кольорів
        self.hero = hero
        self.enemy = enemy
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.SysFont(None, 48)
        self.input_font = pygame.font.SysFont(None, 36)
        self.timer_font = pygame.font.SysFont(None, 24)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')

        # Завантаження та масштабування фонового зображення
        self.background_image = pygame.image.load("static/back_fight2.png")
        self.background_image = pygame.transform.scale(self.background_image, (display.width_window, display.height_window))

        # Генерація першого питання
        self.generate_question()

    def start(self):
        # Збереження копії початкового екрану та встановлення режиму відображення
        self.original_screen = self.screen.copy()
        pygame.display.set_mode((display.width_window, display.height_window))
        
        # Запуск основного циклу бою
        self.fight_loop()
        
        # Відновлення початкового екрану після завершення бою
        self.screen.blit(self.original_screen, (0, 0)) 
        pygame.display.flip()

    def generate_question(self):
        # Генерація випадкового питання для бою
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 40)

        # Вибір випадкової арифметичної операції та відповідної функції
        operations = {
            "+": operator.add,
            "-": operator.sub,
        }
        operation_symbol = random.choice(list(operations.keys()))
        operation_func = operations[operation_symbol]
        correct_answer = operation_func(num1, num2)

        self.question = f"Скільки буде {num1} {operation_symbol} {num2}?"
        self.correct_answer = str(correct_answer)

    def fight_loop(self):
        # Основний цикл бою: триває, поки обидва учасники живі
        while self.hero.is_alive and self.enemy.is_alive:
            # Отрисовка фону на початку кожного циклу
            self.screen.blit(self.background_image, (0, 0))

            # Створення та відображення спливаючого вікна з питанням
            self.popup = Popup(self)
            self.popup.display() 

            # Перевірка умови завершення бою (поразка героя)
            if not self.hero.is_alive:
                self.show_end_message(False)
                break
            # Перевірка умови завершення бою (перемога героя)
            if not self.enemy.is_alive:
                self.show_end_message(True)
                break

            # Генерація нового питання для наступного раунду
            self.generate_question() 

    def show_end_message(self, status:bool):
        # Відображення повідомлення про завершення бою (перемога або поразка)
        if status:
            victory_image = pygame.image.load("static/victory_popup.jpg")
            victory_image = pygame.transform.scale(victory_image, (display.width_window, display.height_window))
            self.screen.blit(victory_image, (0, 0)) 

        pygame.display.flip()
        pygame.time.wait(1500)

class Popup:
    def __init__(self, fight):
        self.fight = fight
        panel_width = 400 
        panel_height = 90  
        print(self.fight.screen.get_width())
        print(self.fight.screen.get_height())
        panel_x = (self.fight.screen.get_width() - panel_width) // 2
        panel_y = 680  
        self.input_box = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        self.active = False
        self.text_input = ''
        self.time_remaining = 6
        self.clock = pygame.time.Clock()
        self.answered = False
        
    def display(self):
        """Відображає спливаюче вікно з питанням та обробляє відповідь гравця."""

        # Цикл триває, поки залишається час і гравець не відповів
        while self.time_remaining > 0 and not self.answered:  
            self.handle_events()  # Обробляємо події (натискання клавіш, тощо)

            # Оновлюємо таймер, якщо відповідь ще не дана
            if not self.answered:
                self.time_remaining -= self.clock.tick(60) / 1000  # Віднімаємо час, що минув

            # Оновлюємо вміст екрану (питання, таймер, здоров'я)
            self.update_screen()

            # Якщо герой помер під час відповіді, виходимо з циклу
            if not self.fight.hero.is_alive:
                return

        # Якщо час вийшов, а гравець не відповів, герой отримує пошкодження
        if not self.answered:
            self.fight.hero.health -= 1 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONDOWN:
                self.active = True

            if event.type == KEYDOWN:
                    if event.key == K_RETURN: 
                        if self.text_input == self.fight.correct_answer:
                            self.fight.enemy.health -= 1  
                        else:
                            self.fight.hero.health -= 1
                        self.answered = True  
              
                    elif event.key == K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    else:
                        self.text_input += event.unicode

    def update_screen(self):
        color = self.fight.color_active if self.active else self.fight.color_inactive
        popup = pygame.Surface((self.fight.screen.get_width(), self.fight.screen.get_height()), pygame.SRCALPHA)
        question_text = self.fight.font.render(self.fight.question, True, (255, 0, 0))
        question_rect = question_text.get_rect(center=((self.fight.screen.get_width() // 2), (self.fight.screen.get_height() // 4 )+ 15))
        popup.blit(question_text, question_rect)


        timer_rect = self.fight.timer_font.render(f"Час на відповідь: {round(self.time_remaining, 1)} с", True, (0, 0, 0, 0)).get_rect() 
        timer_rect.topright = (self.fight.screen.get_width() - 10, 10)
        popup.blit(self.fight.background_image, timer_rect, timer_rect) 

        timer_text = self.fight.timer_font.render(f"Час на відповідь: {round(self.time_remaining, 1)} с", True, (255, 255, 255)) 
        popup.blit(timer_text, (self.fight.screen.get_width() - timer_text.get_width() - 10, 10))


        self.draw_health_bars(popup)


        self.fight.screen.blit(popup, (0, 0))  
        pygame.display.flip()

    def draw_health_bars(self, popup):
        self.heart_width = 20  
        self.heart_spacing = 5  
        self.x_offset = 50  
        self.y_offset = 50  
        total_width = self.fight.hero.max_health * (self.heart_width + self.heart_spacing) - self.heart_spacing  
        start_x = self.x_offset + (200 - total_width) // 2 
        for i in range(self.fight.hero.max_health):
            x = start_x + i * (self.heart_width + self.heart_spacing)  
            color = (255, 0, 0) if i < self.fight.hero.health else (128, 128, 128)
            self.draw_heart(popup, x, self.y_offset, color)
        if self.fight.enemy:
            start_x = self.x_offset + 500 + (200 - total_width) // 2 
            for i in range(self.fight.enemy.max_health):
                x = start_x + i * (self.heart_width + self.heart_spacing)
                color = (255, 0, 0) if i < self.fight.enemy.health else (128, 128, 128)
                self.draw_heart(popup, x, self.y_offset, color)
                
    def draw_heart(self, surface, x, y, color):
        points = [
            (x + self.heart_width // 2, y + self.heart_width // 4),
            (x + self.heart_width, y),
            (x + self.heart_width * 3 // 2, y + self.heart_width // 4),
            (x + self.heart_width, y + self.heart_width // 2),
            (x + self.heart_width // 2, y + self.heart_width),
            (x, y + self.heart_width // 2),
        ]
        pygame.draw.polygon(surface, color, points) 