# Info Creator
 Creates a text file with info about the folder for convenience
 
 I do plan to add more features to this later such as multiple folder support but its not a high priority


```python
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

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

        # Folder location
        self.Folder = ""

        # Counter
        self.created = 0
        self.ignored = 0
        
        # Get folder location
        self.request_location()

        # Set Filename
        self.fname = "Info.txt"

        # fill folders with text file
        self.fill_folders()

        # Show finish dialogue
        self.ShowFinishDialogue()

    def void(self):
        print("Done!")

    # Finished popup
    def ShowFinishDialogue(self):
        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText(str(self.created) + " files created!" + "\n" + str(self.ignored) + " files alreay exist!")
        self.msgBox.setWindowTitle("Info!")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.buttonClicked.connect(self.void)
        self.msgBox.show() # this is so stupid but it makes sense why this exists - took me a good 20 minutes to add this line of code in :P

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
    def fill_folders(self):
        path = self.Folder + r"/"
        folders = next(os.walk(path))[1]
        print(os.listdir())

        for folder in folders:
            local_path = path + folder + r"/" + self.fname
            print(local_path)
                
            if not os.path.exists(local_path):
                f = open(local_path, "w+")
                f.write(self.creation_date(local_path))
                f.close()

                self.created += 1
            else:
                self.ignored += 1

        #print(str(created) + " files created")
        #print(str(ignored) + " files already created")
        
        #quit()
        
# Run App
if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)
  
    # create the instance of our Window
    window = Window()

    # Show window
    #window.show()

    sys.exit(App.exec_())
```
