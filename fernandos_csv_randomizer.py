import os
import shutil
import tempfile
# noinspection PyPackageRequirements
import wx

from randomizer import csv_random_rows

APP_NAME = "FernandosCSVRandomizer"
APP_TITLE = "Fernando's CSV randomizer"
APP_VERSION = '1.0'


class MainFrame(wx.Frame):
    __DEFAULT_ROW_COUNT = 100

    __slots__ = [
        '__ui',

        '__input_csv_file_entry',
        '__row_count_entry',
    ]

    def __init__(self):
        wx.Frame.__init__(self,
                          parent=None,
                          id=wx.ID_ANY,
                          title=APP_TITLE,
                          size=(480, 240),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.__init_gui()

        self.Center()
        self.Show()

    def __init_gui(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        quit_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit {}'.format(APP_TITLE))
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, lambda ev: self.Close(), quit_item)

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(rows=3, cols=2, vgap=9, hgap=25)

        input_csv_file_label = wx.StaticText(panel, label="Choose input CSV file:")
        self.__input_csv_file_entry = wx.FilePickerCtrl(panel, message="CSV input file:",
                                                        wildcard="CSV files (*.csv)|*.csv")
        row_count_label = wx.StaticText(panel, label="Rows to output:")
        self.__row_count_entry = wx.TextCtrl(panel, value=str(self.__DEFAULT_ROW_COUNT))
        randomize_button = wx.Button(panel, label="Randomize CSV")
        randomize_button.Bind(wx.EVT_BUTTON, lambda ev: self.__randomize_csv())

        fgs.AddMany([
            (input_csv_file_label,), (self.__input_csv_file_entry, 1, wx.EXPAND),
            (row_count_label,), (self.__row_count_entry, 1, wx.EXPAND),
            (randomize_button,),
        ])

        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)

    def __randomize_csv(self):
        temp_csv_output_path = os.path.join(tempfile.mkdtemp(), 'output.csv')

        input_path = self.__input_csv_file_entry.GetPath()
        row_count = int(self.__row_count_entry.GetValue())

        try:
            csv_random_rows(input_csv_path=input_path, output_csv_path=temp_csv_output_path, row_count=row_count)

        except Exception as ex:
            wx.MessageBox(
                message="Unable to randomize {} rows from '{}':\n\n{}".format(row_count, input_path, str(ex)),
                caption='Error',
                style=wx.OK | wx.ICON_ERROR
            )

        else:

            input_path_dir = os.path.dirname(input_path)
            input_path_filename_ext = os.path.splitext(os.path.basename(input_path))
            output_filename = '{}-random{}{}'.format(input_path_filename_ext[0], row_count, input_path_filename_ext[1])

            dlg = wx.FileDialog(self,
                                message="Choose output CSV file:",
                                defaultDir=input_path_dir,
                                defaultFile=output_filename,
                                wildcard="CSV files (*.csv)|*.csv",
                                style=wx.FD_SAVE | wx.FLP_USE_TEXTCTRL | wx.FLP_OVERWRITE_PROMPT)

            if dlg.ShowModal() == wx.ID_OK:

                output_path = dlg.GetPath()

                try:

                    if output_path == input_path:
                        raise Exception("Can't read from and write to the same file.")

                    shutil.copyfile(temp_csv_output_path, output_path)

                except Exception as ex:
                    wx.MessageBox(
                        message="Unable to save randomized rows:\n\n{}".format(str(ex)),
                        caption='Error',
                        style=wx.OK | wx.ICON_ERROR
                    )

                else:
                    wx.MessageBox(
                        message="Randomized {} rows into '{}'.".format(row_count, output_path),
                        caption='Information',
                        style=wx.OK | wx.ICON_INFORMATION
                    )


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    app_frame = MainFrame()
    app.SetTopWindow(app_frame)
    app_frame.Show()
    app.MainLoop()
