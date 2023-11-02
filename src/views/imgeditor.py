import tkinter as tk


class ImageEditor(tk.LabelFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.configure(text="操作介面")