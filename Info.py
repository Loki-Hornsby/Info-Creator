from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui

import os
import platform
import sys
import time
from datetime import datetime
import subprocess

class Utilities:
    class UI:
        # Update file
        def Update(self, list):
            print("up " + self.SelectedFile)
        
        # Update all files
        def UpdateAll(self, list):
            print("up* " + self.SelectedFile)
        
        # Delete file
        def Delete(self, list):
            self.files.remove(self.SelectedFile)
            list.takeItem(self.SelectedIndex)
            Utilities.Folder.Delete(self.SelectedFile)
        
        # Edit settings
        def EditSettings(self, list):
            print("ed " + self.SelectedFile)

        # List
        def CreateList(self, items, layout, row, column, rowspan, columnspan, action):
            listwidget = QListWidget()

            for i in range(len(items)):
                item = QListWidgetItem(items[i])
                listwidget.addItem(item) 

            layout.addWidget(listwidget, 
                row, column,
                rowspan, columnspan
            )

            listwidget.clicked.connect(action)

            return listwidget

        # Button
        def CreateButton(self, text, layout, row, column, rowspan, columnspan, action):
            button = QPushButton(text)
            
            layout.addWidget(button, 
                row, column,
                rowspan, columnspan
            )

            button.clicked.connect(action)

            return button

        # Dynamic Popup
        def ShowDialogue(self, icon, text, title, action, buttons):
            msgBox = None

            msgBox = QMessageBox(self)
            msgBox.setIcon(icon)
            msgBox.setText(text)
            msgBox.setWindowTitle(title)
            if action != None: msgBox.buttonClicked.connect(action)
            msgBox.setStandardButtons(buttons)

            msgBox.show()

            return msgBox

        # Confirm Writing
        def QueryConfirmation(self):
            confirm = Utilities.UI.ShowDialogue( 
                self,
                QMessageBox.Warning,
                "Warning! \n" + "This will create " + "!~0~!" + " files\nare you sure?",
                "Warning!",
                None, 
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )

            ex = confirm.exec()

            if ex == QMessageBox.Yes:
                return "Yes"
            elif ex == QMessageBox.No:
                return "No"
            elif ex == QMessageBox.Cancel:
                return "Cancel"

        # Request folder location
        def RequestLocation(self):
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setViewMode(QFileDialog.Detail)

            if dialog.exec():
                return dialog.directory().absolutePath()
            else:
                Utilities.UI.ShowDialogue( 
                    self,
                    QMessageBox.Information,
                    "Cancelled Operation",
                    "Info!",
                    lambda:quit(),
                    QMessageBox.Ok,
                )

                return None

    class Folder:
        # View file
        def View(self, file):
            process = QProcess(self)
            process.startDetached('cmd.exe', ['/c', file])

        # Delete file
        def Delete(file):
            os.remove(file)

        def CreateFile(dir, name):
            with open(os.path.join(dir, name), "w") as f:
                f.close()

        # Find files given inputs
        def FindFiles(self, filename, path):
            results = []

            # Walking top-down from the root
            for root, dir, files in os.walk(self.path):
                Utilities.Folder.CreateFile(root, self.filename)

                if self.filename in files:
                    results.append(os.path.join(root, self.filename).replace("\\", "/"))

            return results

        # Get creation date of folder
        def GetCreationDate(self, path_to_file):
            if platform.system() == 'Windows':
                literal_time = os.path.getctime(path_to_file)
                converted_time = str(datetime.fromtimestamp(literal_time).strftime('This folder was created on %Y-%m-%d at %H:%M:%S!'))

                return converted_time
            else:
                print("Not supported!")

class Window(QWidget):
    # Initialize app
    def __init__(self):
        super(Window, self).__init__()

        # Stay ontop
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Set Filename
        self.filename = "Info.txt"

        # Main Func
        self.Main()
    
    # Clicked item in list
    def clicked(self, index):
        self.SelectedItem = self.listwidget.currentItem() 
        self.SelectedIndex = self.listwidget.indexFromItem(self.SelectedItem).row()
        self.SelectedFile = self.files[self.SelectedIndex]

    # Create and show list window
    def List(self):
        # Show Window
        self.show()

        # Layout
        layout = QGridLayout()
        self.setLayout(layout)

        # List
        items = []
        Indent = ""

        for i in range(len(self.files)):
            text = self.files[i]

            if i > 0:
                string = ""
                lastSlashIndex = text.rfind("/") # index of Last occurrence of character "/"
                before = text[:lastSlashIndex].replace(self.path, "") # text before the last occurrence of "/" - removing the root path
                after = text[lastSlashIndex:] # after the last occurrence of "/"
                
                folders = before.count("/") # amount of occurrences of "/"
                string = str(folders * "    ") + "..." + before + after # folders * indent + "..." + text before "/" + text after "/"
            else:
                string = text

            items.append(string)

        self.listwidget = Utilities.UI.CreateList(self, items, layout, 1, 1, 1, 5, self.clicked)


        # Buttons
        self.Edit = Utilities.UI.CreateButton(self, "Edit Settings", layout, 
            2, 1, 
            1, 1, 
            lambda: Utilities.UI.EditSettings(
                self, 
                self.listwidget
            ))

        self.UpdateAll = Utilities.UI.CreateButton(self, "Update All", layout, 
            2, 2, 
            1, 1, 
            lambda: Utilities.UI.UpdateAll(
                self, 
                self.listwidget
            ))

        self.Delete = Utilities.UI.CreateButton(self, "Delete", layout, 
            2, 3, 
            1, 1, 
            lambda: Utilities.UI.Delete(
                self, 
                self.listwidget
            ))

        self.Update = Utilities.UI.CreateButton(self, "Update", layout, 
            2, 4, 
            1, 1, 
            lambda: Utilities.UI.Update(
                self, 
                self.listwidget
            ))

        self.View = Utilities.UI.CreateButton(self, "View", layout, 
            2, 5, 
            1, 1, 
            lambda: Utilities.Folder.View(
                self, self.SelectedFile
            ))

    # Main Function
    def Main(self):
        # Folder location
        self.FolderLocation = Utilities.UI.RequestLocation(self)

        if self.FolderLocation != None:
            # Setup path and folders
            self.path = self.FolderLocation + r"/"
            self.folders = next(os.walk(self.path))[1]
            
            # Confirmation for scanning and writing
            query = Utilities.UI.QueryConfirmation(self)
            
            if query == "Yes": # Show list of files and fill in any missing files
                self.files = Utilities.Folder.FindFiles(self, self.filename, self.path)

                self.List()
            elif query == "No": # Restart Program
                self.Main() 
            elif query == "Cancel": # Quit program
                quit()

# Run App
if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)
  
    # create the instance of our Window
    window = Window()

    sys.exit(App.exec_())