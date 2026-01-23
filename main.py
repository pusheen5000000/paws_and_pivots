import pygame, sys
import math
tilt_angle = 0
mouse_held = False

#initialization
pygame.init()
pygame.mixer.init()

#audio
pygame.mixer.music.load('assets/bgmusic.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0
click_sound = pygame.mixer.Sound('assets/click.mp3')
click_sound.set_volume(0.5)


SCREEN = pygame.display.set_mode((800,800))
shrink = 0.625
#bg / assetloading
BG = pygame.image.load('assets/main_menu.png').convert_alpha()
BG = pygame.transform.scale(BG,(800, 800))
welcomeBG = pygame.image.load('assets/welcomeBG.png').convert_alpha()
welcomeBG = pygame.transform.scale(welcomeBG, (800, 800))
critterBG = pygame.image.load('assets/critterBG.png').convert_alpha()
critterBG = pygame.transform.scale(critterBG, (800, 800))
#window name
pygame.display.set_caption('Paws and Pivots')

#font
font = pygame.font.SysFont('arial', 30)

#cursor
cursor_surface = pygame.image.load('assets/cursor.png').convert_alpha()
cursor_surface = pygame.transform.scale(cursor_surface,(32, 32))

clickcursor_surface = pygame.image.load('assets/clickcursor.png').convert_alpha()
clickcursor_surface = pygame.transform.scale(clickcursor_surface,(32, 32))

hotspot = (0,0)
custom_cursor = pygame.cursors.Cursor(hotspot, cursor_surface)
custom_clickcursor = pygame.cursors.Cursor(hotspot, clickcursor_surface)
pygame.mouse.set_cursor(custom_cursor)
class Button():
    def __init__(self, x_pos, y_pos, image, click_sound=None):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.original_image = image
        self.image = self.original_image

        self.grown_image = pygame.transform.scale(image, (int(image.get_width() * 1.1), int(image.get_height() * 1.1)))
        self.grown_rect = self.grown_image.get_rect(center = (self.x_pos, self.y_pos))
        self.original_rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = self.original_rect

        self.click_sound = click_sound
    # tilt animation
    def tilt(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.original_rect.center)



    def update(self):
        SCREEN.blit(self.image, self.rect)

    def grow(self, isHovering):
        if isHovering:
            self.rect = self.grown_rect
            self.image = self.grown_image
        else:
            self.rect = self.original_rect
            self.image = self.original_image
    def changeCursor(self, isHovering):
        if isHovering:
            pygame.mouse.set_cursor(custom_clickcursor)
        else:
            pygame.mouse.set_cursor(custom_cursor)

    def checkForInput(self, position):
        return self.original_rect.collidepoint(position)

    def click(self):
        if self.click_sound:
            self.click_sound.play()

    def move(self, newx, newy):
        self.x_pos = newx
        self.y_pos = newy
        self.grown_rect = self.grown_image.get_rect(center=(self.x_pos, self.y_pos))
        self.original_rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = self.original_rect

#button loading
playbutton_surface = pygame.image.load('assets/button.png').convert_alpha()
playbutton_surface = pygame.transform.scale(playbutton_surface, (263, 263))
playbutton = Button(210, 625, playbutton_surface, click_sound)

gobutton_surface = pygame.image.load('assets/gobutton.png').convert_alpha()
gobutton = Button(300, 450, gobutton_surface, click_sound)

#critters loading and resizing
critter_scale = 0.6  # 60% of original size

critter_surface1 = pygame.image.load('assets/critter1.png').convert_alpha()
critter_surface1 = pygame.transform.scale(
    critter_surface1,
    (int(critter_surface1.get_width() * critter_scale),
     int(critter_surface1.get_height() * critter_scale))
)

critter_surface2 = pygame.image.load('assets/critter2.png').convert_alpha()
critter_surface2 = pygame.transform.scale(
    critter_surface2,
    (int(critter_surface2.get_width() * critter_scale),
     int(critter_surface2.get_height() * critter_scale))
)

critter_surface3 = pygame.image.load('assets/critter3.png').convert_alpha()
critter_surface3 = pygame.transform.scale(
    critter_surface3,
    (int(critter_surface3.get_width() * critter_scale),
     int(critter_surface3.get_height() * critter_scale))
)

critter_surface4 = pygame.image.load('assets/critter4.png').convert_alpha()
critter_surface4 = pygame.transform.scale(
    critter_surface4,
    (int(critter_surface4.get_width() * critter_scale),
     int(critter_surface4.get_height() * critter_scale))
)

critter1 = Button(250, 80, critter_surface1)  # dubai
critter2 = Button(650, 45, critter_surface2)  # monkey
critter3 = Button(150, 400, critter_surface3)  # bunny
critter4 = Button(550, 625, critter_surface4)  # kitty


def main_menu():
    global tilt_angle, mouse_held
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        tilt_angle += 0.025
        tilt = math.sin(tilt_angle) * 10
        for c in [critter1, critter2, critter3, critter4]:
            c.tilt(tilt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_held:
                mouse_held = True
                if playbutton.checkForInput(MENU_MOUSE_POS): #checks if button is clicked, this should take you to next screen
                    playbutton.click()
                    pygame.mouse.set_cursor(custom_cursor)
                    welcome()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        playbutton.grow(playbutton.checkForInput(MENU_MOUSE_POS))
        playbutton.changeCursor(playbutton.checkForInput(MENU_MOUSE_POS))
        playbutton.update()

        for c in [critter1, critter2, critter3, critter4]:
            c.update()
        pygame.display.update()

def welcome():
    global mouse_held
    while True:
        SCREEN.blit(welcomeBG, (0, 0))

        WELCOME_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_held:
                mouse_held = True
                if gobutton.checkForInput(WELCOME_MOUSE_POS):
                    gobutton.click() #button clicked or something
                    pygame.mouse.set_cursor(custom_cursor)
                    chooseCritter()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        gobutton.grow(gobutton.checkForInput(WELCOME_MOUSE_POS))
        gobutton.changeCursor(gobutton.checkForInput(WELCOME_MOUSE_POS))
        gobutton.update()

        pygame.display.update()

def chooseCritter():
    global mouse_held, critter2
    critter1.move(150, 300)
    critter3.move(130, 650)
    critter4.move(550, 350)
    critter2 = Button(500, 700, pygame.transform.flip(critter2.original_image, True, True))
    for c in [critter1, critter2, critter3, critter4]:
        c.image = c.original_image
        c.rect = c.original_rect
    while True:
        SCREEN.blit(critterBG, (0, 0))

        critter_mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_held:
                mouse_held = True
                for c in [critter1, critter2, critter3, critter4]:
                    if c.checkForInput(critter_mouse_pos):
                        c.click()
                        pygame.mouse.set_cursor(custom_cursor)

        for c in [critter1, critter2, critter3, critter4]:
            c.grow(c.checkForInput(critter_mouse_pos))
            c.changeCursor(c.checkForInput(critter_mouse_pos))
            c.update()

        pygame.display.update()


#run game
main_menu()
