import tkinter as tk

from tkinter import filedialog

from widgets import FileListbox

class FileManager(tk.LabelFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grid_propagate(False)

        self.configure(text="檔案")

        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._setup_widgets()


    def _setup_widgets(self) -> None:
        '''
        初始化FileManager中的所有部件類型及位置
        '''
        self.access_file_button = tk.Button(
            self, text="選擇存取檔案", command=self._access_file
        )
        self.access_file_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)

        self.remove_accessedfile_button = tk.Button(
            self, text="移除存取檔案", command=self._remove_accessedfile
        )
        self.remove_accessedfile_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)

        self.preview_file_button = tk.Button(
            self, text="選取預覽檔案"
        )
        self.preview_file_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)

        self.cancel_preview_button = tk.Button(
            self, text="取消預覽檔案"
        )
        self.cancel_preview_button.grid(row=3, column=0, padx=5, pady=5, sticky=tk.EW)

        tk.Label(self, text="檔案列表:").grid(row=4, column=0, sticky=tk.W)

        self.file_listbox = FileListbox(self)
        self.file_listbox.grid(row=5, column=0, padx=5, pady=5, sticky=tk.NSEW)


    def _access_file(self):
        filepaths = filedialog.askopenfilenames(
            title="Select a file",
            filetypes=[
                ("Image Files", "*.png *.jpg *.tif")
            ]
        )

        for filepath in filepaths:
            self.file_listbox.insert_file(filepath)
    
    def _remove_accessedfile(self) -> None:
        self.file_listbox.remove_file()
            