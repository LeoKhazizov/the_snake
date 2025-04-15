
from random import choice, randrange
import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Атрибуты:
            position: координаты объекта.
            body_color: цвет объекта.
    """

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def randomize_position(self):
        """
        Метод, используемый в дочерних классах,
        чтобы создать случайные координаты объекту.
        """
        return (
            randrange(20, SCREEN_WIDTH, GRID_SIZE),
            randrange(20, SCREEN_HEIGHT, GRID_SIZE),
        )

    def draw(self):
        """
        Пустой метод, переопредленный в дочерних классах,
        отрисовывающий объекты на поле.
        """
        pass


class Apple(GameObject):
    """
    Дочерний класс GameObject,
    отвечает за объекты удлиняющие змейку.

    Атрибуты:
            Те же, что у родителя GameObject.
    """

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = self.set_position()

    def set_position(self):
        """Метод, задающий случайную позицию."""
        return GameObject.randomize_position(self)

    def draw(self):
        """Метод, отрисовывающий объекты класса."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Barriers(GameObject):
    """
    Дочерний класс GameObject,
    отвечает за объекты-препятствия.

    Атрибуты:
            Те же, что у родителя GameObject.
            Один новый атрибут.
            barrier_type: определяет тип препятствия.
    """

    def __init__(self):
        self.position, self.barrier_type, self.body_color = self.set_values()

    def set_values(self):
        """Метод, задающий случайную позицию, тип и цвет объекта."""
        coordinates = GameObject.randomize_position(self)
        rock_or_posion = choice(['rock', 'poison'])
        color = POISON_COLOR if rock_or_posion == 'poison' else ROCK_COLOR
        return coordinates, rock_or_posion, color

    def draw(self):
        """Метод, отрисовывающий объекты класса."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Дочерний класс GameObject,
    создает объект змейку.

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
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 1
        self.last = None
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
        if self.direction == RIGHT:
            new_head_position = (
                self.positions[0][0] + GRID_SIZE,
                self.positions[0][1]
            )
            self.positions.insert(0, new_head_position)
            self.last = self.positions.pop(-1)
        elif self.direction == LEFT:
            new_head_position = (
                self.positions[0][0] - GRID_SIZE,
                self.positions[0][1]
            )
            self.positions.insert(0, new_head_position)
            self.last = self.positions.pop(-1)
        elif self.direction == DOWN:
            new_head_position = (
                self.positions[0][0],
                self.positions[0][1] + GRID_SIZE
            )
            self.positions.insert(0, new_head_position)
            self.last = self.positions.pop(-1)
        elif self.direction == UP:
            new_head_position = (
                self.positions[0][0],
                self.positions[0][1] - GRID_SIZE
            )
            self.positions.insert(0, new_head_position)
            self.last = self.positions.pop(-1)

    def draw(self):
        """Метод, отрисовывающий объекты класса."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод определяющий положение головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сброса игры в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.body_color = self.pick_color()
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def is_on_screen(game_object):
    """Функция проверяет находиться ли змейка в пределах экрана."""
    on_screen = True
    for i in game_object.positions:
        if i[0] < 0 or i[0] > SCREEN_WIDTH - GRID_SIZE:
            on_screen = False
        elif i[1] < 0 or i[1] > SCREEN_HEIGHT - GRID_SIZE:
            on_screen = False
    return on_screen


def handle_keys(snake):
    """Функция обработки пользовтельского ввода."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if is_on_screen(snake):
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT


def asp_return_cycle(snake):
    """
    Функция, обеспечивающая проход змейки через край и выход с другого.
    Проверяет координаты хвоста и перемещает змеку по частям.
    """
    tail = snake.positions[snake.length - 1]

    if snake.direction == LEFT and tail[0] < 0:
        x_coordinate, y_coordinate = (SCREEN_WIDTH, tail[1])
        for i in range(len(snake.positions) - 1, -1, -1):
            x_coordinate += GRID_SIZE
            snake.positions[i] = (x_coordinate, y_coordinate)

    elif snake.direction == RIGHT and tail[0] > SCREEN_WIDTH:
        x_coordinate, y_coordinate = (0, tail[1])
        for i in range(len(snake.positions) - 1, -1, -1):
            x_coordinate = SCREEN_WIDTH - snake.positions[i][0]
            snake.positions[i] = (x_coordinate, y_coordinate)

    elif snake.direction == DOWN and tail[1] > SCREEN_HEIGHT:
        x_coordinate, y_coordinate = (tail[0], 0)
        for i in range(len(snake.positions) - 1, -1, -1):
            y_coordinate = SCREEN_HEIGHT - snake.positions[i][1]
            snake.positions[i] = (x_coordinate, y_coordinate)

    elif snake.direction == UP and tail[1] < 0:
        x_coordinate, y_coordinate = (tail[0], SCREEN_HEIGHT)
        for i in range(len(snake.positions) - 1, -1, -1):
            y_coordinate += GRID_SIZE
            snake.positions[i] = (x_coordinate, y_coordinate)


def eat_apple(asp, apple):
    """Функция позволяющая змейке есть яблоки."""
    head_x, head_y = asp.get_head_position()
    if asp.direction == RIGHT:
        new_segment = (head_x - GRID_SIZE, head_y)
        asp.positions.insert(1, new_segment)
        asp.length += 1
        for i in asp.positions[asp.length - 1:1:-1]:
            i = (i[0] - GRID_SIZE, i[1])
    elif asp.direction == LEFT:
        new_segment = (head_x + GRID_SIZE, head_y)
        asp.positions.insert(1, new_segment)
        asp.length += 1
        for i in asp.positions[asp.length - 1:1:-1]:
            i = (i[0] + GRID_SIZE, i[1])
    elif asp.direction == UP:
        new_segment = (head_x, head_y - GRID_SIZE)
        asp.positions.insert(1, new_segment)
        asp.length += 1
        for i in asp.positions[asp.length - 1:1:-1]:
            i = (i[0], i[1] - GRID_SIZE)
    elif asp.direction == DOWN:
        new_segment = (head_x, head_y + GRID_SIZE)
        asp.positions.insert(1, new_segment)
        asp.length += 1
        for i in asp.positions[asp.length - 1:1:-1]:
            i = (i[0], i[1] + GRID_SIZE)
    eaten_apple = pygame.Rect(apple.position, (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, eaten_apple)
    return Apple()


def barrier_interaction(asp, barrier):
    """Функция задает взаимодействие змейки с барьерами."""
    if barrier.barrier_type == 'rock':
        for i in range(asp.length - 1, 0, -1):
            broken_segment = asp.positions.pop(i)
            last_rect = pygame.Rect(broken_segment, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        asp.length = 1

        asp.positions = [asp.get_head_position()]
        asp.length = 1
    else:
        poisoned_segment = asp.positions.pop(asp.length - 1)
        asp.length -= 1
        last_rect = pygame.Rect(poisoned_segment, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    used_barrier = pygame.Rect(barrier.position, (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, used_barrier)
    return Barriers()


def asp_bit_itself(asp):
    """Функция проверяющая не укусила змейка себя."""
    if is_on_screen(asp):
        for i in asp.positions[1:]:
            if i == asp.get_head_position():
                asp.reset()


def main():
    """Входная точка программы."""
    pygame.init()

    asp = Snake()

    apple = Apple()

    barrier_one, barrier_two, barrier_three = (Barriers() for _ in range(3))

    while True:
        """Основной игровой цикл."""
        clock.tick(SPEED)
        handle_keys(asp)
        asp.draw()
        apple.draw()
        barrier_one.draw()
        barrier_two.draw()
        barrier_three.draw()
        asp.update_direction()
        asp.move()
        asp.draw()
        if apple.position == asp.get_head_position():
            apple = eat_apple(asp, apple)
        elif asp.length > 1:
            if barrier_one.position == asp.get_head_position():
                barrier_one = barrier_interaction(asp, barrier_one)
            if barrier_two.position == asp.get_head_position():
                barrier_two = barrier_interaction(asp, barrier_two)
            if barrier_three.position == asp.get_head_position():
                barrier_three = barrier_interaction(asp, barrier_three)
        else:
            asp_bit_itself(asp)
        asp_return_cycle(asp)
        pygame.display.update()


if __name__ == '__main__':
    """Запуск скрипта."""
    main()
