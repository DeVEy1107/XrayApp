import os

import tkinter as tk

from PIL import Image, ImageTk

class BaseCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._image = None
        self._current_image = None
        self._imagetk = None
        self._imageid = None

        self._delta = 0.75
        self._imscale = 1.0

        self._points_pos = []
        self._pointid = []

        self._pointsize = 10

        self._setup_keybind()

    def init_canvas(self):
        self.delete("all")

        self._current_image = None
        self._imagetk = None
        self._imageid = None

        self._imscale = 1.0

        self._points_pos = []
        self._pointid = []


    def load_image(self, img:Image.Image) -> None:
        self.init_canvas()

        self._image = img
        self._current_image = img 

    def update_canvas(self) -> None:
        if self._current_image:
            width, height = self._current_image.size
            assert isinstance(self._current_image, Image.Image)
            new_size = int(round(self._imscale * width)), int(round(self._imscale * height))
            self._imagetk = ImageTk.PhotoImage(
                self._current_image.resize(new_size, Image.BILINEAR)
            )
            self._imageid = self.create_image(
                0, 0, anchor=tk.NW, image=self._imagetk
            )
        
        if self._points_pos:
            self._pointid = []
            for x, y in self._points_pos:
                r = (self._pointsize / 2) * self._imscale

                x, y = x * self._imscale, y * self._imscale
                x0, y0 = x - r, y - r
                x1, y1 = x + r, y + r
                pointid = self.create_oval(x0, y0, x1, y1, fill="red", tags="point")
                self._pointid.append(pointid)

    def _move_from(self, event) -> None:
        self._start_x = event.x
        self._start_y = event.y
    
    def _move_to(self, event) -> None:
        dx = event.x - self._start_x
        dy = event.y - self._start_y
        self._start_x = event.x
        self._start_y = event.y
        self.move("all", dx, dy)

    def _wheel(self, event) -> None:
        if event.delta == -120:
            self._imscale *= self._delta
        if event.delta == 120:
            self._imscale /= self._delta

        x, y = event.x, event.y
        
        self.scale("all", x, y, self._imscale, self._imscale)
        self.update_canvas()
    
    def _draw_point(self, event) -> None:
        x, y = event.x, event.y
        width, height = self._image.size
        img_x, img_y = self.coords(self._imageid)
        
        abs_point_x, abs_point_y = int(round((x - img_x) / self._imscale)), \
                                   int(round((y - img_y) / self._imscale))

        if abs_point_x < 0:
            abs_point_x = 0
        if abs_point_x >= width:
            abs_point_x = width - 1
        if abs_point_y < 0:
            abs_point_y = 0
        if abs_point_y >= height:
            abs_point_y = height - 1

        self._points_pos.append([abs_point_x, abs_point_y])

        print(f"Marking at ({abs_point_x}, {abs_point_y})")
        print(f"current points {self._points_pos}")

        self.update_canvas()

    def _delete_one_point(self, event) -> None:
        pointid = self.find_closest(event.x, event.y)[-1]

        if pointid != self._imageid:
            index = self._pointid.index(pointid)

            self._pointid.pop(index)
            self._points_pos.pop(index)
            self.update_canvas()

    def _setup_keybind(self) -> None:
        self.bind("<ButtonPress-1>", self._move_from)
        self.bind("<B1-Motion>", self._move_to)
        self.bind("<MouseWheel>", self._wheel)
    
    def switch_mode(self, mode) -> None:
        if mode == "marking":
            self.unbind("<ButtonPress-1>")
            self.unbind("<B1-Motion>")
            self.unbind("<MouseWheel>")

            self.bind("<ButtonPress-1>", self._draw_point)
            self.tag_bind("point", "<ButtonPress-3>", self._delete_one_point)

        elif mode == "preview":
            self.unbind("<ButtonPress-1>")
            self.tag_unbind("point", "<ButtonPress-3>")

            self._setup_keybind()

        else:
            print("Invalid mode!")

    def clear_allpoints(self) -> None:
        self.delete("point")
        self._pointid = []
    
    def save_markedimage(self) -> None:
        pass
