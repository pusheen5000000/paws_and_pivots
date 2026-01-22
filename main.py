import pygame, sys
import pygame, sys
import math
tilt_angle = 0
#initialization
pygame.init()

SCREEN = pygame.display.set_mode((800,800))
shrink = 0.625
#bg / assetloading
BG = pygame.image.load('assets/main_menu.png').convert_alpha()
BG = pygame.transform.scale(BG,(800, 800))
welcomeBG = pygame.image.load('assets/welcomeBG.png').convert_alpha()
welcomeBG = pygame.transform.scale(welcomeBG, (800, 800))

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
    def __init__(self, x_pos, y_pos, image):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.original_image = image
        self.image = self.original_image

        self.grown_image = pygame.transform.scale(image, (int(image.get_width() * 1.1), int(image.get_height() * 1.1)))
        self.grown_rect = self.grown_image.get_rect(center = (self.x_pos, self.y_pos))
        self.original_rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = self.original_rect

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

#button loading
playbutton_surface = pygame.image.load('assets/button.png').convert_alpha()
playbutton_surface = pygame.transform.scale(playbutton_surface, (263, 263))
playbutton = Button(210, 625, playbutton_surface)

gobutton_surface = pygame.image.load('assets/gobutton.png').convert_alpha()
gobutton = Button(300, 450, gobutton_surface)

#critters loading and resizing
critter_scale = 0.6  # 60% of original size

critter_sufrace1 = pygame.image.load('assets/Subject.png').convert_alpha()
critter_sufrace1 = pygame.transform.scale(
    critter_sufrace1,
    (int(critter_sufrace1.get_width() * critter_scale),
     int(critter_sufrace1.get_height() * critter_scale))
)

critter_sufrace2 = pygame.image.load('assets/Subject 2.png').convert_alpha()
critter_sufrace2 = pygame.transform.scale(
    critter_sufrace2,
    (int(critter_sufrace2.get_width() * critter_scale),
     int(critter_sufrace2.get_height() * critter_scale))
)

critter_sufrace3 = pygame.image.load('assets/Subject 3.png').convert_alpha()
critter_sufrace3 = pygame.transform.scale(
    critter_sufrace3,
    (int(critter_sufrace3.get_width() * critter_scale),
     int(critter_sufrace3.get_height() * critter_scale))
)

critter_sufrace4 = pygame.image.load('assets/Subject 4.png').convert_alpha()
critter_sufrace4 = pygame.transform.scale(
    critter_sufrace4,
    (int(critter_sufrace4.get_width() * critter_scale),
     int(critter_sufrace4.get_height() * critter_scale))
)

critter1 = Button(250, 80, critter_sufrace1)  # dubai
critter2 = Button(650, 45, critter_sufrace2)  # monkey
critter3 = Button(150, 400, critter_sufrace3)  # bunny
critter4 = Button(550, 625, critter_sufrace4)  # kitty


def main_menu():
    global tilt_angle
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        tilt_angle += 0.025
        tilt = math.sin(tilt_angle) * 10
        critter1.tilt(tilt)
        critter2.tilt(tilt)
        critter3.tilt(tilt)
        critter4.tilt(tilt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playbutton.checkForInput(MENU_MOUSE_POS): #checks if button is clicked, this should take you to next screen
                    pygame.mouse.set_cursor(custom_cursor)
                    chooseCritter()

        playbutton.grow(playbutton.checkForInput(MENU_MOUSE_POS))
        playbutton.changeCursor(playbutton.checkForInput(MENU_MOUSE_POS))
        playbutton.update()

        critter1.update()
        critter2.update()
        critter3.update()
        critter4.update()

        pygame.display.update()

def chooseCritter():
    while True:
        SCREEN.blit(welcomeBG, (0, 0))

        WELCOME_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = 1 #button clicked or something

        gobutton.grow(gobutton.checkForInput(WELCOME_MOUSE_POS))
        gobutton.changeCursor(gobutton.checkForInput(WELCOME_MOUSE_POS))
        gobutton.update()

        pygame.display.update()



main_menu()
