import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc
from widget.settings_ui import Ui_SettingsDialog
import os
import subprocess



class SettingsDialog(qtw.QDialog, Ui_SettingsDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.editSaveLocation.setText(parent.settings.value("save_location", "../widgets"))
    
    def saveSettings(self):
        self.parent().settings.setValue("save_location", self.editSaveLocation.text())
