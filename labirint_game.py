import random
import pygame
import time


class Labirint():
    def __init__(self, x=20, y=15):
        self.__record_time = None
        self.__start_time = time.time()
        self.__player = None
        self.__matrix = None
        self.__start = None
        self.__finish = None
        self.__matrix_base = None

        self.__border = 5
        self.__width_line = 40
        self.__width_walls = 5
        self.__color_way = (255, 255, 255)
        self.__color_wall = (0, 0, 0)
        self.__color_player = (0, 0, 255)
        self.__color_start = (0, 255, 0)
        self.__color_finish = (255, 0, 0)
        self.__trace = False
        self.__color_trace = (0, 0, 255)
        self.__width = x
        self.__height = y
        self.__width_window = ((self.__width * 2 - 1) // 2 + 1) * self.__width_line + ((self.__width * 2 - 1) // 2) * self.__width_walls + self.__border * 2
        self.__height_window = ((self.__height * 2 - 1) // 2 + 1) * self.__width_line + ((self.__height * 2 - 1) // 2) * self.__width_walls + self.__border * 2
        self.__info = True
        self.__score = 0
        self.__t = 0
        self.__record_time = 9999
        if self.__width < 10:
            self.__info = False
        if self.__info:
            self.__height_window += 70
        self.__matrix_base = []

        pygame.init()
        self.__window = pygame.display.set_mode((self.__width_window, self.__height_window))
        pygame.display.set_caption("Лабиринт")
        self.__font = pygame.font.Font(None, 25)
        self.__flag_game = True
        self.__matrix, self.__start, self.__finish = self.__create_labyrinth(self.__width, self.__height)
        self.__k = 0

        def hello():
            pass

        def create_labyrinth(n=5, m=5):
            """Генерация лабиринта"""
            reach_matrix = []
            for i in range(n):  # создаём матрицу достижимости ячеек
                reach_matrix.append([])
                for j in range(m):
                    reach_matrix[i].append(False)
            transition_matrix = []
            for i in range(n * 2 - 1):  # заполнение матрицы переходов
                transition_matrix.append([])
                for j in range(m * 2 - 1):
                    if i % 2 == 0 and j % 2 == 0:
                        transition_matrix[i].append(True)
                    else:
                        transition_matrix[i].append(False)
            start = self.start_point_generate(n, m)
            finish = self.finish_point_generate(start, n, m)
            list_transition = [start]
            print(start)
            x, y = start
            reach_matrix[x][y] = True
            x, y, tx, ty = self.transition_choice(x, y, reach_matrix)
            for i in range(1, m * n):
                while not (x >= 0 and y >= 0):
                    x, y = list_transition[-1]
                    list_transition.pop()
                    x, y, tx, ty = self.transition_choice(x, y, reach_matrix)
                reach_matrix[x][y] = True
                list_transition.append((x, y))
                transition_matrix[tx][ty] = True
                x, y, tx, ty = self.transition_choice(x, y, reach_matrix)
            return transition_matrix, start, finish  # возвращаем матрицу проходов и начальную точку