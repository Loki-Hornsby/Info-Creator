from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui

import os
import platform
import sys
import time
from datetime import datetime
import os

class Window(QWidget):
    # Initialize app
    def __init__(self):
        super(Window, self).__init__()

        # Stay ontop
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Set Filename
        self.fname = "Info.txt"

        # Main Func
        self.Main()

    # Main Function
    def Main(self):
        # Folder location
        self.FolderLocation = ""

        # Get folder location and exit if cancel
        if self.request_location():
            # Setup path and folders
            self.path = self.FolderLocation + r"/"
            self.folders = next(os.walk(self.path))[1]

            # Setup Amount
            self.created = 0
            self.ignored = 0
            self.get_amount()
            
            # Confirm
            if self.Confirm():
                # Fill folders with text files
                self.fill_folders()

                # Show finish dialogue
                self.ShowDialogue( 
                    QMessageBox.Information,
                    str(self.created) + " files created!" + "\n" + str(self.ignored) + " files alreay exist!",
                    "Info!",
                    lambda:quit(),
                    QMessageBox.Ok,
                )

    # Dynamic Popup
    def ShowDialogue(self, icon, text, title, action, buttons):
        msgBox = None

        msgBox = QMessageBox(self)
        msgBox.setIcon(icon)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.buttonClicked.connect(action)
        msgBox.setStandardButtons(buttons)

        msgBox.show()

        return msgBox

    # Request folder location
    def request_location(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec():
            self.FolderLocation = dialog.directory().absolutePath()

            return True
        else:
            self.ShowDialogue( 
                QMessageBox.Information,
                "Cancelled Operation",
                "Info!",
                lambda:quit(),
                QMessageBox.Ok,
            )

            return False

    # Get creation date of folder
    def creation_date(self, path_to_file):
        if platform.system() == 'Windows':
            literal_time = os.path.getctime(path_to_file)
            converted_time = str(datetime.fromtimestamp(literal_time).strftime('This folder was created on %Y-%m-%d at %H:%M:%S!'))

            return converted_time
        else:
            print("Not supported!")

    # Get Folder Amount
    def get_amount(self):
        for folder in self.folders:
            local_path = self.path + folder + r"/" + self.fname

            if not os.path.exists(local_path):
                self.created += 1
            else:
                self.ignored += 1

    # Confirm Writing
    def Confirm(self):
        confirm = self.ShowDialogue( 
            QMessageBox.Warning,
            "Warning! \n" + "This will create " + str(self.created) + " files\nare you sure?",
            "Warning!",
            lambda:print("User Selected: "), 
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )

        ex = confirm.exec()

        if ex == QMessageBox.Yes:
            print("Yes....Writing to location....")
            return True
        elif ex == QMessageBox.No:
            print("No....Reopening Folder Select....")
            self.Main()
            return False
        elif ex == QMessageBox.Cancel:
            print("Cancel....Quitting Application....")
            quit()
            return False
            
    # Write info to folder
    def fill_folders(self):
        for folder in self.folders:
            local_path = self.path + folder + r"/" + self.fname
            if not os.path.exists(local_path):
                f = open(local_path, "w+")
                f.write(self.creation_date(local_path))
                f.close()
                print("Wrote to: " + str(local_path))


# Run App
if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)
  
    # create the instance of our Window
    window = Window()

    sys.exit(App.exec_())



