import cv2
import mediapipe
import pygame
import math

mp_landmark = mediapipe.solutions.drawing_utils
mp_stile = mediapipe.solutions.drawing_styles
mp_face_mesh = mediapipe.solutions.face_mesh

cap = cv2.VideoCapture(0)

pygame.init()
Nero = (0, 0, 0)
Rosso = (255, 0, 0)
RossoScuro = (128, 0, 0)
Bianco = (255, 255, 255)
Verde = (0, 128, 0)
Blu = (40, 50, 120)
Blu2 = (30, 40, 100)
dw = 630
dh = 600
border_radius = 30
screen = pygame.display.set_mode([dw, dh])
pygame.display.set_caption("Brick Breaker")

background = pygame.image.load("sfondo.png")
background = pygame.transform.scale(background, [dw, dh])

min_x, max_x = float('inf'), float('-inf')
smooth_factor = 0.3


def display_text(txt, col, dim, x, y):
    font = pygame.font.SysFont("bold", dim)
    testo = font.render(txt, True, col)
    rect = testo.get_rect()
    rect.center = x, y
    screen.blit(testo, rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([105, 30], pygame.SRCALPHA)
        pygame.draw.rect(self.image, Blu2, [0, 0, 105, 30], border_radius=20)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target_x = x

    def update(self, x_occhio):
        self.target_x = x_occhio - self.rect.width // 2
        self.rect.x += (self.target_x - self.rect.x) * smooth_factor
        if self.rect.right > dw:
            self.rect.right = dw
        if self.rect.left < 0:
            self.rect.left = 0


class Palla(pygame.sprite.Sprite):
    def __init__(self, p, w, pos):
        super().__init__()
        self.image = pygame.image.load("b.png")
        self.image = pygame.transform.scale(self.image, [45, 45])
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.p = p
        self.w = w
        self.pos = pos
        self.vx = 0
        self.vy = 5
        self.speed = 5
        self.top_coll = False
        self.bot_coll = False
        self.punteggio = 0

    def muro_colpito(self):
        colpito = pygame.sprite.groupcollide(palle, self.pos.muri, False, True)
        if colpito:
            muri_colpiti = len(colpito[self])
            self.punteggio += muri_colpiti
            return True
        return False

    def player_colpito(self):
        colpito = pygame.sprite.spritecollide(self.p, palle, False)
        return bool(colpito)

    def print_punteggio(self):
        display_text("Punteggio: " + str(self.punteggio), Blu2, 20, 315, 10)

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= dw:
            self.vx = -self.vx
        if self.rect.top <= 0:
            self.vy = -self.vy
        if self.player_colpito():
            self.vy = -self.vy
            offset = (self.rect.centerx - self.p.rect.centerx) / (self.p.rect.width // 2)
            self.vx += offset
        if self.muro_colpito():
            self.vy = -self.vy
        self.rect.x += self.vx
        self.rect.y += self.vy
        current_speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if current_speed != self.speed:
            factor = self.speed / current_speed
            self.vx *= factor
            self.vy *= factor


class Muri(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("muro.png")
        self.image = pygame.transform.scale(self.image, [90, 30])
        self.rect = self.image.get_rect()
        self.rect.x = x * 30
        self.rect.y = y * 30


class Map:
    def __init__(self, pos_file):
        self.pos_file = pos_file
        self.pos_list = []
        self.muri = pygame.sprite.Group()

    def update(self):
        with open(self.pos_file, 'r+') as f:
            for r in f:
                self.pos_list.append(r)
        for r, cars in enumerate(self.pos_list):
            for c, car in enumerate(cars):
                if car == '1':
                    self.m = Muri(c, r)
                    self.muri.add(self.m)
                    sprites.add(self.muri)


Celeste1 = (173, 226, 230)
Celeste2 = (135, 196, 235)


def draw_gradient_background(surface, color1, color2):
    for y in range(surface.get_height()):
        r = int(color1[0] + (color2[0] - color1[0]) * y / surface.get_height())
        g = int(color1[1] + (color2[1] - color1[1]) * y / surface.get_height())
        b = int(color1[2] + (color2[2] - color1[2]) * y / surface.get_height())
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))


def intro():
    draw_gradient_background(screen, Celeste1, Celeste2)
    display_text("Brick Breaker", Blu, 40, dw // 2, 100)

    icona = pygame.image.load("icon.png")
    icona = pygame.transform.scale(icona, (250, 250))
    icona_rect = icona.get_rect(center=(dw // 2, 230))
    screen.blit(icona, icona_rect)

    wait = True

    button_width, button_height = 150, 50
    button_y = 400
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


running, start, game, game_over = True, True, False, False


def update_eye_position(face_landmarks):
    global min_x, max_x

    occhio_sx_x = sum([face_landmarks.landmark[i].x for i in [362, 263, 386, 374]]) / 4
    occhio_dx_x = sum([face_landmarks.landmark[i].x for i in [33, 133, 159, 145]]) / 4

    avg_x = (occhio_sx_x + occhio_dx_x) / 2

    min_x = min(min_x, avg_x)
    max_x = max(max_x, avg_x)

    if min_x < max_x:
        norm_x = 1 - (avg_x - min_x) / (max_x - min_x)
        game_x = int(norm_x * dw)
    else:
        game_x = int((1 - avg_x) * dw)

    return game_x


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


with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened() and running:
        succ, image = cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        res = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        game_x = None

        if res.multi_face_landmarks:
            for face_landmarks in res.multi_face_landmarks:
                game_x = update_eye_position(face_landmarks)

        if start:
            intro()
            start = False
            game = True

        if game:
            map = Map('map.txt')
            sprites = pygame.sprite.Group()
            player = Player(225, 555)
            palla = Palla(player, dw, map)
            palle = pygame.sprite.Group()
            palle.add(palla)
            sprites.add(player)
            sprites.add(palle)
            map.update()
            game = False

        if game_over:
            game_over = False
            start = True
            game = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_x is not None:
            player.update(game_x)

        screen.blit(background, (0, 0))
        palla.update()
        palla.print_punteggio()
        sprites.draw(screen)

        if palla.rect.bottom >= dh:
            display_popup("Hai perso :(", Rosso)
            game_over = True

        if len(map.muri) == 0:
            display_popup("Hai vinto! :)", Verde)
            start = True
            game = True

        pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
