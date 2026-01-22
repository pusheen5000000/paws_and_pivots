import pygame, sys
#initialization
pygame.init()

SCREEN = pygame.display.set_mode((800,800))

#bg
BG = pygame.image.load('assets/main_menu.png').convert_alpha()
BG = pygame.transform.scale(BG,(800, 800))

#window name
pygame.display.set_caption('Paws and Pixels')

#font
font = pygame.font.SysFont('arial', 30)

#cursor
cursor_surface = pygame.image.load('assets/cursor.png').convert_alpha()
cursor_surface = pygame.transform.scale(cursor_surface,(32, 32))
hotspot = (0,0)
custom_cursor = pygame.cursors.Cursor(hotspot, cursor_surface)
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



    def update(self):
        SCREEN.blit(self.image, self.rect)

    def grow(self, isHovering):
        if isHovering:
            self.rect = self.grown_rect
            self.image = self.grown_image
        else:
            self.rect = self.original_rect
            self.image = self.original_image

    def checkForInput(self, position):
        return self.original_rect.collidepoint(position)


playbutton_surface = pygame.image.load('assets/button.png').convert_alpha()
playbutton_surface = pygame.transform.scale(playbutton_surface, (263, 263))
playbutton = Button(210, 625, playbutton_surface)


def main_menu():

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = font.render("Main Menu", True, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playbutton.checkForInput(MENU_MOUSE_POS) #checks if button is clicked, this should take you to next screen

        playbutton.update()
        playbutton.grow(playbutton.checkForInput(MENU_MOUSE_POS))

        pygame.display.update()


main_menu()
