import sys, pygame
import time
from pygame.locals import *
import glob
import os
import random
import model

class Tile:


    def __init__(self, name):
        a = name.split('.')
        self._value = a[0]
        self._img = pygame.image.load(name)
        self._img = pygame.transform.scale(self._img, (60, 60))

class Board:


    def __init__(self, names):
        self._board = []
        self._rect = []
        line = []
        line_rect = []
        for name in names:
            new_tile = Tile(name)
            line.append(new_tile)
            line_rect.append(new_tile._img.get_rect())
            if (len(line) == 3):
                self._board.append(line)
                self._rect.append(line_rect)
                line = []
                line_rect = []

    def draw_board(self, screen):
        x = -(184 / 2) + (screen.get_width() / 2)
        y = 40
        for line, rect_line in zip(self._board, self._rect):
            for tile, rect in zip(line, rect_line):
                screen.blit(tile._img, (x, y))
                rect.x = x
                rect.y = y
                x += 62
            x = -(184 / 2) + (screen.get_width() / 2)
            y += 62

    def move_blank(self, direction):
        ret = False
        index = []
        a = None
        a_rect = None
        for line, rect_line in zip(self._board, self._rect):
            for tile, rect in zip(line, rect_line):
                if (tile._value == '0' ):
                    a = tile
                    a_rect = rect
                    index.append(self._board.index(line))
                    index.append(line.index(a))
        blank = self._rect[index[0]][index[1]]
        if (direction == 'UP'):
            if (index[0] == 0):
                raise ValueError('Can\'t go Up')
            else:
                neighbor = self._rect[index[0] - 1][index[1]]
                if blank.bottom >= neighbor.top:
                    self._rect[index[0] - 1][index[1]] = self._rect[index[0] - 1][index[1]].move([0, 1])
                    self._rect[index[0]][index[1]] = self._rect[index[0]][index[1]].move([0, -1])
                if blank.bottom == neighbor.top :
                    screen.blit(self._board[index[0]][index[1]]._img, self._rect[index[0]][index[1]])
                    inter = self._board[index[0]][index[1]]
                    self._board[index[0]][index[1]] = self._board[index[0] - 1][index[1]]
                    self._board[index[0] - 1][index[1]] = inter

                    inter = self._rect[index[0]][index[1]]
                    self._rect[index[0]][index[1]] = self._rect[index[0] - 1][index[1]]
                    self._rect[index[0] - 1][index[1]] = inter
                    ret = True

        if (direction == 'DOWN'):
            if (index[0] == 2):
                raise ValueError('Can\'t go Down')
            else:
                neighbor = self._rect[index[0] + 1][index[1]]
                if neighbor.bottom >= blank.top:
                    self._rect[index[0] + 1][index[1]] = self._rect[index[0] + 1][index[1]].move([0, -1])
                    self._rect[index[0]][index[1]] = self._rect[index[0]][index[1]].move([0, +1])
                if neighbor.bottom == blank.top:
                    screen.blit(self._board[index[0]][index[1]]._img, self._rect[index[0]][index[1]])
                    inter = self._board[index[0]][index[1]]
                    self._board[index[0]][index[1]] = self._board[index[0] + 1][index[1]]
                    self._board[index[0] + 1][index[1]] = inter

                    inter = self._rect[index[0]][index[1]]
                    self._rect[index[0]][index[1]] = self._rect[index[0] + 1][index[1]]
                    self._rect[index[0] + 1][index[1]] = inter
                    ret = True
        if (direction == 'RIGHT'):
            if (index[1] == 2):
                raise ValueError('Can\'t go Right')
            else:
                neighbor = self._rect[index[0]][index[1] + 1]
                if neighbor.right >= blank.left:
                    self._rect[index[0]][index[1] + 1] = self._rect[index[0]][index[1] + 1].move([-1, 0])
                    self._rect[index[0]][index[1]] = self._rect[index[0]][index[1]].move([1, 0])
                if neighbor.right == blank.left:
                    screen.blit(self._board[index[0]][index[1]]._img, self._rect[index[0]][index[1]])
                    inter = self._board[index[0]][index[1]]
                    self._board[index[0]][index[1]] = self._board[index[0]][index[1] + 1]
                    self._board[index[0]][index[1] + 1] = inter

                    inter = self._rect[index[0]][index[1]]
                    self._rect[index[0]][index[1]] = self._rect[index[0]][index[1] + 1]
                    self._rect[index[0]][index[1] + 1] = inter
                    ret = True
        if (direction == 'LEFT'):
            if (index[1] == 0):
                raise ValueError('Can\'t go Left')
            else:
                neighbor = self._rect[index[0]][index[1] - 1]
                if neighbor.left <= blank.right:
                    self._rect[index[0]][index[1] - 1] = self._rect[index[0]][index[1] - 1].move([+1, 0])
                    self._rect[index[0]][index[1]] = self._rect[index[0]][index[1]].move([-1, 0])
                if neighbor.left == blank.right:
                    screen.blit(self._board[index[0]][index[1]]._img, self._rect[index[0]][index[1]])
                    inter = self._board[index[0]][index[1]]
                    self._board[index[0]][index[1]] = self._board[index[0]][index[1] - 1]
                    self._board[index[0]][index[1] - 1] = inter
                    inter = self._rect[index[0]][index[1]]
                    self._rect[index[0]][index[1]] = self._rect[index[0]][index[1] - 1]
                    self._rect[index[0]][index[1] - 1] = inter
                    ret = True

        for k in range(3):
            for j in range(3):
                if (k == index[0]) and (j == index[1]):
                    continue
                screen.blit(self._board[k][j]._img, self._rect[k][j])
        return ret


    def update(self):
        for k in range(3):
            for j in range(3):
                screen.blit(self._board[k][j]._img, self._rect[k][j])

    def matrix(self):
        mat = []
        for line in self._board:
            for item in line:
                mat.append(int(item._value))
        return mat


def count_inversions(til_ind, board):
    ind = til_ind
    board_length = len(board)
    nb_inv = 0
    while (ind < board_length):
        if board[ind] != 0 and board[ind] < board[til_ind]:
            nb_inv += 0
    return nb_inv


a = pygame.init()
pygame.font.init()

size = width, height = 320, 620

speed = [0, 1]
speed2 = [0, -1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption("GameOf15")
screen.fill((0, 0, 0))

current_working_directory = os.getcwd()
imgPaths = glob.glob(current_working_directory + '/*.png')

imgNames = []
imgs = []
for name in imgPaths:
    l = name.split('/')
    imgNames.append(l[-1])
    imgs.append(pygame.image.load(name))



img = []
l = [i for i in range(9)]
for k in range(9):
    index = random.randint(0, len(l) - 1)
    img.append(imgNames[l.pop(index)])

imgNames = img
print(imgNames)
# imgNames.sort()
# imgNames.reverse()
print(len(img))


b = Board(imgNames)
b.draw_board(screen)

pygame.display.flip()
a = False
c = True
#time.sleep(2)
i = 0
# movement = ['UP', 'UP', 'LEFT', 'LEFT', 'DOWN', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'UP', 'LEFT', 'LEFT', 'DOWN', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'UP', 'LEFT', 'LEFT', 'DOWN', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'UP', 'LEFT', 'LEFT']
print('mat' + str(b.matrix()))

button = pygame.Rect((screen.get_width() / 2) - (150 / 2), screen.get_height() / 2, 150, 50)

movement = []
mouse_pos = None
def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()
smallText = pygame.font.Font("freesansbold.ttf", 20)
textSurf, textRect = text_objects("Start!", smallText)
textRect.center = ( (screen.get_width() / 2), screen.get_height() / 2 + button.height / 2)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button.collidepoint(mouse_pos):
                movement = model.A(3, b.matrix())

    # print('moving ' + movement[i])

    screen.fill((255, 255, 255))
    m_pose = pygame.mouse.get_pos()
    if button.collidepoint(m_pose):
        pygame.draw.rect(screen, [25, 118, 210], button)
    else:
        pygame.draw.rect(screen, [6, 165, 245], button)
    screen.blit(textSurf, textRect)
    b.update()

    if (i < len(movement)):
        a = b.move_blank(movement[i])
    #print(a)
    time.sleep(0.01)
    pygame.display.flip()
    if (a == True) and (i < len(movement)):
        a = False
        i += 1
        time.sleep(0.5)





# print(ball.right)


# default_font = pygame.font.get_default_font()
# font_render = pygame.font.Font(default_font, 15)

# label = font_render.render(str(k), 1, (255, 255, 255))


#        screen.blit(label, (xx, yy))