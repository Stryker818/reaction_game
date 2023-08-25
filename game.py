# Імпортуємо необхідні бібліотеки
import pygame
import sys
import random
import time
import pygame.mixer
from settings import sound_enabled

pygame.mixer.init()

neon_colors = [
    (255, 0, 0),  # Червоний
    (255, 165, 0),  # Оранжевий
    (255, 255, 0),  # Жовтий
    (0, 255, 0),  # Зелений
    (0, 0, 255),  # Синій
    (75, 0, 130),  # Індиго
    (238, 130, 238),  # Фіолетовий
]


# Функція, яка визначає параметри кругів в залежності від обраного рівня складності
def random_properties(selected_difficulty):
    if selected_difficulty == "1":
        circle_color = (0, 255, 0)  # Зеленый цвет
        circle_radius = 30
        num_circles_to_pop = 10
    elif selected_difficulty == "2":
        circle_color = (255, 255, 0)  # Желтый цвет
        circle_radius = 25
        num_circles_to_pop = 15
    elif selected_difficulty == "3":
        circle_color = (255, 0, 0)  # Красный цвет
        circle_radius = 20
        num_circles_to_pop = 20
    elif selected_difficulty == "4":
        circle_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        circle_radius = 15
        num_circles_to_pop = 9999  # Песочница - нет ограничения по кругам
    return circle_color, circle_radius, num_circles_to_pop


# Основна функція для гри
def run_game(selected_difficulty, sound_enabled, music_enabled):
    # Ініціалізація Pygame та створення вікна гри
    pygame.init()
    game_window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Реакційна гра")

    # Ініціалізація звуків
    sound_file1 = "popal.ogg"
    sound_file2 = "ne_popal.ogg"
    pygame.mixer.init()
    sound_file1 = pygame.mixer.Sound(sound_file1)
    sound_file2 = pygame.mixer.Sound(sound_file2)
    sound_file1.set_volume(0.2)
    pygame.mixer.music.set_volume(0.5)

    if sound_enabled:
        music_game = pygame.mixer.music.set_volume(1.0)
        sound_file1.set_volume(0.2)
        sound_file2.set_volume(1.0)
        pygame.mixer.music.set_volume(0.5)
    else:
        sound_file1.set_volume(0.0)
        sound_file2.set_volume(0.0)
        pygame.mixer.music.set_volume(0.0)

    # Відтворення музики при запуску гри
    pygame.mixer.music.play(-1)  # -1 означає безкінечне відтворення

    # Налаштування шрифту
    font = pygame.font.Font(None, 30)

    # Генерація випадкової позиції для круга
    def random_position(circle_radius):
        return random.randint(circle_radius, 800 - circle_radius), random.randint(
            circle_radius, 600 - circle_radius
        )

    # Ініціалізація параметрів для круга
    circle_color, circle_radius, num_circles_to_pop = 0, 0, 0
    circle_x, circle_y = 0, 0

    goal_reached_time = None

    while True:
        if selected_difficulty == "0":
            break

        # Отримання параметрів круга залежно від обраного рівня складності
        circle_color, circle_radius, num_circles_to_pop = random_properties(
            selected_difficulty
        )
        circle_x, circle_y = random_position(circle_radius)

        random_color = random.choice(neon_colors)
        goal_reached = False
        score = 0
        start_time = time.time()
        num_total_clicks = 0
        num_hits = 0
        num_misses = 0

        while not goal_reached:
            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Натискання пробілу під час гри
                        pygame.mixer.music.stop()
                        return  # Повернення до головного меню
                    if event.key == pygame.K_c:
                        goal_reached = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    num_total_clicks += 1
                    if sound_enabled:  # Використовуйте глобальну змінну sound_enabled
                        sound_file1.play()
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    distance = (
                        (mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2
                    ) ** 0.5
                    if distance < circle_radius:
                        sound_file1.play()
                        circle_x, circle_y = random_position(circle_radius)
                        score += 1
                        num_hits += 1

                        if score >= num_circles_to_pop:
                            goal_reached = True
                            end_time = time.time()
                            elapsed_time = round(end_time - start_time, 2)
                            goal_reached_time = elapsed_time
                    else:
                        sound_file2.play()
                        num_misses += 1

                    if selected_difficulty == "4":
                        circle_color = (
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255),
                        )
                        circle_x, circle_y = random_position(circle_radius)
                        score += 1
                        if score >= num_circles_to_pop:
                            goal_reached = True
                            end_time = time.time()
                            elapsed_time = round(end_time - start_time, 2)
                            goal_reached_time = elapsed_time

            # Оновлення графіки на екрані
            game_window.fill((255, 255, 255))
            pygame.draw.circle(
                game_window, circle_color, (circle_x, circle_y), circle_radius
            )

            score_text = font.render(
                f"Рахунок: {score} / {num_circles_to_pop}", True, (0, 0, 0)
            )
            game_window.blit(score_text, (600, 10))

            if goal_reached:
                time_text1 = font.render(
                    f"Гра пройдена за {goal_reached_time} сек.",
                    True,
                    (0, 0, 0),
                )
                time_text2 = font.render(
                    f"Space для повторення гри",
                    True,
                    (0, 0, 0),
                )
                time_text3 = font.render(
                    f"Esc для повернення в Головне меню",
                    True,
                    (0, 0, 0),
                )
                time_text_rect1 = time_text1.get_rect(center=(150, 525))
                time_text_rect2 = time_text1.get_rect(center=(150, 550))
                time_text_rect3 = time_text1.get_rect(center=(150, 575))
                game_window.blit(time_text1, time_text_rect1)
                game_window.blit(time_text2, time_text_rect2)
                game_window.blit(time_text3, time_text_rect3)

                hits_text = font.render(f"Попадань: {num_hits}", True, (0, 0, 0))
                misses_text = font.render(f"Промахів: {num_misses}", True, (0, 0, 0))
                hits_text_rect = hits_text.get_rect(center=(700, 50))
                misses_text_rect = misses_text.get_rect(center=(700, 75))
                game_window.blit(hits_text, hits_text_rect)
                game_window.blit(misses_text, misses_text_rect)

                accuracy = (
                    (num_hits / num_total_clicks) * 100 if num_total_clicks > 0 else 0
                )
                accuracy_text = font.render(
                    f"Точність: {accuracy:.2f}%", True, (0, 0, 0)
                )
                accuracy_text_rect = accuracy_text.get_rect(center=(700, 100))
                game_window.blit(accuracy_text, accuracy_text_rect)

            pygame.display.update()

            if goal_reached:
                # Очікування дії гравця після завершення гри
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif (
                            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                        ):
                            break
                        elif (
                            event.type == pygame.KEYDOWN
                            and event.key == pygame.K_ESCAPE
                        ):
                            pygame.mixer.music.stop()  # Зупинити відтворення музики
                            return
                    else:
                        continue
                    break


# Основний блок коду
if __name__ == "__main__":
    run_game("4")  # Запуск гри зі складністю "2" за замовчуванням
