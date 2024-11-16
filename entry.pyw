import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
from widget.entry_ui import Ui_MainWindow
from settings import SettingsDialog
import os
import subprocess



class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings = qtc.QSettings("nabildevelop", "ui_converter")
        self.label.dragEnterEvent = self.dragEnterEvent
        self.label.dropEvent = self.dropEvent
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        relative_save_location = self.settings.value("save_location")
        for url in event.mimeData().urls():
            input_path = url.path()[1:]
            containing_folder_path, name = os.path.split(input_path)
            name_without_extension, extension = os.path.splitext(name)
            try:
                command = "pyuic6 {}".format(input_path)
                result = subprocess.run(command, capture_output=True)
                if result.returncode==0:
                    output_txt = result.stdout.decode("utf-8")
                    output_folder= os.path.join(containing_folder_path, relative_save_location)
                    output_path = os.path.join(output_folder, "{}.py".format(name_without_extension))
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "w+") as f:
                        f.write(output_txt)
                else:
                    err = result.stderr.decode("utf-8")
                    self.statusbar.showMessage(err)
            except Exception as e:
                self.statusbar.showMessage(str(e))
                print('Failed to convert ui file: ' + str(e))

    def openSettingsDialog(self):
        dialog = SettingsDialog(self)
        dialog.show()
    



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())