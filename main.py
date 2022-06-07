from theme import Ui_MainWindow
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys
import os
import yt_dlp


# Initialization of Main Screen
app = QtWidgets.QApplication(sys.argv)
mainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mainWindow)

new_file_name = None
current_save_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
ui.savePath.setText(current_save_dir)


def downloadMedia(URL):
    def hook(d):
        if d['status'] == 'finished':
            ui.status.setText("Done!")

        if d['status'] == 'downloading':
            total_bytes = d['total_bytes']
            downloaded_bytes = d['downloaded_bytes']
            download_speed = d['speed']
            
            total_bytes_text = str(round((total_bytes/1000000), 2)) + " mb"
            downloaded_bytes_text = str(round((downloaded_bytes/1000000), 2)) + " mb"
            download_speed_text = str(round((download_speed/1000000), 2)) + " mb/s"
            percentage = (int)((downloaded_bytes * 100) / total_bytes)
            
            def changeText():
                ui.fileSize.setText(total_bytes_text)
                ui.downloadedBytes.setText(downloaded_bytes_text)
                ui.downloadSpeed.setText(str(download_speed_text))
                ui.DownloadPercentage.setText(str(percentage) + "%")
                ui.status.setText("Downloading!")

            threading.Thread(
                target=changeText, daemon=True
            ).start()
            

    temp_file_name = ui.newFileName.text()
    if temp_file_name != "":
        new_file_name = temp_file_name
    else:
        new_file_name = None

    if new_file_name == None or new_file_name == "":
        ydl_opts = {
            'progress_hooks': [hook],
            'outtmpl': current_save_dir + '/%(title)s.%(ext)s',
        }
    else:
        ydl_opts = {
            'progress_hooks': [hook],
            'outtmpl': current_save_dir + '/'+ new_file_name +'.%(ext)s',
        }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        def _download():
            ydl.download(URL)

        threading.Thread(
            target=_download, daemon=True
        ).start()
        



def prepareDownload():
    url_address = ui.urlTextBox.text()
    downloadMedia(url_address)

def selectNewPath():
    current_save_dir = str(QFileDialog.getExistingDirectory(mainWindow, "Select Directory"))
    ui.savePath.setText(current_save_dir)
    

ui.downloadButton.clicked.connect(prepareDownload)
ui.selectPathButton.clicked.connect(selectNewPath)


mainWindow.show()
sys.exit(app.exec_())



