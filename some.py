import pygame
from pygame import Surface, SurfaceType

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 480, 480
FPS = 10
MAPS_DIR = 'maps'
TILE_SIZE = 32


class Labyrinth:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = []
        with open(f"{MAPS_DIR}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen: Surface | SurfaceType):
        color = {0: (0, 0, 0), 1: (120, 120, 120), 2: (50, 50, 50)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(color[self.get_tile_id(x, y)], rect)

    def get_tile_id(self, x, y):
        return self.map[y][x]

    def is_free(self, x, y):
        return self.get_tile_id(x, y) in self.free_tiles


class Hero:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def set_position(self, x, y):
        self.x, self.y = x, y

    def render(self, screen: Surface | SurfaceType):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (255, 255, 255), center, TILE_SIZE // 2)


class Game:
    def __init__(self, labyrinth: Labyrinth, hero: Hero):
        self.labyrinth = labyrinth
        self.hero = hero

    def render(self, screen: Surface | SurfaceType) -> None:
        self.labyrinth.render(screen)
        self.hero.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        print(next_x, next_y)
        if self.labyrinth.is_free(next_x, next_y):
            self.hero.set_position(next_x, next_y)


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    labyrinth = Labyrinth("simple_map.txt", [0, 2], 2)
    hero = Hero(7, 7)
    game = Game(labyrinth, hero)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update_hero()
        screen.fill((0, 0, 0))
        game.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
