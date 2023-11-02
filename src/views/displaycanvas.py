import os
import tkinter as tk

from PIL import Image

from widgets import BaseCanvas

class DisplayCanvas(tk.LabelFrame):
   def __init__(self, *args, **kwargs) -> None:
      super().__init__(*args, **kwargs)

      self.configure(text="影像畫面")
      
      self._setup_widgets()

   def _setup_widgets(self) -> None:
      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)

      self.canvas = BaseCanvas(self, background="gray70")
      self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

   def display_image(self, filepath) -> None:
      if os.path.isfile(filepath):
         print(f"Loading image from {filepath}")
         image = Image.open(filepath)
         self.canvas.load_image(image)
         self.canvas.update_canvas()
   
   def clear_canvas(self) -> None:
      self.canvas.init_canvas()

