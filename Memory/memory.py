import cv2
import mediapipe
import pyautogui
import random
import time
import pygame

mp_landmark = mediapipe.solutions.drawing_utils
mp_stile = mediapipe.solutions.drawing_styles
mp_face_mesh = mediapipe.solutions.face_mesh

cap = cv2.VideoCapture(0)

pygame.init()
Bianco = (255, 255, 255)
Nero = (0, 0, 0)
Rosso = (255, 0, 0)
RossoScuro = (128, 0, 0)
Verde = (0, 128, 0)
Blu = (40, 50, 120)
Blu2 = (30, 40, 100)
dw = 1400
dh = 900
border_radius = 30
screen = pygame.display.set_mode([dw, dh])
pygame.display.set_caption("Memory")

lun = 200
marg = 20
pad_x = 100
pad_y = 100
r = 4
c = 5
cards = [i for i in range(10) for j in range(2)]
random.shuffle(cards)
val_grid = [cards[i * len(cards) // r:(i + 1) * len(cards) // r] for i in range(r)]
grid = [[] for _ in range(r)]
for i in range(r):
    for j in range(c):
        x = marg + (lun + marg) * j
        y = marg + (lun + marg) * i
        grid[i].append(pygame.Rect(x, y, lun, lun))

girata = []
matched = []
sbag = []
turno = 0

min_x, max_x = float('inf'), float('-inf')
min_y, max_y = float('inf'), float('-inf')

card_hover_start_time = None
hovered_card = None

screen_w, screen_h = pyautogui.size()
screen_x = 400
screen_y = 400

smooth_factor = 0.12


def inizializza():
    global cards, val_grid, grid, girata, matched, sbag, turno
    cards = [i for i in range(10) for j in range(2)]
    random.shuffle(cards)
    val_grid = [cards[i * len(cards) // r:(i + 1) * len(cards) // r] for i in range(r)]
    grid = [[] for _ in range(r)]
    for i in range(r):
        for j in range(c):
            x = marg + (lun + marg) * j
            y = marg + (lun + marg) * i
            grid[i].append(pygame.Rect(x, y, lun, lun))

    girata = []
    matched = []
    sbag = []
    turno = 0


inizializza()


def display_text(txt, col, dim, x, y):
    font = pygame.font.SysFont("bold", dim)
    testo = font.render(txt, True, col)
    rect = testo.get_rect()
    rect.center = x, y
    screen.blit(testo, rect)


face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def normalize_val(val, min_val, max_val):
    if min_val < max_val:
        return (val - min_val) / (max_val - min_val)
    return val


def track_face():
    global screen_x, screen_y, card_hover_start_time, hovered_card, min_x, max_x, min_y, max_y
    success, image = cap.read()
    if not success:
        return

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            frame_h, frame_w, _ = image.shape

            occhio_sx_x = sum([landmarks[i].x for i in [362, 263, 386, 374]]) / 4
            occhio_dx_x = sum([landmarks[i].x for i in [33, 133, 159, 145]]) / 4
            avg_x = (occhio_sx_x + occhio_dx_x) / 2
            avg_y = (landmarks[1].y + landmarks[4].y) / 2

            min_x = min(min_x, avg_x)
            max_x = max(max_x, avg_x)
            min_y = min(min_y, avg_y)
            max_y = max(max_y, avg_y)

            norm_x = normalize_val(avg_x, min_x, max_x)
            norm_y = normalize_val(avg_y, min_y, max_y)

            inverted_x = 1 - norm_x

            new_screen_x = inverted_x * screen_w
            new_screen_y = norm_y * screen_h

            screen_x += (new_screen_x - screen_x) * smooth_factor
            screen_y += (new_screen_y - screen_y) * smooth_factor

            screen_x = max(50, min(screen_x, screen_w - 50))
            screen_y = max(50, min(screen_y, screen_h - 50))

            pyautogui.moveTo(screen_x, screen_y)

            mouse_pos = pygame.mouse.get_pos()
            for i in range(r):
                for j in range(c):
                    if grid[i][j].collidepoint(mouse_pos):
                        if hovered_card != (i, j):
                            hovered_card = (i, j)
                            card_hover_start_time = time.time()
                        elif time.time() - card_hover_start_time >= 1:
                            if [i, j] not in girata and [i, j] not in matched:
                                girata.append([i, j])
                            card_hover_start_time = None
                            hovered_card = None
                    else:
                        if hovered_card == (i, j):
                            card_hover_start_time = None
                            hovered_card = None


Celeste1 = (173, 226, 230)
Celeste2 = (135, 196, 235)


def draw_gradient_rect(surface, color1, color2, rect):
    for y in range(rect.height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / rect.height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / rect.height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / rect.height)
        pygame.draw.line(surface, (r, g, b), (rect.left, rect.top + y), (rect.right, rect.top + y))


def draw_cards():
    screen.fill(Nero)
    for i in range(r):
        for j in range(c):
            if [i, j] not in girata and [i, j] not in matched and [i, j] not in sbag:
                draw_gradient_rect(screen, Celeste1, Celeste2, grid[i][j])
            else:
                pygame.draw.rect(screen, Bianco, grid[i][j])

    if girata:
        for i in girata:
            display_text(str(val_grid[i[0]][i[1]]), Nero, 50, grid[i[0]][i[1]].x + pad_x, grid[i[0]][i[1]].y + pad_y)
    if matched:
        for i in matched:
            display_text(str(val_grid[i[0]][i[1]]), Verde, 50, grid[i[0]][i[1]].x + pad_x, grid[i[0]][i[1]].y + pad_y)
    if sbag:
        for i in sbag:
            display_text(str(val_grid[i[0]][i[1]]), Rosso, 50, grid[i[0]][i[1]].x + pad_x, grid[i[0]][i[1]].y + pad_y)
    display_text("Memory", Bianco, 35, 1250, 80)
    display_text("Turni: " + str(turno), Bianco, 40, 1250, 180)


def draw_gradient_background(surface, color1, color2):
    for y in range(surface.get_height()):
        r = int(color1[0] + (color2[0] - color1[0]) * y / surface.get_height())
        g = int(color1[1] + (color2[1] - color1[1]) * y / surface.get_height())
        b = int(color1[2] + (color2[2] - color1[2]) * y / surface.get_height())
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))


def intro():
    draw_gradient_background(screen, Celeste1, Celeste2)
    display_text("Memory", Blu, 60, dw // 2, 100)

    icona = pygame.image.load("icon.png")
    icona = pygame.transform.scale(icona, (360, 360))
    icona_rect = icona.get_rect(center=(dw // 2, 380))
    screen.blit(icona, icona_rect)

    wait = True

    button_width, button_height = 150, 50
    button_y = 620
    start_button_x = dw // 2 - button_width - 100
    exit_button_x = dw // 2 + 100

    while wait:
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        start_button_rect = pygame.Rect(start_button_x, button_y, button_width, button_height)
        if start_button_rect.collidepoint(cur):
            pygame.draw.rect(screen, Blu2, start_button_rect, border_radius=border_radius)

            if click[0] == 1:
                wait = False
                pygame.time.wait(300)
        else:
            pygame.draw.rect(screen, Blu, start_button_rect, border_radius=border_radius)
        display_text("Inizia", Bianco, 30, start_button_x + button_width // 2, button_y + button_height // 2)

        exit_button_rect = pygame.Rect(exit_button_x, button_y, button_width, button_height)
        if exit_button_rect.collidepoint(cur):
            pygame.draw.rect(screen, Blu2, exit_button_rect, border_radius=border_radius)
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, Blu, exit_button_rect, border_radius=border_radius)
        display_text("Esci", Bianco, 30, exit_button_x + button_width // 2, button_y + button_height // 2)

        pygame.display.flip()


def display_popup(mess, col):
    overlay = pygame.Surface((dw, dh), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    popupw, popuph = 400, 200
    popup = pygame.Surface((popupw, popuph), pygame.SRCALPHA)
    pygame.draw.rect(popup, (255, 255, 255), popup.get_rect(), border_radius=20)
    pygame.draw.rect(popup, col, popup.get_rect(), 5, border_radius=20)

    font = pygame.font.SysFont("bold", 40)
    text_surface = font.render(mess, True, col)
    text_rect = text_surface.get_rect(center=(popupw // 2, popuph // 2))
    popup.blit(text_surface, text_rect)
    screen.blit(overlay, (0, 0))
    screen.blit(popup, (dw // 2 - popupw // 2, dh // 2 - popuph // 2))

    pygame.display.flip()
    pygame.time.wait(1000)


start, game, game_over = True, False, False

while True:
    if start:
        intro()
        inizializza()
        start = False
        game = True

    if game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                exit()

        track_face()

        if len(girata) == 2:
            turno += 1
            if val_grid[girata[0][0]][girata[0][1]] == val_grid[girata[1][0]][girata[1][1]]:
                matched.extend(girata)
            else:
                sbag.extend(girata)
            girata.clear()

        draw_cards()

        if len(matched) == 20:
            display_popup("Hai vinto! :)", Verde)
            start = True
            game = False

        pygame.display.flip()

        if sbag:
            time.sleep(1)
            sbag.clear()

    clock = pygame.time.Clock()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
