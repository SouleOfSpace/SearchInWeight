import random
from collections import deque
import time

import pygame


def update_vertical_matrix(matrix):
    '''переводим вертикальную матрицу в массив с кортежами смежных стен (для генерации горизонтальной матрицы)'''
    res = []
    for r_index, row in enumerate(matrix):
        counter = 1
        arr = []
        res.append([])

        for c_index, colm in enumerate(row):
            arr.append(counter)
            if colm == 1 and len(arr) > 1:
                res[r_index].append(arr)
                arr = []
                counter = c_index + 2
                continue
            elif colm == 1:
                arr = []
                res[r_index].append(counter)
                counter = c_index + 2

    return res


def update_vertical_matrix_level_2(rows, cols, v_matrix, h_matrix):
    '''добавляем случайные проходы  в вертикальную матрицу для усложнения лабиринта'''
    flag = (rows+cols)//5

    for row in range(2, rows-1):
        if not flag: break
        for col in range(1, cols-1):
            if not flag: break
            if v_matrix[row][col] == 1 and v_matrix[row-1][col] == 1 and v_matrix[row-2][col] and h_matrix[row][col] == 1 and h_matrix[row-1][col] == 0:
                v_matrix[row-1][col] = 0
                flag -=1

    for i in range(len(v_matrix[-3])):
        if v_matrix[-1][i] == 0 and v_matrix[-2][i] == 0 and v_matrix[-3][i] == 0 and h_matrix[-1][i] == 1 and h_matrix[-2][i] == 0:
         v_matrix[-1][i] = 1

    return v_matrix


def create_finish_point(v_matrix, h_matrix, start):
    '''pass'''
    finish = start
    while abs(finish[1] - start[1]) < len(v_matrix)//3:
        if start[1] < len(v_matrix)//2:
            finish = (len(v_matrix)-1, random.randrange(len(v_matrix)//2, len(h_matrix)))
        else:
            finish = (len(v_matrix)-1, random.randrange(0, len(v_matrix)//2))

    return finish


def create_start_point(v_matrix, h_matrix):
    '''pass'''
    return (0, random.randrange(0, len(h_matrix)))


def create_vertical_matrix(row=6, col=6):
    matrix = [[random.randint(0,1) if i!=col-1 else 1 for i in range(col)] for j in range(row-1)]
    matrix.append([0]*(col-1))
    matrix[-1].append([1])

    return matrix


def create_horizontal_matrix(v_matrix):
    # matrix = [[random.randint(0,1) if j!=col-1 else 1 for i in range(row)] for j in range(col-1)]
    h_matrix = []

    for r_index, row in enumerate(v_matrix):
        # if r_index == len(v_matrix-1):
        h_matrix.append([])
        for col in row:
            if isinstance(col, int):
                h_matrix[r_index].append(0)
            else:
                flag = get_random_h_main_line(col)
                for i in range(len(col)):
                    if i == flag: h_matrix[r_index].append(0)
                    else: h_matrix[r_index].append(1)
    h_matrix[-1] = [1]*len(h_matrix[0])
    return h_matrix


def get_random_h_main_line(arr):
    '''Выбираем случайный свободный путь из предложенных'''
    return random.randrange(len(arr))


def down_click(m_player, h_matrix):
    '''move down'''
    if m_player[1] < len(h_matrix) and not h_matrix[m_player[1]][m_player[0]]:
        m_player[1] = m_player[1] + 1
    return m_player

def up_click(m_player, h_matrix):
    '''move down'''
    if m_player[1] - 1 >= 0 and not h_matrix[m_player[1]-1][m_player[0]]:
        m_player[1] = m_player[1] - 1
    return m_player

def left_click(m_player, v_matrix):
    '''move down'''
    if m_player[0] - 1 >= 0 and not v_matrix[m_player[1]][m_player[0]-1]:
        m_player[0] = m_player[0] - 1
    return m_player

def right_click(m_player, v_matrix):
    '''move down'''
    if m_player[0] < len(v_matrix) and not v_matrix[m_player[1]][m_player[0]]:
        m_player[0] = m_player[0] + 1
    return m_player


def get_graf(v_matrix, h_matrix):
    '''Создаем граф доступных ходов (клеток)'''
    start = (0,0)
    graf = {start: None}

    # Определяем вертикальные ходы
    for i_row, row in enumerate(v_matrix):
        for i_call, call in enumerate(row):
            if not graf.get((i_row, i_call), False): #Если данной вершины нет - создаем
                graf[(i_row, i_call)] = []


            if not h_matrix[i_row][i_call]: #Ход вниз
                graf[(i_row, i_call)].append((i_row+1, i_call))
            if i_row-1 >= 0 and not h_matrix[i_row-1][i_call]: #Ход вверх
                graf[(i_row, i_call)].append((i_row-1, i_call))

    # Определяем горизонтальные ходы
    for i_row, row in enumerate(h_matrix):
        for i_call, call in enumerate(row):
            if not graf.get((i_row, i_call), False): #Если данной вершины нет - создаем
                graf[(i_row, i_call)] = []

            if not v_matrix[i_row][i_call]: #Ход вправо
                graf[(i_row, i_call)].append((i_row, i_call+1))
            if i_call - 1 >= 0 and not v_matrix[i_row][i_call-1]: #Ход влево
                graf[(i_row, i_call)].append((i_row, i_call-1))

    print(graf)
    return graf


def btf_search(graf, start, finish, screen, margin, border, main_line):
    # from collections import deque

    checked = [(start[1], start[0])]
    queue = deque([(start[1], start[0])])
    # queue = [(start[0], start[1])]


    while queue:
        if queue:
            current_point = queue.popleft()
            # print(f'current {current_point}')
            next_nodes = graf[current_point]
            print(f'cur:{current_point}\n graf: {graf}')
            # time.sleep(1000)
            # print(graf)
            # print(f'nodes {next_nodes}')

            for next_point in next_nodes:
                # print(f'next {next_point}')
                if next_point not in checked:
                    queue.append(next_point)
                    checked.append(next_point)
                if next_point == (finish[0], finish[1]):
                    checked.append(next_point)
                    return checked
            # print(f'queue {checked}')

    return checked


def draw_start_point(screen, margin, border, start, main_line):
    '''Рисум вход в лабиринт'''
    pygame.draw.rect(screen, pygame.Color('green'), (margin + border, margin + border + start[1] * (main_line + border), main_line-border, main_line-border), border_radius=5)


def draw_finish_point(screen, margin, border, finish, main_line):
    '''Рисуем выход из лабиринта'''
    pygame.draw.rect(screen, pygame.Color('red'), (margin + border + finish[0]*(main_line + border), margin + border + finish[1] * (main_line + border), main_line-border, main_line-border), border_radius=5)


def draw_current_point(screen, margin, border, m_player, main_line):
    '''Рисуем текущее положение пользователя'''
    pygame.draw.rect(screen, pygame.Color('blue'), (
    margin + border + m_player[0] * (main_line + border), margin + border + m_player[1] * (main_line + border),
    main_line - border, main_line - border), border_radius=5)

def draw_btf_way(screen, margin, border, path_segment, main_line):
    '''рисуем путь к выходу из текущей позиции'''
    pygame.draw.rect(screen, pygame.Color('blue'), (
        margin + border + path_segment[1] * (main_line + border),
        margin + border + path_segment[0] * (main_line + border),
        main_line - border, main_line - border), border_radius=10)

def draw_v_borders():
    pass

def main():
    border = 3
    main_line = 25
    margin = 20

    FPS = 30
    rows = 8
    cols = 8

    v_matrix = create_vertical_matrix(rows, cols)
    u_v_matrix = update_vertical_matrix(v_matrix)
    h_matrix = create_horizontal_matrix(u_v_matrix)
    v_matrix = update_vertical_matrix_level_2(rows, cols, v_matrix, h_matrix)

    graf = get_graf(v_matrix, h_matrix)

    start = create_start_point(v_matrix, h_matrix)
    finish = create_finish_point(v_matrix, h_matrix, start)

    pygame.init()
    screen = pygame.display.set_mode(((margin * 2) + cols * (border + main_line), (margin * 2) + rows * (border + main_line)))
    clock = pygame.time.Clock()

    m_player = [start[0], start[1]]
    flag = 0
    visited = {(start[0], start[1]): None}
    queue = deque()

    while True:
        screen.fill(pygame.Color('white'))
        if m_player[0] == finish[0] and m_player[1] == finish[1]:
            main()

        #проверка на нажатие клавиши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    m_player = down_click(m_player, h_matrix)
                elif event.key == pygame.K_UP:
                    m_player = up_click(m_player, h_matrix)
                elif event.key == pygame.K_LEFT:
                    m_player = left_click(m_player, v_matrix)
                elif event.key == pygame.K_RIGHT:
                    m_player = right_click(m_player, v_matrix)
                elif event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    rout = btf_search(graf, start, finish, screen, margin, border, main_line)
                    queue = deque([(m_player[1], m_player[0])])
                    visited = {(m_player[1], m_player[0]): None}
                    flag = True


        for i_row, row in enumerate(v_matrix):
            for i_col, col in enumerate(row):
                if col: pygame.draw.line(screen, pygame.Color('black'),
                                         (margin + (1+i_col)*(main_line + border), margin + i_row*(main_line + border)),
                                         (margin + (1+i_col) * (main_line + border), margin + (i_row+1) * (main_line + border)), border)
                # if i_col == 0: pygame.draw.line(screen, pygame.Color('black'),
                #                          (margin + i_col * (main_line + border), margin + i_row*(main_line + border)),
                #                          (margin + i_col * (main_line + border), margin + (i_row+1)*(main_line + border)), border)


        for i_row, row in enumerate(h_matrix):
            for i_col, col in enumerate(row):
                if col: pygame.draw.line(screen, pygame.Color('black'),
                                         (margin + i_col * (main_line + border), margin + (i_row+1) * (main_line + border)),
                                         (margin + (i_col+1) * (main_line + border), margin + (i_row+1) * (main_line + border)), border)
                if i_row == 0: pygame.draw.line(screen, pygame.Color('black'),
                                         (margin + i_col * (main_line + border), margin + i_row * (main_line + border)),
                                         (margin + (i_col+1) * (main_line + border), margin + i_row * (main_line + border)), border)

        if queue:
            cur_point = queue.popleft()
            next_points = graf[cur_point]

            for next_point in next_points:
                if next_point not in visited:
                    queue.append(next_point)
                    visited[next_point] = cur_point

            path_head, path_segment = cur_point, cur_point

            while path_segment:
                print(path_segment)
                clock.tick(20)
                draw_btf_way(screen=screen, margin=margin, border=border, path_segment=path_segment, main_line=main_line)

                if path_head == (finish[1], finish[0]): flag = False
                if path_head != (finish[1], finish[0]) and not flag: main()

                path_segment = visited[path_segment]

        draw_current_point(screen=screen, margin=margin, border=border, m_player=m_player, main_line=main_line)
        draw_start_point(screen=screen, margin=margin, border=border, start=start, main_line=main_line)
        draw_finish_point(screen=screen, margin=margin, border=border, finish=finish, main_line=main_line)


        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()