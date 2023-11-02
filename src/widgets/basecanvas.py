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

        self._setup_keybind()

    def init_canvas(self):
        self.delete("all")

        self._current_image = None
        self._imagetk = None
        self._imageid = None

        self._imscale = 1.0


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
    
    def _setup_keybind(self) -> None:
        self.bind("<ButtonPress-1>", self._move_from)
        self.bind("<B1-Motion>", self._move_to)
        self.bind("<MouseWheel>", self._wheel)
