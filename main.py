import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#TODO: сдвиг фигуры
#TODO: круг
#TODO: посмотреть другие алгоритмы

class Polygon:
    def __init__(self, *points):
        self.points = []
        for point in points:
            self.points.append(point)

    def checkCollision(self, poly2):
        f = False
        self.points.append(self.points[0])
        poly2.points.append(poly2.points[0])

        for i in range(0, len(self.points) - 1):
            for j in range(0, len(poly2.points) - 1):
                if self.intersect(self.points[i], self.points[i + 1], poly2.points[j], poly2.points[j + 1]):
                    f = True
                    break
        return f

    def intersect(self, a, b, c, d):
        def ccw(a, b, c):
            return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)

        return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

    def plotPolygon(self, color='blue'):
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        x_values.append(self.points[0].x)
        y_values.append(self.points[0].y)
        plt.plot(x_values, y_values, color=color)


polygon1 = Polygon(Point(1, 1), Point(3, 3), Point(3, 1))
polygon2 = Polygon(Point(1, 2), Point(2, 4), Point(4, 2))

if polygon1.checkCollision(polygon2):
    print("Многоугольники пересекаются")
else:
    print("Многоугольники не пересекаются")

polygon1.plotPolygon()
polygon2.plotPolygon(color='red')
plt.axis('equal')
plt.show()
