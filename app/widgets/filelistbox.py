import tkinter as tk


class FileListbox(tk.Listbox):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.filepaths = {}
    
    def insert_file(self, filepath) -> None:
        if filepath not in self.filepaths.keys():
            filename = filepath.split('/')[-1]
            self.filepaths[filename] = filepath
            self.insert(tk.END, filename)
    
    def remove_file(self) -> None:
        selected_file_index = self.curselection() 
        self.filepaths.pop(self.get(selected_file_index))
        self.delete(selected_file_index)

    def get_selected_filepath(self) -> str:
        selected_file_index = self.curselection()
        if isinstance(selected_file_index, (tuple, list)):
            selected_file_index = selected_file_index[-1]

        filepath = self.filepaths.get(self.get(selected_file_index), "Not found!")

        return filepath