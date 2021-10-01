from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QFileDialog

import os
import platform
import sys
import time
from datetime import datetime

class Window(QWidget):

    # Initialize app
    def __init__(self):
        super(Window, self).__init__()

        # Folder location
        self.Folder = ""

        # Get folder location
        self.request_location()

        # Write data to file in folder
        self.write_to_file()
        

    # Request folder location
    def request_location(self):
        self.Folder = QFileDialog.getExistingDirectory(self, "Select Directory")

    # Get creation date of folder
    def creation_date(self, path_to_file):
        if platform.system() == 'Windows':
            # this is stupid :P
            literal_time = os.path.getctime(path_to_file)
            converted_time = str(datetime.fromtimestamp(literal_time).strftime('This folder was created on %Y-%m-%d at %H:%M:%S!'))

            return converted_time
        else:
            print("Not supported!")

    # Write info to folder
    def write_to_file(self):
        fname = "Info.txt"
        fpath = self.Folder + "//" + fname
        
        if os.path.exists(self.Folder):
            f = open(fpath, "w+")
            f.write(self.creation_date(self.Folder))
            f.close()

        quit()
        
# Run App
if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)
  
    # create the instance of our Window
    window = Window()

    sys.exit(App.exec_())



