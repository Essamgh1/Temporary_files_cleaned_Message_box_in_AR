import tkinter as tk
from tkinter import ttk
import os
import shutil
import tempfile

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('حذف ملفات النظام الغير ضرورية')
        self.create_widgets()
        self.deleted_files_folders = 0

    def create_widgets(self):
        self.start_button = ttk.Button(self, text='ابدأ', command=self.start_deleting)
        self.start_button.pack(pady=20)

        self.progress = ttk.Progressbar(self, mode='determinate', length=200)
        self.progress.pack(pady=20)

        self.status_label = ttk.Label(self, text='الحالة: في انتظار البدء')
        self.status_label.pack(pady=10)

    def start_deleting(self):
        self.deleted_files_folders = 0  # Reset count
        paths = [tempfile.gettempdir(), os.environ.get('TEMP'), r'C:\Windows\Prefetch']
        total_paths = sum([len(files) for r, d, files in os.walk('C:\Windows\Prefetch') for path in paths if os.path.exists(path)])
        self.progress['maximum'] = total_paths

        for path in paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        try:
                            os.remove(os.path.join(root, name))
                            self.deleted_files_folders += 1
                            self.progress['value'] += 1
                            self.update_progress()
                        except Exception as e:
                            print(e)

                    for name in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, name))
                            self.deleted_files_folders += 1
                            self.progress['value'] += 1
                            self.update_progress()
                        except Exception as e:
                            print(e)

        self.status_label.config(text=f'العملية اكتملت: تم حذف {self.deleted_files_folders} ملفات/مجلدات')

    def update_progress(self):
        self.status_label.config(text=f'جاري الحذف... {self.progress["value"]}/{self.progress["maximum"]}')
        self.update_idletasks()

if __name__ == "__main__":
    app = App()
    app.mainloop()
