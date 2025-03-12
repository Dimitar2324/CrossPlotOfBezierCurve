import tkinter as tk
from tkinter import Canvas


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class CrossPlot:
    def __init__(self):
        self.points = []
        self.x_func = []
        self.y_func = []

        self.frame_width = 1200
        self.frame_height = 700

        self.point_stroke = 8
        self.line_stroke = 1
        self.bezier_stroke = 2
        self.de_casteljau_steps = 100

        self.x_func_flag = False
        self.y_func_flag = False

        self.root = tk.Tk()
        self.root.title("CrossPlot")
        self.root.geometry(f"{self.frame_width}x{self.frame_height}")

        self.canvas = Canvas(self.root, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<KeyPress>", self.key_pressed)
        self.canvas.bind("<Button-1>", self.mouse_pressed)
        self.canvas.bind("<Button-3>", self.mouse_pressed)

        self.draw()
        self.root.mainloop()

    def draw(self):
        self.canvas.delete("all")
        self.set_coordinate_lines()
        self.set_up_labels()

        self.draw_lines(self.points)
        self.draw_bezier_curve(self.points)
        self.draw_points(self.points)

        if self.x_func_flag:
            self.draw_x_points()
        if self.y_func_flag:
            self.draw_y_points()

    def draw_lines(self, points):
        if len(points) > 1:
            for i in range(len(points) - 1):
                self.canvas.create_line(points[i].x, points[i].y, points[i + 1].x, points[i + 1].y, fill="yellow", width=self.line_stroke)

    def draw_points(self, points):
        for point in points:
            self.canvas.create_oval(point.x - self.point_stroke / 2, point.y - self.point_stroke / 2,
                                    point.x + self.point_stroke / 2, point.y + self.point_stroke / 2, fill="cyan")

    def draw_bezier_curve(self, points):
        if len(points) < 2:
            return
        curve_points = self.calculate_bezier_curve(points)
        for i in range(len(curve_points) - 1):
            self.canvas.create_line(curve_points[i].x, curve_points[i].y, curve_points[i + 1].x, curve_points[i + 1].y,
                                    fill="red", width=self.bezier_stroke)

    def draw_x_points(self):
        self.compute_x_functional_points()

        self.draw_lines(self.x_func)
        self.draw_bezier_curve(self.x_func)
        self.draw_points(self.x_func)

    def draw_y_points(self):
        self.compute_y_functional_points()

        self.draw_lines(self.y_func)
        self.draw_bezier_curve(self.y_func)
        self.draw_points(self.y_func)

    def set_coordinate_lines(self):
        self.canvas.create_line(self.frame_width / 2, 0, self.frame_width / 2, self.frame_height, fill="white")
        self.canvas.create_line(0, self.frame_height / 2, self.frame_width, self.frame_height / 2, fill="white")

    def set_up_labels(self):
        self.canvas.create_text(self.frame_width - 30, self.frame_height / 2 - 15, text="X", font=("Arial", 20), fill="white")
        self.canvas.create_text(self.frame_width / 2 + 15, 55, text="Y", font=("Arial", 20), fill="white")
        self.canvas.create_text(20, self.frame_height / 2 - 15, text="T", font=("Arial", 20), fill="white")
        self.canvas.create_text(self.frame_width / 2 + 15, self.frame_height - 20, text="T", font=("Arial", 20), fill="white")

    def calculate_bezier_curve(self, points):
        curve_points = []
        for i in range(self.de_casteljau_steps + 1):
            t = i / self.de_casteljau_steps
            curve_points.append(self.de_casteljau_algorithm(t, points))
        return curve_points

    def de_casteljau_algorithm(self, t, points):
        points_copy = points[:]
        while len(points_copy) > 1:
            points_copy = [
                Point((1 - t) * points_copy[i].x + t * points_copy[i + 1].x,
                      (1 - t) * points_copy[i].y + t * points_copy[i + 1].y)
                for i in range(len(points_copy) - 1)
            ]
        return points_copy[0]

    def compute_x_functional_points(self):
        self.x_func = [
            Point(point.x, self.frame_height / 2 + (i + 1) * (self.frame_height / 2) / (len(self.points) + 1))
            for i, point in enumerate(self.points)
        ]

    def compute_y_functional_points(self):
        self.y_func = [
            Point(self.frame_width / 2 - (i + 1) * (self.frame_width / 2) / (len(self.points) + 1), point.y)
            for i, point in enumerate(self.points)
        ]

    def key_pressed(self, event):
        if event.char == 'x':
            self.x_func_flag = not self.x_func_flag
        elif event.char == 'y':
            self.y_func_flag = not self.y_func_flag

        self.draw()

    def mouse_pressed(self, event):
        if event.num == 1:
            self.points.append(Point(event.x, event.y))
        elif event.num == 3:
            if self.points:
                self.points.pop()
        self.draw()


if __name__ == "__main__":
    CrossPlot()
