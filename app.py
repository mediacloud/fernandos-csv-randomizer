import os
import shutil
import tempfile
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from randomizer import csv_random_rows


APP_NAME = "FernandosCSVRandomizer"
APP_TITLE = "Fernando's CSV randomizer"
APP_VERSION = '1.0'


class App(object):
    __DEFAULT_ROW_COUNT = 100

    __slots__ = [
        '__ui',

        '__input_csv_file_entry_stringvar',
        '__output_csv_file_entry_stringvar',
        '__row_count_entry_stringvar',
    ]

    def __init__(self):
        self.__ui = tk.Tk()
        self.__ui.resizable(width=False, height=False)
        self.__ui.winfo_toplevel().title(APP_TITLE)
        # self.__ui.geometry('{}x{}'.format(480, 240))

        input_csv_file_label = tk.Label(self.__ui, text="Choose input CSV file:")
        input_csv_file_label.grid(row=0, column=0, sticky=tk.E)

        self.__input_csv_file_entry_stringvar = tk.StringVar()
        input_csv_file_entry = tk.Entry(self.__ui,
                                        textvariable=self.__input_csv_file_entry_stringvar,
                                        state=tk.DISABLED)
        input_csv_file_entry.grid(row=0, column=1, sticky=tk.W)

        input_csv_file_button = tk.Button(self.__ui, text="...", command=self.__choose_input_file)
        input_csv_file_button.grid(row=0, column=2, sticky=tk.W)

        row_count_label = tk.Label(self.__ui, text="Rows to output:")
        row_count_label.grid(row=1, column=0, sticky=tk.E)

        self.__row_count_entry_stringvar = tk.StringVar()
        self.__row_count_entry_stringvar.set(str(self.__DEFAULT_ROW_COUNT))
        row_count_entry = tk.Entry(self.__ui, textvariable=self.__row_count_entry_stringvar)
        row_count_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        randomize_button = tk.Button(self.__ui, text="Randomize CSV", command=self.__randomize_csv, bg='red')
        randomize_button.grid(row=2, column=0, columnspan=3)

    def __choose_input_file(self):
        self.__input_csv_file_entry_stringvar.set(askopenfilename(filetypes=[("CSV file", "*.csv")]))

    def __choose_output_file(self):
        self.__output_csv_file_entry_stringvar.set()

    def __randomize_csv(self):
        temp_csv_output_path = os.path.join(tempfile.mkdtemp(), 'output.csv')

        input_path = self.__input_csv_file_entry_stringvar.get()
        row_count = int(self.__row_count_entry_stringvar.get())

        try:
            csv_random_rows(input_csv_path=input_path, output_csv_path=temp_csv_output_path, row_count=row_count)
            output_path = asksaveasfilename(filetypes=[("CSV files", "*.csv")], defaultextension='.csv')

            if output_path == input_path:
                raise Exception("Can't read from and write to the same file.")

            shutil.copyfile(temp_csv_output_path, output_path)

        except Exception as ex:
            messagebox.showerror(
                message="Unable to randomize {} rows from '{}':\n\n{}".format(row_count, input_path, str(ex))
            )

        else:
            messagebox.showinfo(message="Randomized {} rows into '{}'.".format(row_count, output_path))

    def ui_loop(self) -> None:
        self.__ui.mainloop()


if __name__ == "__main__":
    app = App()
    app.ui_loop()
