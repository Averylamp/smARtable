import pygame

# -- Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        self.width = 150
        self.height = 150
        # Set height, width
        self.image = pygame.Surface([self.width, self.height])
        pygame.draw.circle(self.image, (238,160,0), (self.width // 2,self.width // 2), self.width // 2, 0)


        # self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y - self.width // 2
        self.rect.x = x - self.width // 2

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y

    def setPosition(self, x, y):
        self.rect.x = x - self.width // 2
        self.rect.y = y - self.width // 2

    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x


        # Move up/down
        self.rect.y += self.change_y


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('Test')

# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()


# Create the player paddle object
player = Player(0, 0)
player.setPosition(900,540)

alignment_rect = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.draw.rect(alignment_rect, (255,0,255), [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 10)

all_sprite_list.add(player)

clock = pygame.time.Clock()

done = False

while not done:
    movement = 20
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-movement, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(movement, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -movement)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, movement)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(movement, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-movement, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, movement)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -movement)

    all_sprite_list.update()

    screen.fill(BLACK)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
