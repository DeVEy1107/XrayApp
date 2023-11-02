import tkinter as tk

from controllers import MainController

class App(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.title("Xray prediction app")

        self._setup_mainwindow()

        self.controller = MainController(self)

    def _setup_mainwindow(self) -> None:
        '''
        用於初始化主視窗大小及位置
        '''
        screen_w, screen_h = self.winfo_screenwidth(), self.winfo_screenheight()

        scale_w, scale_h = 0.6, 0.8

        self.window_w, self.window_h = int(scale_w * screen_w), int(scale_h * screen_h)

        x_pos, y_pos = (screen_w - self.window_w) // 2, (screen_h - self.window_h) // 2
        
        self.geometry(f"{self.window_w}x{self.window_h}+{x_pos}+{y_pos}")


if __name__ == "__main__":
    app = App()
    app.mainloop()