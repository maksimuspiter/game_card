import os
from random import choice, randrange
from time import sleep

options_health = {1: randrange(1, 3),
          2: randrange(1, 5),
          3: randrange(1, 7),
          4: randrange(1, 9),
          5: randrange(1, 11),
          6: randrange(1, 14)}
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

        def move_cards_by_one_direction(direction: (int, int)):
            """
                Карты перемещаются в одном направлении
                Пока карта, которая должна последовать за картой героя не касается края поля
                count - счетчик перегруппировок карт в одном действии
            """
            x_hero, y_hero = self.get_position_hero()
            x_delta, y_delta = direction

            counter = 0
            while True:

                counter += 1
                old_pos = ((x_hero - x_delta * (counter - 1)), (y_hero - y_delta * (counter - 1)))
                new_pos = (
                    (x_hero + x_delta - x_delta * (counter - 1)), (y_hero + y_delta - y_delta * (counter - 1)))

                self.field[old_pos[0]][old_pos[1]], self.field[new_pos[0]][new_pos[1]] = \
                    EmptyCards(), self.field[old_pos[0]][old_pos[1]]

                # Перемещаем карту героя, а позицию, на которой он находился, занимает пустая карта
                # Проверка: касается ли пустая карта края поля
                if old_pos[0] in (0, self.dimension - 1) or (old_pos[1] in (0, self.dimension - 1)):
                    self.field[x_hero - x_delta * (counter - 1)][y_hero - y_delta * (counter - 1)] = new_card
                    break

        if 0 <= x_hero + x_delta <= (self.dimension - 1) and 0 <= y_hero + y_delta <= (self.dimension - 1):

            absorbed_card = self.field[x_hero + x_delta][y_hero + y_delta]
            hero_card = self.field[x_hero][y_hero]
            """ 
                Change of health depending on the status 
            """
            if absorbed_card.CODE == "GOOD":
                extra = absorbed_card.get_health()
                hero_card.change_health(extra)
            elif absorbed_card.CODE == "BAD":
                extra = absorbed_card.get_health()
                hero_card.change_health(-extra)

            """ 
                Change of hero's position.
                
                !!!!   if the hero does not touch the edge of the map       !!!!
                !!!!   (x_hero and y_hero not in (0, self.dimension-1),     !!!!
                !!!!   the cards behind the vector of his movement move     !!!!
                !!!!   in the same direction as the hero                    !!!!
            """
            new_card = choice([GoodCards(), BadCards(), EmptyCards()])
            edge_map = (0, self.dimension-1)

            # Если стоит в углу
            if x_hero in edge_map and y_hero in edge_map:

                self.field[x_hero][y_hero], self.field[x_hero + x_delta][y_hero + y_delta] = \
                    new_card, self.field[x_hero][y_hero]

            # Если стоит у края, только по одной координате касается границы
            elif x_hero in edge_map or y_hero in edge_map:

                # Если движется по ряду --> карты последуют за героем
                if (x_delta and x_hero - x_delta in range(self.dimension)
                        or y_delta and y_hero - y_delta in range(self.dimension)):

                    counter = 0
                    while True:

                        counter += 1
                        old_pos = ((x_hero - x_delta * (counter - 1)), (y_hero - y_delta * (counter - 1)))
                        new_pos = (
                            (x_hero + x_delta - x_delta * (counter - 1)), (y_hero + y_delta - y_delta * (counter - 1)))

                        self.field[old_pos[0]][old_pos[1]], self.field[new_pos[0]][new_pos[1]] = \
                            EmptyCards(), self.field[old_pos[0]][old_pos[1]]

                        # Перемещаем карту героя, а позицию, на которой он находился, занимает пустая карта
                        # Проверка: касается ли пустая карта УГЛА поля !!!!!!!!!!!!!! В УСЛОВИИ and
                        if old_pos[0] in (0, self.dimension - 1) and (old_pos[1] in (0, self.dimension - 1)):
                            self.field[x_hero - x_delta * (counter - 1)][y_hero - y_delta * (counter - 1)] = new_card
                            break

                else:
                    """
                        Если движется вниз/вверх ↑ ↓ карта последует за героем (только одна).
                        На место карты, которая последует за героем появится новая, случайная карта.
                        
                        Если герой ПОВЫШАЕТ координату по X за ним следует карта координата которой по Y МЕНЬШЕ.
                        Если герой УМЕНЬШАЕТ координату по X за ним следует карта координата которой по Y БОЛЬШЕ.

                        Если герой ПОВЫШАЕТ координату по Y за ним следует карта координата которой по Y БОЛЬШЕ.
                        Если герой УМЕНЬШАЕТ координату по Y за ним следует карта координата которой по Y МЕНЬШЕ.
                    """

                    # Общее перемещение карты героя в нужном направлении и появление карты EmptyCards()
                    self.field[x_hero][y_hero], self.field[x_hero + x_delta][y_hero + y_delta] = \
                        EmptyCards(), self.field[x_hero][y_hero]
                    # move_down
                    # if x_delta == 1:
                    #     pass
                    #
                    # # move_up
                    # elif x_delta == -1:
                    #     pass
                    #
                    # # move_right
                    # elif y_delta == 1:
                    #     pass
                    #
                    # # move_left
                    # elif y_delta == -1:
                    #     pass
                    x_delta_new, y_delta_new = -y_delta, -x_delta

                    self.field[x_hero][y_hero], self.field[x_hero + x_delta_new][y_hero + y_delta_new] = \
                        self.field[x_hero + x_delta_new][y_hero + y_delta_new], new_card

            # не касается края поля
            else:
                move_cards_by_one_direction(direction)

            # Change position of the hero
            ##
            ###
            ####
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

    def __str__(self):
        return f'{self.IMG_CARD_TEST}{self.health}'


class Hero(Card):
    """
        🥷 🕵 👮 🤴 👸 👲
    """
    list_hero = ["🥷", "🕵", "👮", "🤴", "👸", "👲"]
    CODE = 'hero'
    IMG_CARD_TEST = choice(list_hero)
    IMG_CARD_TEST = IMG_CARD_TEST
    STATUS = "HERO"

    # def __new__(cls, *args, **kwargs):
    #     print("I'm a hero")
    #     return super().__new__(cls, *args, **kwargs)

    def __init__(self, health):
        self.health = health

    def __str__(self):
        return self.IMG_CARD_TEST
        # return (f"______\n"
        #       f"| {self.IMG_CARD_TEST} |\n"
        #       f"| {self.health} |\n"
        #       f"¯¯¯¯¯¯")

    def show_hero_card(self):
        print(f"{'_' * 6}\n"
              f"|{' ' * 4}|\n"
              f"{'| '}{self.IMG_CARD_TEST}{' |'}\n"
              f"|{' '}{self.health if self.health // 10 > 0 else ' ' + str(self.health)}{' '}|\n"
              f"|{' ' * 4}|\n"
              f"{'¯' * 6}\n"
              f"Health: {self.health}")

    def change_health(self, extra):
        self.health += extra


class EmptyCards(Card):
    STATUS = "EMPTY"
    IMG_CARD_TEST = '  '

    def __str__(self):
        return self.IMG_CARD_TEST


class GoodCards(Card):

    CODE = 'GOOD'
    IMG_CARD_TEST = f'+'
    STATUS = "GOOD"
    health = {1: randrange(1, 3),
              2: randrange(1, 5),
              3: randrange(1, 7),
              4: randrange(1, 9),
              5: randrange(1, 11),
              6: randrange(1, 14)}

    def __init__(self, level_field=4):
        self.level_field = level_field
        self.health = options_health[int(self.level_field)]



class BadCards(Card):

    CODE = "BAD"
    IMG_CARD_TEST = '-'
    STATUS = "GOOD"
    health = {1: randrange(1, 3),
              2: randrange(1, 5),
              3: randrange(1, 7),
              4: randrange(1, 9),
              5: randrange(1, 11),
              6: randrange(1, 14)}

    def __init__(self, level_field=4):
        self.level_field = level_field
        self.health = self.health[int(self.level_field)]


class Coin(GoodCards):
    CODE = 'COIN'


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
    hero.show_hero_card()

    while True:
        if move():
            break
        os.system('cls||clear')
        f1.show_field()
        print()
        hero.show_hero_card()


if __name__ == '__main__':
    play()
