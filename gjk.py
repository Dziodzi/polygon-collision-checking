import math
import time
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Polygon:
    def __init__(self, *points):
        self.points = []
        for point in points:
            self.points.append(point)

    def get_max_x(self):
        cur_max = -math.inf
        for point in self.points:
            if point.x > cur_max:
                cur_max = point.x
        return cur_max

    def get_max_y(self):
        cur_max = -math.inf

        for point in self.points:
            if point.y > cur_max:
                cur_max = point.y
        return cur_max

    def get_min_x(self):
        cur_min = math.inf
        for point in self.points:
            if point.x < cur_min:
                cur_min = point.x
        return cur_min

    def get_min_y(self):
        cur_min = math.inf
        for point in self.points:
            if point.y < cur_min:
                cur_min = point.y
        return cur_min

    """Проверка боксов на несоприкосновение"""

    def check_boxes_collision(self, box):
        if self.get_min_x() <= box.get_min_x() <= self.get_max_x() or self.get_min_x() <= box.get_max_x() <= self.get_max_x():
            if self.get_min_y() <= box.get_min_y() <= self.get_max_y() or self.get_min_y() <= box.get_max_y() <= self.get_max_y():
                return True
        elif box.get_min_x() <= self.get_min_x() <= box.get_max_x() or box.get_min_x() <= self.get_max_x() <= box.get_max_x():
            if box.get_min_y() <= self.get_min_y() <= box.get_max_y() or box.get_min_y() <= self.get_max_y() <= box.get_max_y():
                return True
        return False


class Circle(Polygon):
    step = 8

    def __init__(self, x, y, radius, *points):
        super().__init__(*points)
        self.points = []

        cur_angle = 0
        for i in range(0, self.step):
            angle_rad = cur_angle / 180 * math.pi
            cur_x = x + radius * math.cos(angle_rad)
            cur_y = y + radius * math.sin(angle_rad)
            cur_angle += 360 / self.step
            self.points.append(Point(cur_x, cur_y))


"""Функция для сэмплирования точки на ребре разности Минковского без построения всей фигуры. 
Она получает фигуру и направление, которое нужно проверить, а затем 
получает наиболее удалённую точку."""


def support(poly, direction):
    max_dot = -math.inf
    max_point = None

    for point in poly.points:
        dot_product = point.x * direction.x + point.y * direction.y
        if dot_product > max_dot:
            max_dot = dot_product
            max_point = point

    return max_point


"""Вычитание координат точек"""


def subtract_points(point1, point2):
    return Point(point1.x - point2.x, point1.y - point2.y)


"""Непосредственно сам алгоритм Гилберта-Джонсона-Кирти"""


def gjk(poly1, poly2):
    """Первичная проверка - если боксы не соприкасаются, то gjk можно не прогонять"""
    if not poly1.check_boxes_collision(poly2):
        return False

    direction = Point(1, 0)
    support_point = subtract_points(support(poly1, direction), support(poly2, direction))
    simplex = [support_point]

    direction = Point(-support_point.x, -support_point.y)

    while True:
        a = support(poly1, direction)
        b = support(poly2, Point(direction.x, direction.y))
        ab = subtract_points(b, a)

        if (ab.x * direction.x + ab.y * direction.y) <= 0:
            return False
        simplex.append(ab)

        if len(simplex) == 3:
            if contains_origin(simplex, direction):
                return True
            else:
                simplex = reduce_simplex(simplex)


"""Проверка симплекса (выборки точек вдоль фигуры разности Минковского) на содержание в себе точки начала координат"""


def contains_origin(simplex, direction):
    a = simplex[-1]
    ao = Point(-a.x, -a.y)
    if len(simplex) == 3:
        b = simplex[-2]
        c = simplex[-3]

        ab = subtract_points(b, a)
        ac = subtract_points(c, a)

        ab_perp = cross_vectors(ac, ab)
        ac_perp = cross_vectors(ab, ac)

        if (ab_perp.x * ao.x + ab_perp.y * ao.y) > 0:
            direction.x = ab_perp.x
            direction.y = ab_perp.y
            simplex.remove(c)
            return False
        elif (ac_perp.x * ao.x + ac_perp.y * ao.y) > 0:
            direction.x = ac_perp.x
            direction.y = ac_perp.y
            simplex.remove(b)
            return False
        else:
            return True
    else:
        b = simplex[-2]
        ab = subtract_points(b, a)
        direction.x = cross_vectors(ab, ao).x
        direction.y = cross_vectors(ab, ao).y
        return False


"""Векторное произведение"""


def cross_vectors(a, b):
    return Point(
        a.y * b.x - a.x * b.y,
        a.x * b.y - a.y * b.x
    )


"""Уменьшение симплекса до отрезка"""


def reduce_simplex(simplex):
    if (simplex[1].x * simplex[0].x + simplex[1].y * simplex[0].y) > (
            simplex[1].x * simplex[2].x + simplex[1].y * simplex[2].y):
        return [simplex[0], simplex[1]]
    else:
        return [simplex[2], simplex[1]]


def plot_polygon(poly, color='b'):
    x = [point.x for point in poly.points]
    y = [point.y for point in poly.points]
    plt.plot(x + [x[0]], y + [y[0]], color)


def plot_collision(poly1, poly2):
    plt.figure(figsize=(5, 5))

    plot_polygon(poly1, 'b-')
    plot_polygon(poly2, 'g-')

    plt.axis('equal')
    plt.title('Polygon Collision')
    plt.show()


if __name__ == "__main__":
    polygonList = []

    for i in range(0, 20):
        polygonList.append(Circle(i, 1, 1))
        polygonList.append(Circle(i, 1, 5))
        polygonList.append(Circle(i, 1, 1))
        polygonList.append(Circle(i + 0.5, 1.5, 1))
        polygonList.append(Circle(i + 3, 4, 1))
        polygonList.append(Polygon(Point(i, 1), Point(1, 2), Point(2, 2)))
        polygonList.append(Polygon(Point(i, 1), Point(1, 2), Point(2, 2)))
        polygonList.append(Polygon(Point(i + 2, 3), Point(3, 4), Point(4, 4)))
        polygonList.append(Polygon(Point(i + 3, 5), Point(13, 14), Point(14, 14)))
        polygonList.append(Polygon(Point(i + 4, 10), Point(11, 15), Point(15, 15)))

    seconds_start = time.time()

    for i in range(0, len(polygonList) - 1):
        for j in range(i + 1, len(polygonList)):
            collision = gjk(polygonList[i], polygonList[j])
            if collision:
                # print("Многоугольники пересекаются")
                pass
            else:
                # print("Многоугольники не пересекаются")
                pass

    total_time = time.time() - seconds_start
    count_pairs = int((len(polygonList) * (len(polygonList) - 1)) / 2)

    print("Программа обработала", count_pairs, "пар полигонов за", round(total_time, 4)
          , "секунд.")
