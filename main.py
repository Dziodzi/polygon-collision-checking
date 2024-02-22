import math
import time
from copy import copy

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

    def check_boxes_collision(self, box):
        if self.get_min_x() <= box.get_min_x() <= self.get_max_x() or self.get_min_x() <= box.get_max_x() <= self.get_max_x():
            if self.get_min_y() <= box.get_min_y() <= self.get_max_y() or self.get_min_y() <= box.get_max_y() <= self.get_max_y():
                return True
        elif box.get_min_x() <= self.get_min_x() <= box.get_max_x() or box.get_min_x() <= self.get_max_x() <= box.get_max_x():
            if box.get_min_y() <= self.get_min_y() <= box.get_max_y() or box.get_min_y() <= self.get_max_y() <= box.get_max_y():
                return True
        return False

    def check_boxes_borders(self, box):
        i = 0
        if self.get_min_x() == box.get_min_x(): i += 1
        if self.get_max_x() == box.get_max_x(): i += 1
        if self.get_max_y() == box.get_max_y(): i += 1
        if self.get_min_y() == box.get_min_y(): i += 1
        if i >= 3:
            return True
        return False

    def checkCollision(self, poly2):
        f = False

        self.points.append(copy(self.points[0]))
        poly2.points.append(copy(poly2.points[0]))

        if not self.check_boxes_collision(poly2):
            return False
        if self.check_boxes_borders(poly2):
            return True

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

    def get_max_x(self):
        cur_max = -9223372036854775806
        for point in self.points:
            if point.x > cur_max:
                cur_max = point.x
        return cur_max

    def get_max_y(self):
        cur_max = -9223372036854775806

        for point in self.points:
            if point.y > cur_max:
                cur_max = point.y
        return cur_max

    def get_min_x(self):
        cur_min = 9223372036854775807
        for point in self.points:
            if point.x < cur_min:
                cur_min = point.x
        return cur_min

    def get_min_y(self):
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

total_time = time.time() - seconds_start
count_pairs = int((len(polygonList) * (len(polygonList) + 1)) / 2)

print("Программа обработала", count_pairs, "пар полигонов за", round(total_time, 4)
      , "секунд.")
