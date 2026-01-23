import pygame, sys, math, random
tilt_angle = 0
mouse_held = False
confetti_particles = []

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

        self.grown_image = pygame.transform.scale(
            image,
            (int(image.get_width() * 1.1), int(image.get_height() * 1.1))
        )
        self.grown_rect = self.grown_image.get_rect(center=(self.x_pos, self.y_pos))
        self.original_rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = self.original_rect

        self.click_sound = click_sound


    def tilt(self, angle):
        base_image = self.grown_image if self.image == self.grown_image else self.original_image
        self.image = pygame.transform.rotate(base_image, angle)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

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

class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(4, 7)

        self.color = random.choice([
            (255, 182, 193),  # pink
            (173, 216, 230),  # light blue
            (255, 255, 153),  # yellow
            (204, 153, 255),  # purple
            (144, 238, 144)   # green
        ])

        # very gentle drift
        self.vx = random.uniform(-0.4, 0.4)
        self.vy = random.uniform(-0.3, 0.2)

        self.life = 80

        # twinkle values
        self.alpha = random.randint(120, 255)
        self.alpha_speed = random.choice([-4, -3, -2, 2, 3, 4])

        self.rotation = random.randint(0, 360)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # tiny downward drift (almost floating)
        self.vy += 0.01

        # twinkle (fade in/out)
        self.alpha += self.alpha_speed
        if self.alpha <= 80 or self.alpha >= 255:
            self.alpha_speed *= -1

        self.rotation += random.randint(-3, 3)
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            rect_surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            rect_surf.set_alpha(self.alpha)

            pygame.draw.rect(
                rect_surf,
                self.color,
                (0, 0, self.size, self.size)
            )

            rotated = pygame.transform.rotate(rect_surf, self.rotation)
            surface.blit(rotated, (self.x, self.y))

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

        # Tilt critters
        tilt_angle += 0.01
        tilt = math.sin(tilt_angle) * 10
        for c in [critter1, critter2, critter3, critter4]:
            c.tilt(tilt)

        # Hoverable objects
        hoverables = [critter1, critter2, critter3, critter4, playbutton]
        for obj in hoverables:
            if obj.checkForInput(MENU_MOUSE_POS):
                if random.random() < 0.1 and len(confetti_particles) < 100:  # slows down confetti spawn
                    confetti_particles.append(Confetti(MENU_MOUSE_POS[0], MENU_MOUSE_POS[1]))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_held:
                mouse_held = True
                if playbutton.checkForInput(MENU_MOUSE_POS):
                    playbutton.click()
                    pygame.mouse.set_cursor(custom_cursor)
                    welcome()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        # Update buttons
        playbutton.grow(playbutton.checkForInput(MENU_MOUSE_POS))
        playbutton.changeCursor(playbutton.checkForInput(MENU_MOUSE_POS))
        playbutton.update()

        # Update critters
        for c in [critter1, critter2, critter3, critter4]:
            c.update()

        # Draw confetti ON TOP
        for particle in confetti_particles[:]:
            particle.update()
            particle.draw(SCREEN)
            if particle.life <= 0:
                confetti_particles.remove(particle)

        pygame.display.update()




def welcome():
    global mouse_held
    while True:
        SCREEN.blit(welcomeBG, (0, 0))
        WELCOME_MOUSE_POS = pygame.mouse.get_pos()

        # Hoverable objects
        hoverables = [gobutton]
        for obj in hoverables:
            if obj.checkForInput(WELCOME_MOUSE_POS):
                if random.random() < 0.25:
                    confetti_particles.append(Confetti(WELCOME_MOUSE_POS[0], WELCOME_MOUSE_POS[1]))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_held:
                mouse_held = True
                if gobutton.checkForInput(WELCOME_MOUSE_POS):
                    gobutton.click()
                    pygame.mouse.set_cursor(custom_cursor)
                    chooseCritter()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        # Update buttons
        gobutton.grow(gobutton.checkForInput(WELCOME_MOUSE_POS))
        gobutton.changeCursor(gobutton.checkForInput(WELCOME_MOUSE_POS))
        gobutton.update()

        # Draw confetti
        for particle in confetti_particles[:]:
            particle.update()
            particle.draw(SCREEN)
            if particle.life <= 0:
                confetti_particles.remove(particle)

        pygame.display.update()



def chooseCritter():
    global mouse_held, critter2, tilt_angle

    # reposition critters
    critter1.move(150, 300)
    critter3.move(130, 650)
    critter4.move(550, 350)
    critter2 = Button(500, 700, pygame.transform.flip(critter2.original_image, True, True))

    # reset sounds only
    for c in [critter1, critter2, critter3, critter4]:
        c.click_sound = click_sound

    while True:
        SCREEN.blit(critterBG, (0, 0))
        critter_mouse_pos = pygame.mouse.get_pos()

        # Update tilt angle
        tilt_angle += 0.01
        tilt = math.sin(tilt_angle) * 10

        hoverables = [critter1, critter2, critter3, critter4]

        # Spawn confetti if hovering
        for obj in hoverables:
            if obj.checkForInput(critter_mouse_pos):
                if random.random() < 0.1:
                    confetti_particles.append(Confetti(critter_mouse_pos[0], critter_mouse_pos[1]))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_held:
                mouse_held = True
                for c in hoverables:
                    if c.checkForInput(critter_mouse_pos):
                        c.click()
                        pygame.mouse.set_cursor(custom_cursor)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        # Update critters
        for c in hoverables:
            is_hovering = c.checkForInput(critter_mouse_pos)
            c.grow(is_hovering)       # scale up if hovering
            c.tilt(tilt)              # rotate the current scaled image
            c.changeCursor(is_hovering)
            c.update()                # draw on screen

        # Update confetti
        for particle in confetti_particles[:]:
            particle.update()
            particle.draw(SCREEN)
            if particle.life <= 0:
                confetti_particles.remove(particle)

        pygame.display.update()




#run game
main_menu()
