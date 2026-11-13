
# Python-Bibliotheken
import pygame
import tkinter as tk
import sys
import random

# Pygame vorbereiten
pygame.init()

# Farben
gruen = (0, 100, 0)
rot = (255, 0, 0)

# Bildschirmgröße
WIDTH = 1000
HEIGHT = 750


# Schlange
snake_x = 500
snake_y = 375
snake_width = 50
snake_height = 50
snake_color = (0, 255, 0)

snake_geschwindigkeit = 5


# Äpfel
apple_radius = 20
apple_color = rot

apple_x = random.randint(
    apple_radius,
    WIDTH - apple_radius
)

apple_y = random.randint(
    apple_radius,
    HEIGHT - apple_radius
)

apple_rect = pygame.Rect(
    apple_x - apple_radius,
    apple_y - apple_radius,
    apple_radius * 2,
    apple_radius * 2
)


# Bewegungsvariablen
moving_up = False
moving_down = False
moving_left = False
moving_right = False


# FPS
Clock = pygame.time.Clock()


# Apfel neu generieren
def neuer_apfel():

    global apple_x, apple_y, apple_rect

    while True:

        apple_x = random.randint(
            apple_radius,
            WIDTH - apple_radius
        )

        apple_y = random.randint(
            apple_radius,
            HEIGHT - apple_radius
        )

        apple_rect = pygame.Rect(
            apple_x - apple_radius,
            apple_y - apple_radius,
            apple_radius * 2,
            apple_radius * 2
        )

        if not snake_rect.colliderect(apple_rect):
            break


# Menüschleife
def menu():

    title.pack(pady=20)

    settings_button.place(x=10, y=10)

    start_button.pack(pady=30)

    exit_button.pack(pady=30)

    home_menu.mainloop()


# Spielschleife
def game_loop():

    global snake_x, snake_y
    global moving_up, moving_down
    global moving_left, moving_right
    global snake_color
    global apple_x, apple_y, apple_rect
    global snake_rect

    settings_frame.place_forget()
    settings_button.place_forget()

    home_menu.withdraw()

    # Pygame-Fenster erstellen
    game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")

    # Schlange zurücksetzen
    snake_x = 500
    snake_y = 375

    snake_color = (0, 255, 0)

    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False

    snake_rect = pygame.Rect(
        snake_x,
        snake_y,
        snake_width,
        snake_height
    )

    # Apfel neu generieren
    neuer_apfel()

    running = True

    while running:

        # Events abfragen
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Bewegungssteuerung
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    moving_up = True
                    moving_down = False
                    moving_left = False
                    moving_right = False

                elif event.key == pygame.K_s:
                    moving_down = True
                    moving_up = False
                    moving_left = False
                    moving_right = False

                elif event.key == pygame.K_a:
                    moving_left = True
                    moving_right = False
                    moving_up = False
                    moving_down = False

                elif event.key == pygame.K_d:
                    moving_right = True
                    moving_left = False
                    moving_up = False
                    moving_down = False

        # Schlange bewegen
        if moving_right:
            snake_x += snake_geschwindigkeit

        if moving_left:
            snake_x -= snake_geschwindigkeit

        if moving_up:
            snake_y -= snake_geschwindigkeit

        if moving_down:
            snake_y += snake_geschwindigkeit

        # Bildschirmgrenzen überprüfen

        # Links -> Rechts
        if snake_x + snake_width < 0:
            snake_x = WIDTH

        # Rechts -> Links
        if snake_x > WIDTH:
            snake_x = -snake_width

        # Oben -> Unten
        if snake_y + snake_height < 0:
            snake_y = HEIGHT

        # Unten -> Oben
        if snake_y > HEIGHT:
            snake_y = -snake_height

        # Rechteck aktualisieren
        snake_rect = pygame.Rect(
            snake_x,
            snake_y,
            snake_width,
            snake_height
        )

        # Tastenkombination überprüfen
        keys = pygame.key.get_pressed()

        if (
            keys[pygame.K_w]
            and keys[pygame.K_a]
            and keys[pygame.K_s]
            and keys[pygame.K_d]
        ):
            snake_color = rot

        # Apfel-Kollision überprüfen
        if snake_rect.colliderect(apple_rect):

            neuer_apfel()

        # Hintergrund
        game_screen.fill(gruen)

        # Schlange zeichnen
        pygame.draw.rect(
            game_screen,
            snake_color,
            snake_rect
        )

        # Apfel zeichnen
        pygame.draw.circle(
            game_screen,
            apple_color,
            (apple_x, apple_y),
            apple_radius
        )

        # Fenster aktualisieren
        pygame.display.flip()

        # FPS begrenzen
        Clock.tick(60)

    # Spiel beenden
    pygame.display.quit()

    home_menu.deiconify()

    settings_button.place(x=10, y=10)


# Beenden
def exit():

    home_menu.destroy()

    pygame.quit()

    sys.exit()


# Einstellungen öffnen
def settings():

    settings_button.place_forget()

    settings_frame.place(x=0, y=0)

    exit_settings_frame_button.place(x=292, y=3)

    settings_frame_title.pack(pady=30, padx=(0, 90))

    language_menu.pack(pady=30)


# Einstellungen schließen
def exit_settings():

    exit_settings_frame_button.place_forget()

    settings_frame.place_forget()

    settings_frame_title.pack_forget()

    settings_button.place(x=10, y=10)


# Sprache Deutsch
def sprache_deutsch():

    home_menu.title("Spiel")

    title.config(text="Spiel")

    settings_frame_title.config(text="Einstellungen")

    exit_button.config(text="Beenden")

    start_button.config(text="Start")


# Sprache Englisch
def sprache_english():

    home_menu.title("Game")

    title.config(text="Game")

    settings_frame_title.config(text="Settings")

    exit_button.config(text="Exit")

    start_button.config(text="Start")


# Sprache Französisch
def sprache_französisch():

    home_menu.title("Jeu")

    title.config(text="Jeu")

    settings_frame_title.config(text="Paramètres")

    exit_button.config(text="Terminer")

    start_button.config(text="Démarrer")


# Sprache Spanisch
def sprache_spanisch():

    home_menu.title("Juego")

    title.config(text="Juego")

    settings_frame_title.config(text="Configuraciones")

    exit_button.config(text="Terminar")

    start_button.config(text="Empezar")


# Sprachen auswählen
def sprach_auswaelen():

    if Sprache.get() == "Deutsch":
        sprache_deutsch()

    elif Sprache.get() == "English":
        sprache_english()

    elif Sprache.get() == "Français":
        sprache_französisch()

    elif Sprache.get() == "Español":
        sprache_spanisch()


# Tkinter-Fenster
home_menu = tk.Tk()

home_menu.geometry("1000x750")

home_menu.title("Game")

home_menu.configure(bg="#236A23")

home_menu.resizable(False, False)


# Einstellungs-Frame
settings_frame = tk.Frame(
    home_menu,
    bg="#040A04",
    width=350,
    height=750
)

settings_frame.pack_propagate(False)


# Überschrift
title = tk.Label(
    home_menu,
    text="Game",
    bg="#236A23",
    fg="#20BA20",
    font=("Consolas", 50, "bold")
)


# Einstellungs-Überschrift
settings_frame_title = tk.Label(
    settings_frame,
    text="Settings",
    bg="#040A04",
    fg="#E7E7E7",
    font=("Consolas", 22, "bold")
)


# Beenden-Button
exit_button = tk.Button(
    home_menu,
    text="Exit",
    bg="#236A23",
    fg="#20BA20",
    activebackground="#0EEC0E",
    font=("Arial", 30, "bold"),
    command=exit
)


# Start-Button
start_button = tk.Button(
    home_menu,
    text="Start",
    bg="#236A23",
    fg="#20BA20",
    activebackground="#0EEC0E",
    font=("Arial", 30, "bold"),
    command=game_loop
)


# Einstellungen-Button
settings_button = tk.Button(
    home_menu,
    text="⚙️",
    bg="#236A23",
    fg="#20BA20",
    activebackground="#0EEC0E",
    font=("Arial", 30, "bold"),
    command=settings
)


# Einstellungen schließen
exit_settings_frame_button = tk.Button(
    settings_frame,
    text="x",
    bg="#E7E7E7",
    fg="#080A08",
    activebackground="#EC0E0E",
    font=("Arial", 30, "bold"),
    command=exit_settings
)


# Sprachauswahl
Sprache = tk.StringVar(value="English")

language_menu = tk.OptionMenu(
    settings_frame,
    Sprache,
    "English",
    "Français",
    "Español",
    "Deutsch",
    command=lambda _: sprach_auswaelen()
)

language_menu.config(
    font=("Arial", 20, "bold"),
    width=270
)


# Menü starten
if __name__ == "__main__":
    menu()
