import tkinter as tk

from views import FileManager, ImageEditor, DisplayCanvas

class MainController:
    def __init__(self, root) -> None:
        
        assert isinstance(root, tk.Tk)

        self.root = root

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self._setup_layout()
        
        self._setup_command()

    def _setup_layout(self) -> None:
        self.file_manager = FileManager(self.root, width=int(0.2*self.root.window_w))
        self.file_manager.grid(row=0, column=0, padx=5, pady=5, rowspan=2, sticky=tk.NS)

        self.image_editor = ImageEditor(self.root)
        self.image_editor.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

        self.display_canvas = DisplayCanvas(self.root)
        self.display_canvas.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

    def _setup_command(self) -> None:
        self.file_manager.preview_file_button.configure(command=self.__preview_file)
        self.file_manager.cancel_preview_button.configure(command=self.__cancel_preview)
        self.image_editor.previewmode_button.configure(command=self.__switch_mode)
        self.image_editor.markingmode_button.configure(command=self.__switch_mode)
        self.image_editor.clear_allpoints_button.configure(command=self.__clear_allpoints)

    def __preview_file(self) -> None:
        filepath = self.file_manager.file_listbox.get_selected_filepath()
        self.display_canvas.display_image(filepath)
    
    def __cancel_preview(self) -> None:
        self.display_canvas.clear_canvas()

    def __switch_mode(self) -> None:
        current_mode = self.image_editor.get_current_mode()
        self.display_canvas.switch_mode(current_mode)
        print(f"current mode is {current_mode}")
    
    def __clear_allpoints(self) -> None:
        self.display_canvas.clear_allpoints()


        