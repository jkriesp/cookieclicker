#from turtle import width
import click
import pygame, sys
from pygame.locals import *
import time
import threading
from threading import Thread
import os
os.environ["SDL_VIDEODRIVER"]="x11"


pygame.init()
FPS = 30
FramePerSec = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_LIGHT = (170, 170, 170)
COLOR_DARK = (100, 100, 100)

# Fonts
cookies_font = pygame.font.Font(None, 50)

# Texts
auto_clicker = cookies_font.render("Auto Clicker", True, WHITE)

# Setup game window
DISPLAYSURF = pygame.display.set_mode((400,600))
display_width = DISPLAYSURF.get_width()
display_height = DISPLAYSURF.get_height()
pygame.display.set_caption("Cookie Clicker")

# Define thread exit event
exit_event = threading.Event()


# Auto Clicker
def ac():
    global cookies

    while True:
        cookies += 1
        if exit_event.is_set():
            break
        time.sleep(0.1)

auto_clicker = Thread(target=ac)

# And so it begins
cookies = 0

# Update cookie counter
def update_cookies(pressed_key, pressed_mouse):
    global cookies

    if pressed_key[K_RETURN]:
        print("Hello from key update_cookies: " + str(cookies))
        cookies += 1

    elif pressed_mouse:
        print("Hello from mouse update_cookies: " + str(cookies))
        cookies += 0
    elif pressed_key[K_a] and not auto_clicker.is_alive():
        print("Auto Clicker [ACTIVE]")
        auto_clicker.start()
        

# Cookie
class Cookie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Cookie.png"), (300, 300))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 300)

    def update(self, event_list):
        global cookies
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos) and any(mouse_buttons):
            cookies += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

C1 = Cookie()
group = pygame.sprite.Group(C1)

while True:
    # insert game here
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit_event.set()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0] or mouse_presses[2]:
                #update_cookies(pygame.key.get_pressed(), True)
                group.update(event)

    
    DISPLAYSURF.fill(BLACK)
    C1.draw(DISPLAYSURF)

    # Update cookies
    update_cookies(pygame.key.get_pressed(), False)

    cookies_surf = cookies_font.render("Cookies: " + str(cookies), 1, (255, 179, 102))
    cookies_pos = [10, 10]
    DISPLAYSURF.blit(cookies_surf, cookies_pos)


    pygame.display.update()
    FramePerSec.tick(FPS)
