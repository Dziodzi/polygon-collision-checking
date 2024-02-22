# Методы обнаружения коллизий двух выпуклых полигонов

---

## Задание:

* Проверить разными методами, пересекаются ли два произвольных выпуклых полигона;
* Визуализировать их с помощью ```matplotlib```;
* Измерить время работы алгоритмов без ```print``` и отрисовки.

---

## Решение 1:

*Отрезки AB и CD пересекаются тогда и только
тогда, когда точки A и B разделены отрезком CD, а точки C и D разделены отрезком AB.*

* Если точки A и B разделены отрезком
  CD, то ACD и BCD должны иметь противоположную ориентацию, что
  означает, что либо ACD, либо BCD направлены против часовой
  стрелки, но не оба сразу.

````   
def __intersect__(self, A, B, C, D):
    def ccw(A, B, C):
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
````

### Код решения:
[linearSolution.py](https://github.com/Dziodzi/polygon-collision-checking/blob/main/linearSolution.py)

### Результат работы:
![image](https://github.com/Dziodzi/polygon-collision-checking/assets/79766495/8cfa8da8-344a-4504-a87e-7a8964889757)

---
 
## Решение 2:

* Алгоритм Гилберта-Джонсона-Кёрти (GJK) — это алгоритм, предназначенный для определения пересечения двух выпуклых фигур. Он реализуется при помощи разности Минковского и оптимизирован при помощи обобщённой «вспомогательной функции» и симплексов.

### Код решения:
[gjk.py](https://github.com/Dziodzi/polygon-collision-checking/blob/main/gjk.py)

### Результат работы:
![image](https://github.com/Dziodzi/polygon-collision-checking/assets/79766495/419d8006-03eb-48b3-b1b7-78594e04e4a5)

---

## Вывод:

* GJK работает в 308 раз быстрее, чем перебор всех вершин полигонов, который работает за ```O(n + k)```. Такая скорость достигается засчёт оптимизации вспомогательной функции и симплексами, так полной разности Минковского, которая без оптимизации также высчитывается за ```O(n + k)```.
