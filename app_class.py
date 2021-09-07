import pygame
import sys
from player_class import *

from settings import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//28 #
        self.cell_height = MAZE_HEIGHT//30 #
        self.player = Player(self, PLAYER_START_POS)
        self.walls = []

        self.load()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    #################    HELP FUNCTIONS     #####################

    def draw_text(self, words, screen, pos, size, color, font_name, centred=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centred:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('background.png')  # may be improved
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        #Open walls file
        #creating walls list with coords of walls
        with open('walls.txt', 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx,yidx))


    def draw_grid(self):
        for x in range(WIDTH //self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))

        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))

        for wall in self.walls:
            pygame.draw.rect(self.background, (111, 52, 123), (wall.x*self.cell_width, wall.y*self.cell_height,
                                                               self.cell_width, self.cell_height))


    #################    INTRO FUNCTIONS     #####################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(START_TEXT_STRING, self.screen, [WIDTH // 2, HEIGHT // 2], START_TEXT_SIZE, (170, 132, 58),
                       START_FONT, centred=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE, (0, 102, 255),
                       START_FONT, centred=True)
        self.draw_text('HIGH SCORE', self.screen, [10, 0], START_TEXT_SIZE, (244, 244, 244),
                       START_FONT)
        pygame.display.update()

    #################    PLAYING FUNCTIONS     #####################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))

    def playing_update(self):
        self.player.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_text('CURRENT SCORE: 0', self.screen, [60, 0], 19, WHITE, START_FONT)
        self.draw_text('HIGH SCORE: 0', self.screen, [WIDTH//2+60, 0], 19, WHITE, START_FONT)
        self.player.draw()
        pygame.display.update()
