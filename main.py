import os
from random import choice, randrange


class GameField:

    def __init__(self, dimension=3, level_field=1):
        self.dimension = dimension
        self.field = None
        self.position_hero = None
        self.level_field = level_field

    def create_field(self):
        self.field = [[[None] for _ in range(self.dimension)] for _ in range(self.dimension)]

    def show_field(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                print(self.field[i][j], end='')
            print()

    def add_hero(self, hero):
        if self.position_hero:
            raise Exception("The hero already exists")
        for i in range(self.dimension):
            for j in range(self.dimension):
                if i == j == self.dimension // 2:
                    self.field[i][j] = hero
                else:
                    self.field[i][j] = choice([GoodCards(), BadCards()])
        pos = self.dimension // 2
        self.position_hero = (pos, pos)

    def get_position_hero(self):
        return self.position_hero

    def move(self, direction: (int, int)):
        x_hero, y_hero = self.get_position_hero()
        x_delta, y_delta = direction

        if 0 <= x_hero + x_delta <= (self.dimension - 1) and 0 <= y_hero + y_delta <= (self.dimension - 1):

            absorbed_card = self.field[x_hero + x_delta][y_hero + y_delta]
            horo_card = self.field[x_hero][y_hero]
            if absorbed_card.STATUS:
                extra_health = absorbed_card.get_extra_health()
                horo_card.change_health(extra_health)
            self.field[x_hero][y_hero], self.field[x_hero + x_delta][y_hero + y_delta] = \
                choice([GoodCards(), BadCards()]), self.field[x_hero][y_hero]
            self.position_hero = (x_hero + x_delta, y_hero + y_delta)


class Card:
    """
    CODE - card's short description
    IMG_CARD - path to file
    IMG_CARD_TEST - Unicode symbol
    STATUS - GOOD // BAD  // HERO // NEUTRAL
    health - health points
    extra_health - extra health points absorbed card (what happens if hero eat this card)
    level_field - change range of health and extra_health GOOD and BAD cards can be on field
    level_card - change characteristic of Card
    """
    CODE = None
    IMG_CARD = None
    IMG_CARD_TEST = None
    STATUS = None
    health = None
    extra_health = None
    level_field = None
    level_card = None

    def get_health(self):
        return self.health

    def get_extra_health(self):
        return self.extra_health

    def __str__(self):
        return f'{self.IMG_CARD_TEST}{abs(self.extra_health)}'


class Hero(Card):
    """
        🥷 🕵 👮 🤴 👸 👲
    """
    list_hero = ["🥷", "🕵", "👮", "🤴", "👸", "👲"]
    CODE = 'hero'
    IMG_CARD_TEST = choice(list_hero)
    STATUS = "HERO"

    # def __new__(cls, *args, **kwargs):
    #     print("I'm a hero")
    #     return super().__new__(cls, *args, **kwargs)

    def __init__(self, health):
        self.health = health

    def __str__(self):
        return self.IMG_CARD_TEST

    def change_health(self, extra_health):
        self.health += extra_health


class EmptyCards(Card):
    STATUS = "EMPTY"
    IMG_CARD_TEST = '  '

    def __str__(self):
        return self.IMG_CARD_TEST


class GoodCards(Card):

    CODE = 'GOOD'
    IMG_CARD_TEST = f'+'
    STATUS = "GOOD"

    def __init__(self, level_field=1):
        self.health = 2
        self.extra_health = randrange(1, 6)
        self.level_field = level_field

    def get_health(self):
        return self.extra_health


class BadCards(Card):

    CODE = "BAD"
    IMG_CARD_TEST = '-'
    STATUS = "GOOD"

    def __init__(self, level_field=1):
        self.health = 2
        self.extra_health = -randrange(1, 6)
        self.level_field = level_field

    def get_health(self):
        return self.extra_health


def play():

    def move():

        def move_up():
            return -1, 0

        def move_down():
            return 1, 0

        def move_left():
            return 0, -1

        def move_right():
            return 0, 1

        direction = input().strip().lower()
        if direction in ("w", "up", "8", "ц"):
            f1.move(move_up())
        elif direction in ("s", "down", "5", "ы"):
            f1.move(move_down())
        elif direction in ("a", "left", "4", "ф"):
            f1.move(move_left())
        elif direction in ("d", "right", "6", "в"):
            f1.move(move_right())
        elif direction == "stop":
            return True
    f1 = GameField(randrange(3, 6))
    f1.create_field()
    hero = Hero(10)

    f1.add_hero(hero)
    f1.show_field()
    print()
    print('Health', hero.get_health())
    print()
    while True:
        if move():
            break
        os.system('cls||clear')
        f1.show_field()
        print()
        print(f'Health: {hero.get_health()}')


if __name__ == '__main__':
    play()
