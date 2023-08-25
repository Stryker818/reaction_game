import pygame
import sys
from game import run_game
from pygame import mixer
from time import sleep
from settings import sound_file1_path, sound_file2_path, music_file_path

# Ініціалізація Pygame та mixer
pygame.init()
pygame.mixer.init()

# Колір
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
LIGHT_BLUE = (45, 142, 247)
BLACK = (0, 0, 0)

sound_enabled = True

preview_sound = pygame.mixer.Sound("Preview_tanchiki.mp3")
color_cycle = 0

music_game = pygame.mixer.music.load(music_file_path)
preview_sound = pygame.mixer.Sound("Preview_tanchiki.mp3")
sound_file1 = pygame.mixer.Sound(sound_file1_path)
sound_file2 = pygame.mixer.Sound(sound_file2_path)

# Список кольорів для створення ефекту неонової надпису
neon_colors = [
    (255, 0, 0),  # Червоний
    (255, 165, 0),  # Оранжевий
    (255, 255, 0),  # Жовтий
    (0, 255, 0),  # Зелений
    (0, 0, 255),  # Синій
    (75, 0, 130),  # Індиго
    (238, 130, 238),  # Фіолетовий
]


# Функція для зміни кольору тексту
def change_neon_color():
    global color_cycle
    if color_cycle < len(neon_colors) - 1:
        color_cycle += 1
    else:
        color_cycle = 0
    sleep(0.01)
    return neon_colors[color_cycle]


# Функція для вмикання / вимикання звуку та музики
def toggle_sound_and_music():
    global sound_enabled
    sound_enabled = not sound_enabled  # Перемикаємо стан звуку

    if sound_enabled:
        pygame.mixer.music.set_volume(1.0)
        sound_file1.set_volume(0.2)
        sound_file2.set_volume(1.0)
        preview_sound.set_volume(1.0)
        pygame.mixer.unpause()
    else:
        pygame.mixer.music.set_volume(0.0)
        sound_file1.set_volume(0.0)
        sound_file2.set_volume(0.0)
        preview_sound.set_volume(0.0)
        pygame.mixer.pause()


def main_menu():
    global sound_enabled, music_enabled
    menu_running = True
    button_width, button_height = 200, 60
    button_x = 300
    button_spacing = 80
    menu_title_font = pygame.font.Font(None, 60)
    menu_button_font = pygame.font.Font(None, 36)
    menu_title_shadow_font = pygame.font.Font(None, 60)
    title_shadow_text = menu_title_shadow_font.render("Reaction Game", True, BLACK)
    title_shadow_rect = title_shadow_text.get_rect(center=(402, 152))
    selected_difficulty = "2"
    sound_button_image = pygame.image.load("sound.png")

    while menu_running:
        background_image = pygame.image.load("view_menu.jpg")
        window.blit(background_image, (-450, -65))
        # Ініціалізація музики (завантажте її тут)
        music_game = pygame.mixer.music.load(music_file_path)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        button1 = pygame.Rect(button_x, button_spacing * 3, button_width, button_height)
        button2 = pygame.Rect(button_x, button_spacing * 4, button_width, button_height)
        button3 = pygame.Rect(button_x, button_spacing * 5, button_width, button_height)
        button4 = pygame.Rect(button_x, button_spacing * 6, button_width, button_height)
        sound_button_rect = pygame.Rect(730, 20, 35, 35)
        sound_button_image.get_rect(topleft=(730, 20))
        sound_button_rect.topleft = (730, 20)

        pygame.draw.rect(
            window, GRAY if button1.collidepoint((mouse_x, mouse_y)) else WHITE, button1
        )
        pygame.draw.rect(
            window, GRAY if button2.collidepoint((mouse_x, mouse_y)) else WHITE, button2
        )
        pygame.draw.rect(
            window, GRAY if button3.collidepoint((mouse_x, mouse_y)) else WHITE, button3
        )
        pygame.draw.rect(
            window, GRAY if button4.collidepoint((mouse_x, mouse_y)) else WHITE, button4
        )
        pygame.draw.rect(
            window,
            GREEN if sound_enabled else RED,
            sound_button_rect,
        )
        pygame.draw.rect(window, BLACK, sound_button_rect, 1)

        pygame.draw.rect(window, BLACK, button1, 1)
        pygame.draw.rect(window, BLACK, button2, 1)
        pygame.draw.rect(window, BLACK, button3, 1)
        pygame.draw.rect(window, BLACK, button4, 1)

        title_text = menu_title_font.render("Reaction Game", True, change_neon_color())
        title_rect = title_text.get_rect(center=(400, 150))
        window.blit(title_text, title_rect)

        button1_text = menu_button_font.render("Початок гри", True, LIGHT_BLUE)
        button1_rect = button1_text.get_rect(center=button1.center)
        window.blit(button1_text, button1_rect)

        button2_text = menu_button_font.render("Опції", True, LIGHT_BLUE)
        button2_rect = button2_text.get_rect(center=button2.center)
        window.blit(button2_text, button2_rect)

        button3_text = menu_button_font.render("Вихід", True, LIGHT_BLUE)
        button3_rect = button3_text.get_rect(center=button3.center)
        window.blit(button3_text, button3_rect)
        button4_text = menu_button_font.render("Інструкція", True, LIGHT_BLUE)
        button4_rect = button4_text.get_rect(center=button4.center)

        window.blit(button4_text, button4_rect)
        window.blit(title_shadow_text, title_shadow_rect)
        window.blit(title_text, title_rect)
        window.blit(sound_button_image, sound_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint((mouse_x, mouse_y)):
                    run_game(selected_difficulty, sound_enabled, music_enabled)
                    pygame.mixer.music.play()
                elif button2.collidepoint((mouse_x, mouse_y)):
                    selected_difficulty = options(selected_difficulty)
                elif button3.collidepoint((mouse_x, mouse_y)):
                    pygame.quit()
                elif button4.collidepoint((mouse_x, mouse_y)):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        show_instructions()
                if (
                    sound_button_rect.collidepoint((mouse_x, mouse_y))
                    and event.type == pygame.MOUSEBUTTONDOWN
                ):
                    toggle_sound_and_music()  # Виклик функції для вмикання / вимикання звуку та музики
        pygame.display.flip()


def show_instructions():
    instructions_running = True
    instructions_font = pygame.font.Font(None, 30)

    while instructions_running:
        window.fill(WHITE)

        instructions_text = [
            "Інструкція для гри:",
            "----------------------",
            "Ваша мета - спіймати якнайбільше кругів",
            "за найкоротший час.",
            "Для перемоги потрібно набрати певну кількість балів",
            "в залежності від рівня складності.",
            "",
            "Керування:",
            "- Натисніть на круг, щоб спіймати його.",
            "- Під час гри натисніть Esc, щоб повернутися до Головного меню.",
            "",
            "Складність:",
            "- Ви можете обрати складність гри в меню Опції.",
            "- Складність визначає розмір і кількість кругів.",
            "",
            "Гарної гри!",
            "",
            "Натисніть Esc, щоб повернутися до Головного меню.",
        ]

        y_offset = 50
        for line in instructions_text:
            text_surface = instructions_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(400, y_offset))
            window.blit(text_surface, text_rect)
            y_offset += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                instructions_running = False


def options(selected_difficulty):
    options_running = True
    font = pygame.font.Font(None, 36)
    selected_difficulty = "2"  # Значення за замовчуванням

    while options_running:
        background_image = pygame.image.load("view_menu.jpg")
        window.blit(background_image, (-450, -65))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        back_button = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(
            window,
            GRAY if back_button.collidepoint((mouse_x, mouse_y)) else WHITE,
            back_button,
        )
        pygame.draw.rect(window, BLACK, back_button, 1)
        back_text = font.render("Назад", True, LIGHT_BLUE)
        back_text_rect = back_text.get_rect(center=back_button.center)
        window.blit(back_text, back_text_rect)

        # Кнопки для вибору складності
        easy_button = pygame.Rect(100, 100, 200, 40)
        medium_button = pygame.Rect(100, 150, 200, 40)
        hard_button = pygame.Rect(100, 200, 200, 40)
        sandbox_button = pygame.Rect(100, 250, 200, 40)

        # Подсвітка обраної складності
        pygame.draw.rect(
            window,
            GRAY if selected_difficulty == "1" else WHITE,
            easy_button,
        )
        pygame.draw.rect(
            window,
            GRAY if selected_difficulty == "2" else WHITE,
            medium_button,
        )
        pygame.draw.rect(
            window,
            GRAY if selected_difficulty == "3" else WHITE,
            hard_button,
        )
        pygame.draw.rect(
            window,
            GRAY if selected_difficulty == "4" else WHITE,
            sandbox_button,
        )
        pygame.draw.rect(window, BLACK, easy_button, 1)
        pygame.draw.rect(window, BLACK, medium_button, 1)
        pygame.draw.rect(window, BLACK, hard_button, 1)
        pygame.draw.rect(window, BLACK, sandbox_button, 1)

        # Текст на кнопках
        easy_text = font.render("Легко", True, LIGHT_BLUE)
        medium_text = font.render("Середньо", True, LIGHT_BLUE)
        hard_text = font.render("Складно", True, LIGHT_BLUE)
        sandbox_text = font.render("Песочниця", True, LIGHT_BLUE)

        easy_text_rect = easy_text.get_rect(center=easy_button.center)
        medium_text_rect = medium_text.get_rect(center=medium_button.center)
        hard_text_rect = hard_text.get_rect(center=hard_button.center)
        sandbox_text_rect = sandbox_text.get_rect(center=sandbox_button.center)

        window.blit(easy_text, easy_text_rect)
        window.blit(medium_text, medium_text_rect)
        window.blit(hard_text, hard_text_rect)
        window.blit(sandbox_text, sandbox_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint((mouse_x, mouse_y)):
                    options_running = False
                elif easy_button.collidepoint((mouse_x, mouse_y)):
                    selected_difficulty = "1"
                elif medium_button.collidepoint((mouse_x, mouse_y)):
                    selected_difficulty = "2"
                elif hard_button.collidepoint((mouse_x, mouse_y)):
                    selected_difficulty = "3"
                elif sandbox_button.collidepoint((mouse_x, mouse_y)):
                    selected_difficulty = "4"

    return selected_difficulty


# Основний цикл програми
if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Реакційна гра")
    sound_enabled = True  # Додайте цю змінну
    music_enabled = True  # Додайте цю змінну

    # Відтворюємо звук при запуску програми
    preview_sound.play()

    main_menu()
