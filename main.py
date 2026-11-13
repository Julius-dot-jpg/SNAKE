
import asyncio
import pygame
import random

pygame.init()

# ==================================
# BILDSCHIRM
# ==================================

WIDTH = 1000
HEIGHT = 750

# Echter Bildschirm im Vollbildmodus
display = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)

DISPLAY_WIDTH, DISPLAY_HEIGHT = display.get_size()

# Interne Spielfläche
screen = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# ==================================
# FARBEN
# ==================================

DARK = (4, 15, 8)
GREEN_BG = (20, 75, 30)
GREEN = (0, 230, 70)
DARK_GREEN = (0, 100, 0)
RED = (255, 45, 45)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 50)
BLUE = (50, 150, 255)
PURPLE = (180, 70, 255)
ORANGE = (255, 140, 30)

# ==================================
# SCHRIFTARTEN
# ==================================

font_big = pygame.font.Font(None, 90)
font_medium = pygame.font.Font(None, 55)
font_small = pygame.font.Font(None, 34)

# ==================================
# KOORDINATEN UMWANDELN
# ==================================

def screen_position(pos):

    x = int(pos[0] * WIDTH / DISPLAY_WIDTH)
    y = int(pos[1] * HEIGHT / DISPLAY_HEIGHT)

    return (x, y)


# ==================================
# TEXT ZEICHNEN
# ==================================

def draw_text(text, font, color, x, y):

    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    screen.blit(text_surface, text_rect)


# ==================================
# BUTTONS ZEICHNEN
# ==================================

def button(text, x, y, width, height, color=GREEN_BG):

    rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        GREEN,
        rect,
        width=2,
        border_radius=12
    )

    draw_text(
        text,
        font_small,
        WHITE,
        x + width // 2,
        y + height // 2
    )

    return rect


# ==================================
# SPIELZUSTAND
# ==================================

state = "menu"
language = "Deutsch"
coins = 0

movement_mode = "normal"
game_mode = "endless"

moving_left = False
moving_right = False
moving_up = False
moving_down = False

# ==================================
# SPRACHEN
# ==================================

translations = {

    "Deutsch": {
        "title": "SCHLANGE",
        "start": "Start",
        "settings": "Einstellungen",
        "shop": "Laden",
        "back": "Zurück",
        "score": "Punkte",
        "gameover": "SPIEL VORBEI",
        "restart": "Neustart",
        "menu": "Menü",
        "choose": "Sprache auswählen",
        "coins": "Münzen",
        "buy": "Kaufen",
        "owned": "Besitzt du",
        "equipped": "Ausgewählt",
        "choose_game": "Spielmodus auswählen:",
        "endless_mode": "Endlosmodus",
        "adventure_mode": "Abenteuermodus",
        "won": "GESCHAFFT!"
    },

    "English": {
        "title": "SNAKE",
        "start": "Start",
        "settings": "Settings",
        "shop": "Shop",
        "back": "Back",
        "score": "Score",
        "gameover": "GAME OVER",
        "restart": "Restart",
        "menu": "Menu",
        "choose": "Choose language",
        "coins": "Coins",
        "buy": "Buy",
        "owned": "Owned",
        "equipped": "Selected",
        "choose_game": "Select game mode:",
        "endless_mode": "Endless mode",
        "adventure_mode": "Adventure mode",
        "won": "YOU DID IT!"
    },

    "Français": {
        "title": "SERPENT",
        "start": "Démarrer",
        "settings": "Paramètres",
        "shop": "Boutique",
        "back": "Retour",
        "score": "Points",
        "gameover": "FIN DU JEU",
        "restart": "Recommencer",
        "menu": "Menu",
        "choose": "Choisir la langue",
        "coins": "Pièces",
        "buy": "Acheter",
        "owned": "Possédé",
        "equipped": "Choisi",
        "choose_game": "Choisir le mode de jeu:",
        "endless_mode": "Mode infini",
        "adventure_mode": "Mode aventure",
        "won": "BRAVO!"
    },

    "Español": {
        "title": "SERPIENTE",
        "start": "Empezar",
        "settings": "Ajustes",
        "shop": "Tienda",
        "back": "Volver",
        "score": "Puntos",
        "gameover": "FIN DEL JUEGO",
        "restart": "Reiniciar",
        "menu": "Menú",
        "choose": "Elegir idioma",
        "coins": "Monedas",
        "buy": "Comprar",
        "owned": "Comprado",
        "equipped": "Elegido",
        "choose_game": "Seleccionar modo de juego:",
        "endless_mode": "Modo infinito",
        "adventure_mode": "Modo aventura",
        "won": "LO LOGRASTE!"
    }
}


def tr(key):
    return translations[language][key]


# ==================================
# SHOP UND SKINS
# ==================================

skins = {

    "Grün": {
        "color": GREEN,
        "head": (120, 255, 150),
        "price": 0
    },

    "Blau": {
        "color": BLUE,
        "head": (130, 210, 255),
        "price": 5
    },

    "Lila": {
        "color": PURPLE,
        "head": (255, 130, 210),
        "price": 10
    },

    "Orange": {
        "color": ORANGE,
        "head": (255, 210, 120),
        "price": 15
    }
}

owned_skins = ["Grün"]
selected_skin = "Grün"

# ==================================
# SPIELFELD
# ==================================

CELL = 25
COLS = 40
ROWS = 21
FIELD_TOP = 70

snake = []

direction = (1, 0)
next_direction = (1, 0)

apple = (10, 10)
score = 0

SNAKE_SPEED = 200
last_move = 0

ADVENTURE_GOAL = 10

# ==================================
# RICHTUNGEN
# ==================================

def get_direction(key):

    if key in (pygame.K_w, pygame.K_UP):
        return (0, -1)

    if key in (pygame.K_s, pygame.K_DOWN):
        return (0, 1)

    if key in (pygame.K_a, pygame.K_LEFT):
        return (-1, 0)

    if key in (pygame.K_d, pygame.K_RIGHT):
        return (1, 0)

    return None


def set_direction(new_direction):

    global next_direction

    if new_direction is None:
        return

    if (
        new_direction[0] != -direction[0]
        or new_direction[1] != -direction[1]
    ):
        next_direction = new_direction


# ==================================
# BEWEGUNG ZURÜCKSETZEN
# ==================================

def reset_movement():

    global moving_left
    global moving_right
    global moving_up
    global moving_down

    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False


# ==================================
# BEWEGUNG AKTIVIEREN
# ==================================

def activate_movement(new_direction):

    global moving_left
    global moving_right
    global moving_up
    global moving_down

    reset_movement()

    if new_direction == (-1, 0):
        moving_left = True

    elif new_direction == (1, 0):
        moving_right = True

    elif new_direction == (0, -1):
        moving_up = True

    elif new_direction == (0, 1):
        moving_down = True

    set_direction(new_direction)


# ==================================
# SNAKE STEUERUNG
# ==================================

def snake_steuerung(event):

    global moving_left
    global moving_right
    global moving_up
    global moving_down

    if event.type == pygame.KEYDOWN:

        new_direction = get_direction(event.key)

        if new_direction is not None:
            activate_movement(new_direction)

    elif event.type == pygame.KEYUP:

        if event.key in (pygame.K_a, pygame.K_LEFT):
            moving_left = False

        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            moving_right = False

        elif event.key in (pygame.K_w, pygame.K_UP):
            moving_up = False

        elif event.key in (pygame.K_s, pygame.K_DOWN):
            moving_down = False

    elif event.type in (
        pygame.MOUSEBUTTONDOWN,
        pygame.FINGERDOWN
    ):

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = screen_position(event.pos)
        else:
            pos = (
                int(event.x * WIDTH),
                int(event.y * HEIGHT)
            )

        new_direction = None

        if pygame.Rect(470, 605, 60, 45).collidepoint(pos):
            new_direction = (0, -1)

        elif pygame.Rect(405, 665, 60, 45).collidepoint(pos):
            new_direction = (-1, 0)

        elif pygame.Rect(470, 665, 60, 45).collidepoint(pos):
            new_direction = (0, 1)

        elif pygame.Rect(535, 665, 60, 45).collidepoint(pos):
            new_direction = (1, 0)

        if new_direction is not None:
            activate_movement(new_direction)

    elif event.type in (
        pygame.MOUSEBUTTONUP,
        pygame.FINGERUP
    ):

        reset_movement()


# ==================================
# APFEL ERSTELLEN
# ==================================

def neuer_apfel():

    global apple

    free_positions = [
        (x, y)
        for x in range(COLS)
        for y in range(ROWS)
        if (x, y) not in snake
    ]

    if free_positions:
        apple = random.choice(free_positions)
    else:
        apple = None


# ==================================
# SPIEL ZURÜCKSETZEN
# ==================================

def reset_game():

    global snake
    global direction, next_direction
    global score, last_move
    global SNAKE_SPEED

    snake = [
        (20, 10),
        (19, 10),
        (18, 10)
    ]

    direction = (1, 0)
    next_direction = (1, 0)

    score = 0
    SNAKE_SPEED = 200

    reset_movement()

    last_move = pygame.time.get_ticks()

    neuer_apfel()


# ==================================
# SPIELENDE PRÜFEN
# ==================================

def pruefe_spielende():

    global state

    if game_mode == "adventure" and score >= ADVENTURE_GOAL:
        state = "gamewon"


# ==================================
# SCHLANGE BEWEGEN
# ==================================

def move_snake():

    global direction
    global score
    global coins
    global state
    global SNAKE_SPEED

    direction = next_direction

    head_x, head_y = snake[0]

    new_head = (
        (head_x + direction[0]) % COLS,
        (head_y + direction[1]) % ROWS
    )

    eating = new_head == apple

    body = snake if eating else snake[:-1]

    if new_head in body:
        state = "gameover"
        return

    snake.insert(0, new_head)

    if eating:

        score += 1
        coins += 1

        SNAKE_SPEED = max(70, SNAKE_SPEED - 10)

        pruefe_spielende()

        if state != "game":
            return

        neuer_apfel()

    else:
        snake.pop()

    if apple is None:
        state = "gameover"


# ==================================
# BEWEGUNG BEI GEDRÜCKTER TASTE
# ==================================

def move_snake_gedrueckt():

    global direction
    global score
    global coins
    global state
    global SNAKE_SPEED

    if moving_left:
        new_direction = (-1, 0)

    elif moving_right:
        new_direction = (1, 0)

    elif moving_up:
        new_direction = (0, -1)

    elif moving_down:
        new_direction = (0, 1)

    else:
        return

    if (
        new_direction[0] == -direction[0]
        and new_direction[1] == -direction[1]
    ):
        return

    direction = new_direction

    head_x, head_y = snake[0]

    new_head = (
        (head_x + direction[0]) % COLS,
        (head_y + direction[1]) % ROWS
    )

    eating = new_head == apple

    body = snake if eating else snake[:-1]

    if new_head in body:
        state = "gameover"
        return

    snake.insert(0, new_head)

    if eating:

        score += 1
        coins += 1

        SNAKE_SPEED = max(70, SNAKE_SPEED - 10)

        pruefe_spielende()

        if state != "game":
            return

        neuer_apfel()

    else:
        snake.pop()

    if apple is None:
        state = "gameover"


# ==================================
# TOUCH BUTTONS
# ==================================

def draw_controls():

    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (0, 595, WIDTH, 155)
    )

    button("▲", 470, 605, 60, 45)
    button("◀", 405, 665, 60, 45)
    button("▼", 470, 665, 60, 45)
    button("▶", 535, 665, 60, 45)


# ==================================
# SPIEL ZEICHNEN
# ==================================

def draw_game():

    screen.fill(DARK)

    draw_text(
        f"{tr('score')}: {score}",
        font_medium,
        WHITE,
        WIDTH // 2,
        35
    )

    if game_mode == "adventure":

        draw_text(
            f"{score}/{ADVENTURE_GOAL}",
            font_small,
            YELLOW,
            850,
            35
        )

    pygame.draw.rect(
        screen,
        GREEN_BG,
        (0, FIELD_TOP, WIDTH, ROWS * CELL)
    )

    snake_color = skins[selected_skin]["color"]
    head_color = skins[selected_skin]["head"]

    for i, segment in enumerate(snake):

        x = segment[0] * CELL
        y = FIELD_TOP + segment[1] * CELL

        color = head_color if i == 0 else snake_color

        pygame.draw.rect(
            screen,
            color,
            (x + 2, y + 2, CELL - 4, CELL - 4),
            border_radius=6
        )

    if apple is not None:

        apple_x = apple[0] * CELL + CELL // 2
        apple_y = FIELD_TOP + apple[1] * CELL + CELL // 2

        pygame.draw.circle(
            screen,
            RED,
            (apple_x, apple_y),
            10
        )

    draw_controls()


# ==================================
# HAUPTMENÜ
# ==================================

def draw_menu():

    screen.fill(DARK)

    draw_text(
        tr("title"),
        font_big,
        GREEN,
        WIDTH // 2,
        170
    )

    pygame.draw.line(
        screen,
        GREEN,
        (300, 225),
        (700, 225),
        4
    )

    start_rect = button(
        tr("start"),
        350, 300, 300, 75
    )

    settings_rect = button(
        tr("settings"),
        350, 410, 300, 75
    )

    shop_rect = button(
        tr("shop"),
        350, 520, 300, 75
    )

    draw_text(
        f"{tr('coins')}: {coins}",
        font_small,
        YELLOW,
        WIDTH // 2,
        680
    )

    return start_rect, settings_rect, shop_rect


# ==================================
# SPIELMODUS AUSWÄHLEN
# ==================================

def game_mode_auswaelen():

    screen.fill(DARK)

    draw_text(
        tr("choose_game"),
        font_medium,
        GREEN,
        WIDTH // 2,
        130
    )

    endless_rect = button(
        tr("endless_mode"),
        250, 280, 500, 75
    )

    adventure_rect = button(
        tr("adventure_mode"),
        250, 390, 500, 75
    )

    back_rect = button(
        tr("back"),
        350, 550, 300, 65
    )

    return endless_rect, adventure_rect, back_rect


# ==================================
# EINSTELLUNGEN
# ==================================

def draw_settings():

    screen.fill(DARK)

    draw_text(
        tr("settings"),
        font_big,
        GREEN,
        WIDTH // 2,
        120
    )

    draw_text(
        tr("choose"),
        font_medium,
        WHITE,
        WIDTH // 2,
        230
    )

    language_rects = []

    languages = [
        "Deutsch",
        "English",
        "Français",
        "Español"
    ]

    for i, lang in enumerate(languages):

        color = DARK_GREEN if language == lang else GREEN_BG

        rect = button(
            lang,
            350,
            290 + i * 80,
            300,
            60,
            color
        )

        language_rects.append((rect, lang))

    back_rect = button(
        tr("back"),
        350, 640, 300, 65
    )

    return language_rects, back_rect


# ==================================
# SHOP
# ==================================

def draw_shop():

    screen.fill(DARK)

    draw_text(
        tr("shop"),
        font_big,
        GREEN,
        WIDTH // 2,
        85
    )

    draw_text(
        f"{tr('coins')}: {coins}",
        font_medium,
        YELLOW,
        WIDTH // 2,
        155
    )

    skin_rects = []

    for i, (name, data) in enumerate(skins.items()):

        y = 220 + i * 95

        rect = pygame.Rect(200, y, 600, 75)

        pygame.draw.rect(
            screen,
            GREEN_BG,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            data["color"],
            (220, y + 12, 45, 50),
            border_radius=8
        )

        if name in owned_skins:

            if selected_skin == name:
                status = tr("equipped")
            else:
                status = tr("owned")

        else:
            status = f"{tr('buy')}: {data['price']}"

        draw_text(
            name,
            font_medium,
            WHITE,
            300,
            y + 37
        )

        draw_text(
            status,
            font_small,
            YELLOW,
            650,
            y + 37
        )

        skin_rects.append((rect, name))

    back_rect = button(
        tr("back"),
        350, 640, 300, 65
    )

    return skin_rects, back_rect


# ==================================
# SHOP KLICKS
# ==================================

def shop_click(pos):

    global coins
    global selected_skin
    global state

    skin_rects, back_rect = draw_shop()

    for rect, name in skin_rects:

        if rect.collidepoint(pos):

            price = skins[name]["price"]

            if name in owned_skins:
                selected_skin = name

            elif coins >= price:

                coins -= price
                owned_skins.append(name)
                selected_skin = name

    if back_rect.collidepoint(pos):
        state = "menu"


# ==================================
# GAME OVER
# ==================================

def draw_gameover():

    screen.fill(DARK)

    draw_text(
        tr("gameover"),
        font_big,
        RED,
        WIDTH // 2,
        230
    )

    draw_text(
        f"{tr('score')}: {score}",
        font_medium,
        WHITE,
        WIDTH // 2,
        320
    )

    restart_rect = button(
        tr("restart"),
        350, 410, 300, 70
    )

    menu_rect = button(
        tr("menu"),
        350, 510, 300, 70
    )

    return restart_rect, menu_rect


# ==================================
# ABENTEUER GESCHAFFT
# ==================================

def draw_gamewon():

    screen.fill(DARK)

    draw_text(
        tr("won"),
        font_big,
        GREEN,
        WIDTH // 2,
        230
    )

    draw_text(
        f"{tr('score')}: {score}",
        font_medium,
        WHITE,
        WIDTH // 2,
        320
    )

    restart_rect = button(
        tr("restart"),
        350, 410, 300, 70
    )

    menu_rect = button(
        tr("menu"),
        350, 510, 300, 70
    )

    return restart_rect, menu_rect


# ==================================
# HAUPTPROGRAMM
# ==================================

async def main():

    global state
    global language
    global last_move
    global movement_mode
    global game_mode

    reset_game()

    running = True

    while running:

        now = pygame.time.get_ticks()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # ESC beendet den Vollbildmodus
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    if state == "game":
                        state = "menu"
                        reset_movement()
                    else:
                        running = False

            # SNAKE STEUERUNG
            if state == "game":
                snake_steuerung(event)

            # MAUSKLICKS
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = screen_position(event.pos)

                if state == "menu":

                    start_rect, settings_rect, shop_rect = draw_menu()

                    if start_rect.collidepoint(pos):
                        state = "modus_auswaelen"

                    elif settings_rect.collidepoint(pos):
                        state = "settings"

                    elif shop_rect.collidepoint(pos):
                        state = "shop"

                elif state == "modus_auswaelen":

                    endless_rect, adventure_rect, back_rect = game_mode_auswaelen()

                    if endless_rect.collidepoint(pos):

                        game_mode = "endless"
                        movement_mode = "normal"

                        reset_game()
                        state = "game"

                    elif adventure_rect.collidepoint(pos):

                        game_mode = "adventure"
                        movement_mode = "gedrueckt"

                        reset_game()
                        state = "game"

                    elif back_rect.collidepoint(pos):
                        state = "menu"

                elif state == "settings":

                    language_rects, back_rect = draw_settings()

                    for rect, lang in language_rects:

                        if rect.collidepoint(pos):
                            language = lang

                    if back_rect.collidepoint(pos):
                        state = "menu"

                elif state == "shop":

                    shop_click(pos)

                elif state == "gameover":

                    restart_rect, menu_rect = draw_gameover()

                    if restart_rect.collidepoint(pos):
                        reset_game()
                        state = "game"

                    elif menu_rect.collidepoint(pos):
                        state = "menu"

                elif state == "gamewon":

                    restart_rect, menu_rect = draw_gamewon()

                    if restart_rect.collidepoint(pos):
                        reset_game()
                        state = "game"

                    elif menu_rect.collidepoint(pos):
                        state = "menu"

        # ==================================
        # SPIELBEWEGUNG
        # ==================================

        if state == "game":

            if movement_mode == "normal":

                if now - last_move >= SNAKE_SPEED:

                    move_snake()
                    last_move = now

            elif movement_mode == "gedrueckt":

                if (
                    (moving_left or moving_right
                     or moving_up or moving_down)
                    and now - last_move >= SNAKE_SPEED
                ):

                    move_snake_gedrueckt()
                    last_move = now

        # ==================================
        # BILDSCHIRM ZEICHNEN
        # ==================================

        if state == "menu":
            draw_menu()

        elif state == "modus_auswaelen":
            game_mode_auswaelen()

        elif state == "settings":
            draw_settings()

        elif state == "shop":
            draw_shop()

        elif state == "game":
            draw_game()

        elif state == "gameover":
            draw_gameover()

        elif state == "gamewon":
            draw_gamewon()

        # ==================================
        # AUF DEN ECHTEN BILDSCHIRM SKALIEREN
        # ==================================

        display.fill(DARK)

        pygame.transform.scale(
            screen,
            (DISPLAY_WIDTH, DISPLAY_HEIGHT),
            display
        )

        pygame.display.flip()

        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()


# ==================================
# START
# ==================================

if __name__ == "__main__":
    asyncio.run(main())
