import tkinter as tk


class ImageEditor(tk.LabelFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.configure(text="操作介面")
    
        self._setup_widgets()



    def _setup_widgets(self) -> None:

        self.auto_marking_button = tk.Button(self, text="自動標註")
        self.auto_marking_button.grid(row=0, column=0, padx=5, pady=5)

        self.clear_allpoints_button = tk.Button(self, text="清除所有標點")
        self.clear_allpoints_button.grid(row=0, column=1, padx=5, pady=5)

        self.save_marked_image_button = tk.Button(self, text="儲存已標註影像")
        self.save_marked_image_button.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self, text="切換模式:").grid(row=1, column=0, padx=0, pady=0)


        self.switchmode_var = tk.StringVar() 
        self.switchmode_var.set("preview")

        self.previewmode_button = tk.Radiobutton(
            self, text="瀏覽模式", variable=self.switchmode_var, value="preview"
        )
        self.previewmode_button.grid(row=1, column=1, padx=5, pady=5)

        self.markingmode_button = tk.Radiobutton(
            self, text="標註模式", variable=self.switchmode_var, value="marking"
        )
        self.markingmode_button.grid(row=1, column=2, padx=5, pady=5)
    
    def get_current_mode(self) -> str:
        return self.switchmode_var.get()