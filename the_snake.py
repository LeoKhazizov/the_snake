"""Скрипт, представляющий из себя игру Змейку.

Правила игры:
Змейка движется по полю, поедая яблоки.
Яблоки увеличивают длину змейки на 1 сегмент.
Также на поле генерируются препятствия.
Препятствия уменьшают длину змейки.
Пока змейка не столкнулась с собой, игра продолжается.
"""
from random import choice, randrange

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет яда
POISON_COLOR = (0, 255, 0)

# Цвет камня
ROCK_COLOR = (192, 192, 192)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов.

    Атрибуты:
            position: координаты объекта.
            body_color: цвет объекта.
    """

    def __init__(self):
        """Инициализатор класса.

        Задаёт значения:
            Атрибуту позиции объекта.
            Атрибуту цвета.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def randomize_position(self, taken_spots):
        """Метод, используемый в дочерних классах.

        Создает случайные координаты объекту.
        """
        while True:
            position = (
                randrange(GRID_SIZE, SCREEN_WIDTH, GRID_SIZE),
                randrange(GRID_SIZE, SCREEN_HEIGHT, GRID_SIZE),
            )
            if position not in taken_spots:
                return position

    def draw(self):
        """Пустой метод, переопредленный в дочерних классах.

        Отрисовывает объекты на поле.
        """


class Apple(GameObject):
    """Дочерний класс GameObject.

    Отвечает за объекты удлиняющие змейку.
    Атрибуты:
            Те же, что у родителя GameObject.
    """

    def __init__(self, taken_spots):
        """Инициализатор класса.

        Задаёт значения:
            Атрибуту позиции объекта.
            Атрибуту цвета.
        Конструктор класса принимает taken_spots.
        Переменную, нужную для правильного определния позиции.
        """
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(taken_spots)

    def draw(self):
        """Метод, отрисовывающий объекты класса."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Barriers(GameObject):
    """Дочерний класс GameObject.

    Отвечает за объекты-препятствия.
    Атрибуты:
            Те же, что у родителя GameObject.
            Один новый атрибут.
            barrier_type: определяет тип препятствия.
    """

    def __init__(self, taken_spots):
        """Инициализатор класса.

        Задаёт значения:
            Атрибуту типа баррьера.
            Атрибуту цвета объекта.
            Атрибуту позиции объекта.
        Конструктор класса принимает taken_spots.
        Переменную, нужную для правильного определния позиции.
        """
        self.barrier_type, self.body_color = self.set_values()
        self.position = self.randomize_position(taken_spots)

    def set_values(self):
        """Метод, задающий тип и цвет объекта."""
        rock_or_posion = choice(('rock', 'poison'))
        color = POISON_COLOR if rock_or_posion == 'poison' else ROCK_COLOR
        return rock_or_posion, color

    def draw(self):
        """Метод, отрисовывающий объекты класса."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс GameObject.

    Создает объект змейку.
    Атрибуты:
            positions: Координаты сегментов змейки.
            length: Длина змейки.
            last: Координаты последнего сегмента змейки.
            direction: Направление движения.
            next_direction: Следующее направление движения.
            color_chart: Список вариантов цветов змейки.
            body_color: Цвет змейки.
    """

    def __init__(self):
        """Инициализатор класса.

        Задаёт значения:
            Атрибуту позиции объекта.
            Атрибуту позиции сегментов объекта.
            Атрибуту длины объекта.
            Атрибуту позиции последнего сегмента.
            Атрибуту направления движения.
            Атрибуту нового направления движения.
            Атрибуту вариантов цвета объекта.
            Атрибуту цвета объекта.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 1
        # Атрибут позиции последних сегментом переделан в список.
        # Чтобы можно было удалять несколько элементов.
        # Это нужно при столкновении с камнем.
        self.last = []
        self.direction = RIGHT
        self.next_direction = None
        self.color_chart = [
            (255, 255, 0),
            (255, 0, 255),
            (0, 0, 255),
            (0, 255, 255)
        ]
        self.body_color = self.pick_color()

    def pick_color(self):
        """Метод выбора случайного цвета змейки из color_chart."""
        return choice(self.color_chart)

    def update_direction(self):
        """Метод, обновляющий текущее направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения змейки."""
        delta_x, delta_y = self.direction
        start_x, start_y = self.get_head_position()
        new_head_position = (
            (start_x + GRID_SIZE * delta_x) % SCREEN_WIDTH,
            (start_y + GRID_SIZE * delta_y) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if self.length < len(self.positions):
            self.last = [self.positions.pop()]
        else:
            self.last = []

    def eat_apple(self):
        """Метод позволяющий змейке есть яблоки."""
        tail_x, tail_y = self.positions[self.length - 1]
        x_delta, y_delta = self.direction
        new_segment = (
            tail_x - (x_delta * GRID_SIZE),
            tail_y - (y_delta * GRID_SIZE)
        )
        self.positions.append(new_segment)
        self.length += 1

    def barrier_interaction(self, barrier_type):
        """Метод задает взаимодействие змейки с барьерами."""
        if barrier_type == 'poison':
            poisoned_segment = self.positions.pop()
            self.length -= 1
            self.last.append(poisoned_segment)
        else:
            self.last += self.positions
            self.positions = [self.get_head_position()]
            self.length = 1

    def draw(self):
        """Метод, отрисовывающий объекты класса."""
        if self.last:
            for position in self.last:
                last_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
                pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Метод, определяющий положение головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сброса змейки в исходное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.last = []
        self.body_color = self.pick_color()
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(snake):
    """Функция обработки пользовтельского ввода."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit('User quit the game.')
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def asp_bit_itself(asp):
    """Функция проверяющая не укусила змейка себя."""
    if asp.get_head_position() in asp.positions[1:]:
        asp.reset()


def update_taken_spots(asp, apple, bar_one, bar_two, bar_three):
    """Функция, обновляющая список занятых мест."""
    updated_taken_spots = []
    for position in asp.positions:
        updated_taken_spots.append(position)
    updated_taken_spots.extend([
        apple.position,
        bar_one.position,
        bar_two.position,
        bar_three.position
    ])
    return updated_taken_spots


def has_snake_eaten(asp, apple, taken_spots):
    """Функция, проверяющая не съела ли змейка яблоко.

    В случае столкновения вызывает соответсвующий метод змейки.
    """
    if apple.position == asp.get_head_position():
        asp.eat_apple()
        apple.position = apple.randomize_position(taken_spots)


def has_snake_crashed(asp, bar_one, bar_two, bar_three, taken_spots):
    """Функция, проверяющая, врезалась ли змейка в барьер.

    В случае столкновения вызывает соответсвующий метод змейки.
    """
    if asp.length > 1:
        all_barriers = [bar_one, bar_two, bar_three]
        for barrier in all_barriers:
            if barrier.position in asp.positions:
                asp.barrier_interaction(barrier.barrier_type)
                barrier.position = barrier.randomize_position(taken_spots)


def main():
    """Создаем скрипт, собирая вместе вышеописанные элементы."""
    pg.init()

    asp = Snake()
    taken_spots = [asp.position]

    apple = Apple(taken_spots)
    taken_spots = taken_spots + [apple.position]

    barrier_one = Barriers(taken_spots)
    taken_spots += [barrier_one.position]
    barrier_two = Barriers(taken_spots)
    taken_spots += [barrier_two.position]
    barrier_three = Barriers(taken_spots)
    taken_spots += [barrier_three.position]

    while True:
        clock.tick(SPEED)
        asp.update_direction()
        handle_keys(asp)
        asp.update_direction()
        asp.move()
        taken_spots = update_taken_spots(
            asp,
            apple,
            barrier_one,
            barrier_two,
            barrier_three
        )

        has_snake_eaten(asp, apple, taken_spots)

        has_snake_crashed(
            asp,
            barrier_one,
            barrier_two,
            barrier_three,
            taken_spots
        )

        taken_spots = update_taken_spots(
            asp,
            apple,
            barrier_one,
            barrier_two,
            barrier_three
        )

        if asp.get_head_position() in asp.positions[1:]:
            asp.reset()
            taken_spots = [asp.position]

            # Новый экзепляр не создаю, так нужна только новая позиция.
            apple.position = apple.randomize_position(taken_spots)
            taken_spots = taken_spots.append(apple.position)

            # Создаю именно новые объекты, чтобы изменить и тип, и позицию.
            barrier_one = Barriers(taken_spots)
            taken_spots += [barrier_one.position]
            barrier_two = Barriers(taken_spots)
            taken_spots += [barrier_two.position]
            barrier_three = Barriers(taken_spots)
            taken_spots += [barrier_three.position]

            screen.fill(BOARD_BACKGROUND_COLOR)

        asp.draw()
        apple.draw()
        barrier_one.draw()
        barrier_two.draw()
        barrier_three.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
