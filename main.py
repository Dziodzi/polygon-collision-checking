import math
import time
from copy import copy

import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# TODO: лежит ли внутри фигуры
# Проверка: если для любой вершины данной фигуры окажется, что есть вершины другой фигуры левее, правее, выше и ниже, но фигуры пересекаются
# TODO: посмотреть другие алгоритмы
# GJK
# TODO: статистика

class Polygon:
    def __init__(self, *points):
        self.points = []
        for point in points:
            self.points.append(point)

    def checkBoxesCollision(self, box):
        if self.getMinX() < box.getMinX() < self.getMaxX() or (box.getMinX() < self.getMinX() < box.getMaxX()):
            if self.getMinY() < box.getMinY() < self.getMaxY() or (box.getMinY() < self.getMinY() < box.getMaxY()):
                return True
        return False

    def checkCollision(self, poly2):
        f = False

        self.points.append(copy(self.points[0]))
        poly2.points.append(copy(poly2.points[0]))

        if not self.checkBoxesCollision(poly2):
            #print("Боксы пересеклись, а значит")
            return False

        for i in range(0, len(self.points) - 1):
            for j in range(0, len(poly2.points) - 1):
                if self.intersect(self.points[i], self.points[i + 1], poly2.points[j], poly2.points[j + 1]):
                    f = True
                    break

        return f

    @staticmethod
    def intersect(a, b, c, d):
        def ccw(e, f, g):
            return (g.y - e.y) * (f.x - e.x) >= (f.y - e.y) * (g.x - e.x)

        return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

    def plotPolygon(self, color='blue'):
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        x_values.append(self.points[0].x)
        y_values.append(self.points[0].y)
        plt.plot(x_values, y_values, color=color)

    def movePolygon(self, x, y):
        for point in self.points:
            point.x += x
            point.y += y

    def getMaxX(self):
        cur_max = -9223372036854775806
        for point in self.points:
            if point.x > cur_max:
                cur_max = point.x
        return cur_max

    def getMaxY(self):
        cur_max = -9223372036854775806

        for point in self.points:
            if point.y > cur_max:
                cur_max = point.y
        return cur_max

    def getMinX(self):
        cur_min = 9223372036854775807
        for point in self.points:
            if point.x < cur_min:
                cur_min = point.x
        return cur_min

    def getMinY(self):
        cur_min = 9223372036854775807
        for point in self.points:
            if point.y < cur_min:
                cur_min = point.y
        return cur_min


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


polygonList = []

for i in range(0, 5):
    polygonList.append(Polygon(Point(1, i), Point(2, i + 1), Point(1, i + 2)))
    polygonList.append(Polygon(Point(i + 2, 1), Point(i + 1, 3), Point(i + 2, 2)))
    polygonList.append(Polygon(Point(i + 1, 2), Point(2, i + 3), Point(7, i + 5)))
    polygonList.append(Polygon(Point(1, i), Point(2, i + 1), Point(1, i + 2), Point(3, i + 2), Point(i + 3, 3)))
    polygonList.append(Circle(1, i, 2))
    polygonList.append(Circle(1, i, 3))
    polygonList.append(Circle(1, i, 4))

seconds_start = time.time()
# seconds_for_waiting = 0
# step = 1

for i in range(0, len(polygonList) - 1):
    for j in range(i + 1, len(polygonList)):
        if polygonList[i].checkCollision(polygonList[j]):
       #     print("многоугольники пересекаются")
            pass
        else:
            pass
           # print("ОПА! Многоугольники не пересекаются")
       # print("-=-=-=-=-=-=-=-")
        # polygonList[i].plotPolygon()
        # polygonList[j].plotPolygon(color='red')
        # plt.axis('equal')
        # plt.show()
        # time.sleep(step)
        # seconds_for_waiting += step

print("Программа обработала все пары", len(polygonList), "полигонов за",
      time.time() - seconds_start, "секунд.")
