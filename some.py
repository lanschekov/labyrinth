import pygame
from pygame import Surface, SurfaceType

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 480, 480
FPS = 10
MAPS_DIR = 'maps'
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30


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

    def find_path_step(self, start: tuple[int, int], target: tuple[int, int]):
        inf = 1000
        x, y = start
        distance = [[inf] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 <= next_y < self.height and \
                        self.is_free(next_x, next_y) and distance[next_y][next_x] == inf:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == inf or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


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


class Enemy:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self.delay = 100
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def set_position(self, x, y):
        self.x, self.y = x, y

    def render(self, screen: Surface | SurfaceType):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, pygame.Color('brown'), center, TILE_SIZE // 2)


class Game:
    def __init__(self, labyrinth: Labyrinth, hero: Hero, enemy: Enemy):
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemy = enemy

    def render(self, screen: Surface | SurfaceType) -> None:
        self.labyrinth.render(screen)
        self.hero.render(screen)
        self.enemy.render(screen)

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
        if self.labyrinth.is_free(next_x, next_y):
            self.hero.set_position(next_x, next_y)

    def move_enemy(self):
        next_position = self.labyrinth.find_path_step(self.enemy.get_position(), self.hero.get_position())
        self.enemy.set_position(*next_position)

    def is_win(self):
        return self.labyrinth.get_tile_id(*self.hero.get_position()) == \
               self.labyrinth.finish_tile

    def is_loss(self):
        return self.hero.get_position() == self.enemy.get_position()


def show_message(screen: Surface | SurfaceType, message: str):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, (50, 70, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = WINDOW_WIDTH // 2 - text_w // 2
    text_y = WINDOW_HEIGHT // 2 - text_h // 2
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    labyrinth = Labyrinth("simple_map.txt", [0, 2], 2)
    hero = Hero(7, 7)
    enemy = Enemy(7, 1)
    game = Game(labyrinth, hero, enemy)

    clock = pygame.time.Clock()
    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over:
                game.move_enemy()
        if not game_over:
            game.update_hero()
        screen.fill((0, 0, 0))
        game.render(screen)
        if game.is_win():
            game_over = True
            show_message(screen, "You won!")
        if game.is_loss():
            game_over = True
            show_message(screen, "You lost!")
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
