import pygame
import random


#Основные параметры
SQUARE_COLOR = pygame.Color("blue")  # цвет квадратов
TEXT_COLOR = pygame.Color("white")  # цвет текста
BG_MAIN_COLOR = (3, 0, 65)  # цвет фона на основном экране
BG_WIN_COLOR = (53, 231, 167)  # цвет фона на экране после победы
BUTTON_COLOR = (3, 0, 96)  # цвет кнопки
SPEED = 4  # скорость перемещения


class Board:
    def __init__(self, width, height):
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size = 80
        self.correct = [int(i) for i in range(1, self.width * self.height)] + ['']  # прравильная комбинация
        pygame.font.init()
        self.count = 0  # счетчик ходов
        self.winning = False

    def set_view(self, left, top, cell_size):  # параметры окна
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def check(self, num):   # проверка првильности поля
        summ = num.index('') // self.width + 1
        del num[num.index('')]
        for i in num[:-1]:
            for j in num[num.index(i):]:
                if i > j:
                    summ += 1
        if summ % 2 == 0:
            return True
        else:
            return False

    def write_text(self, size, string, x, y):   # вывод текста на экран, аргументы: размер шрифта, текст, x и y центра
        text = pygame.font.Font(None, size).render(string, True, TEXT_COLOR)
        text_rectangle = text.get_rect()
        text_rectangle.center = (x, y)
        screen.blit(text, text_rectangle)

    def get_cell(self, mouse_pos):  # проверка есть ли клетка по данной координате
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if x < 0 or y < 0 or self.width <= x or self.height <= y:
            return None
        return x, y

    def generate_new(self):  # генерация новой комбинации поля
        self.numbers = self.correct[:]
        self.winning = False
        self.count = 0
        correct = False
        while not correct:
            random.shuffle(self.numbers)
            correct = self.check(self.numbers[:])

    def render(self):   # рендеринг поля
        if self.winning:
            self.win()
            return None
        pygame.draw.rect(screen, BUTTON_COLOR, (self.left * 2 + self.cell_size * self.width, self.top,
                                                self.cell_size * 2, self.cell_size))
        self.write_text(40, 'Новая игра', self.left * 2 + self.cell_size * self.width + self.cell_size,
                        self.top + self.cell_size // 2)
        self.write_text(40, 'Ходы:' + str(self.count), self.left * 2 + self.cell_size * self.width + self.cell_size,
                        self.top + self.cell_size * 2)
        for j in range(self.height):    # вывод клеток пятнашек
            for i in range(self.width):
                if self.numbers[j * self.height + i] != '':
                    pygame.draw.rect(screen, SQUARE_COLOR,
                                     (self.left + i * self.cell_size,
                                      self.top + j * self.cell_size,
                                      self.cell_size, self.cell_size))
                    self.write_text(36, str(self.numbers[j * self.height + i]), self.left + i * self.cell_size + self.cell_size // 2,
                                    self.top + j * self.cell_size + self.cell_size // 2)

    def move(self, mouse_pos):  # передвижение клеток
        movex = self.left + self.get_cell(mouse_pos)[0] * self.cell_size
        movey = self.top + self.get_cell(mouse_pos)[1] * self.cell_size
        moving = 'nothing'
        mouse_pos_x_cell = self.get_cell(mouse_pos)[0]
        mouse_pos_y_cell = self.get_cell(mouse_pos)[1]
        # определение направления движения
        if mouse_pos_y_cell * self.height + mouse_pos_x_cell - self.numbers.index('') == -self.width:
            moving = 'down'
        elif mouse_pos_y_cell * self.height + mouse_pos_x_cell - self.numbers.index('') == self.width:
            moving = 'up'
        elif mouse_pos_y_cell * self.height + mouse_pos_x_cell - self.numbers.index('') == 1 and \
                self.numbers.index('') - (self.height - 1) % self.height != 0:
            moving = 'left'
        elif mouse_pos_y_cell * self.height + mouse_pos_x_cell - self.numbers.index('') == -1 and \
                self.numbers.index('') % self.height != 0:
            moving = 'right'
        if moving == 'nothing':
            return None
        # изменения списка с порядком чисел
        new_ind_space = self.get_cell(mouse_pos)[1] * self.height + self.get_cell(mouse_pos)[0]
        new_ind_num = self.numbers.index('')
        newnum = self.numbers[new_ind_space]
        self.numbers[new_ind_space] = ''
        self.numbers[new_ind_num] = newnum
        # сама анимация
        newx = movex
        newy = movey
        for i in range(0, self.cell_size, self.cell_size // SPEED):
            pygame.draw.rect(screen, BG_MAIN_COLOR, (newx, newy, self.cell_size, self.cell_size))
            if moving == 'down':
                pygame.draw.rect(screen, SQUARE_COLOR, (movex, movey + i, self.cell_size, self.cell_size))
                newy += i
                self.write_text(36, str(newnum), movex + self.cell_size // 2, movey + i + self.cell_size // 2)
            elif moving == 'up':
                pygame.draw.rect(screen, SQUARE_COLOR, (movex, movey - i, self.cell_size, self.cell_size))
                newy -= i
                self.write_text(36, str(newnum), movex + self.cell_size // 2, movey - i + self.cell_size // 2)
            elif moving == 'right':
                pygame.draw.rect(screen, SQUARE_COLOR, (movex + i, movey, self.cell_size, self.cell_size))
                newx += i
                self.write_text(36, str(newnum), movex + i + self.cell_size // 2, movey + self.cell_size // 2)
            elif moving == 'left':
                pygame.draw.rect(screen, SQUARE_COLOR, (movex - i, movey, self.cell_size, self.cell_size))
                newx -= i
                self.write_text(36, str(newnum), movex - i + self.cell_size // 2, movey + self.cell_size // 2)
            pygame.display.flip()
            self.clock.tick(30)
        self.count += 1    # увеличение количества ходов
        if self.numbers == self.correct:    # проверка на то, являялся ли ход последним для победы
            self.winning = True
            self.win()

    def win(self):  # вывод окна, уведомляющее о победе
        screen.fill(BG_WIN_COLOR)
        self.write_text(70, 'ПОБЕДА', 350, 170)
        self.write_text(70, 'ХОДОВ:' + str(self.count), 350, 230)
        self.write_text(36, 'Нажмите в люое место или Enter для нвой игры', 350, 300)

    def clicked(self, mouse_pos):   # действия, доступные по нажатию на экран
        if self.get_cell(mouse_pos) and not self.winning:
            board.move(mouse_pos)
        elif self.winning:
            self.winning = False
            self.generate_new()
        else:
            x, y = mouse_pos
            if (x >= self.left * 2 + self.cell_size * self.width and
                x <= self.left * 2 + 3 * self.cell_size * self.width and
                y >= self.top and
                y <= self.top + self.cell_size):
                self.generate_new()

    def actions_by_keys(self, key):    #управление клавитурой
        if not self.winning:    # если еще не победа, то принммаются 4 кнопки для управления полем
            if key == pygame.K_LEFT and (self.numbers.index('') - self.width + 1) % self.height != 0:
                self.move([self.left + (self.numbers.index('') + 1) % self.height * self.cell_size + self.cell_size // 2,
                           self.top + (self.numbers.index('') + 1) // self.height * self.cell_size + self.cell_size // 2])
            elif key == pygame.K_RIGHT and self.numbers.index('') % self.height != 0:
                self.move([self.left + (self.numbers.index('') - 1) % self.height * self.cell_size + self.cell_size // 2,
                           self.top + (self.numbers.index('') - 1) // self.height * self.cell_size + self.cell_size // 2])
            elif key == pygame.K_UP and self.numbers.index('') < (self.width * self.height - self.width):
                self.move([self.left + (self.numbers.index('') + self.width) % self.height * self.cell_size + self.cell_size // 2,
                           self.top + (self.numbers.index('') + self.width) // self.height * self.cell_size + self.cell_size // 2])
            elif key == pygame.K_DOWN and self.numbers.index('') > self.width - 1:
                self.move([self.left + (self.numbers.index('') - self.width) % self.height * self.cell_size + self.cell_size // 2,
                           self.top + (self.numbers.index('') - self.width) // self.height * self.cell_size + self.cell_size // 2])
        elif key == pygame.K_RETURN:    # по нажатию кнопки Enter запускается новая игра
            self.winning = False
            self.generate_new()


screen = pygame.display.set_mode((700, 500))
board = Board(4, 4)
board.set_view(100, 100, 80)
pygame.display.set_caption('Пятнашки')
running = True
board.generate_new()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.clicked(event.pos)
        if event.type == pygame.KEYDOWN:
            board.actions_by_keys(event.key)
        screen.fill((3, 0, 65))
        board.render()
        pygame.display.flip()
pygame.quit()
