
import os
import queue
import tempfile
import types
from pathlib import Path
from pprint import pprint

from PyQt5 import QtCore, QtWidgets
import moviepy.editor as editor
from telepot.namedtuple import InputMediaVideo

from constants import SETTINGS_FILE, SENDING_TMP_FILE
from file_list_widget import FileListWidget
from settings import PROJECT_LIST, RENDER_BOT_ID, ARDENA_BOT_ID, TEST_MODE, BOT_ID
from window import Ui_MainWindow

import telepot
from environs import Env

env = Env()  # Создаем экземпляр класса Env
env.read_env()  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение
BOT_TOKEN = env('BOT_TOKEN')  # Получаем и сохраняем значение переменной окружения в переменную

if TEST_MODE:
    ARDENA_BOT_ID = BOT_ID
    RENDER_BOT_ID = BOT_ID

class BaseThread(QtCore.QThread):
    def __init__(self, queue, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.queue = queue

    def run(self):
        while True:
            func = self.queue.get()  # Get task
            if func:
                func()  # Run input function
                self.queue.task_done()


class ThreadQueue:
    """
    Creates a separate thread with a queue in which functions are dropped
    """
    def __init__(self):
        self.queue = queue.Queue()  # Create a queue
        self.threads = []
        self.thread = BaseThread(self.queue)
        self.threads.append(self.thread)
        self.thread.start()

    def add_task(self, func):
        self.queue.put(func)


class Messanger(ThreadQueue):
    def __init__(self):
        ThreadQueue.__init__(self)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.setWindowTitle("Render 360 sender")
        self.window.setMinimumWidth(700)

        self.ui.messaje_button.clicked.connect(self.run_thread)
        self.ui.project_combo_box.addItems(PROJECT_LIST)
        self.ui.project_combo_box.currentIndexChanged.connect(self.switch_project)
        self.ui.path_button.clicked.connect(self.add_path)

        file_path = os.path.join(tempfile.gettempdir(), SETTINGS_FILE)
        self.settings = QtCore.QSettings(file_path, QtCore.QSettings.IniFormat)

        self.ui.file_list_widget = FileListWidget([])

        self.ui.path_layout.insertWidget(0, self.ui.file_list_widget)

        self.ui.progressBar.hide()


        self.window.show()
        self.load_settings()

    def add_path(self):
        if self.settings.contains('video_folder'):
            saved_dir = str(Path(self.settings.value('video_folder')).parent)
        else:
            saved_dir = QtCore.QDir.currentPath()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.window, "Select file", saved_dir,
                                                             "MP4 Video Files (*.mp4)", None,
                                                             QtWidgets.QFileDialog.DontConfirmOverwrite)

        if not file_path:
            return

        self.ui.file_list_widget.create_item(file_path, file_path)
        self.settings.setValue('video_folder', file_path)


    def clear_fields(self):
        self.ui.path_line_edit.clear()
        self.ui.name_line_edit.clear()
        self.ui.message_text_edit.clear()

    def get_data(self):
        text = self.ui.message_text_edit.toPlainText()
        text = text + "\n" if text else ""
        asset = self.ui.name_line_edit.text()


        data = {'file_path': self.ui.file_list_widget.get_list()}


        if not asset or not data['file_path']:
            print("The asset or file name being sent is not specified.")
            self.ui.name_line_edit.setPlaceholderText('Enter the asset name here')
        #     self.ui.path_line_edit.setPlaceholderText('Specify the path to the video file')
            return

        data['project'] = self.ui.project_combo_box.currentText()
        wareframe = '#wareframe' if self.ui.wareframe_check_box.isChecked() else ""
        data['message'] = f'{text}{data["project"]} #{asset} {wareframe}'

        pprint(data)

        return data

    def run_thread(self):
        data = {}
        # data = self.get_data()
        # if not data:
        #     return
        self.add_task(lambda: self.send_message(data))
        # self.clear_fields()

    def send_message(self, data):
        try:
            # file_path = data['file_path']
            # if self.is_file_larger_than_45mb(file_path):
            #     new_name = os.path.join(tempfile.gettempdir(), SENDING_TMP_FILE)
            #     clip = editor.VideoFileClip(file_path)
            #     clip.write_videofile(new_name)
            #     file_path = new_name

            bot = telepot.Bot(BOT_TOKEN)
            file_path = 'C:/Users/avbeliaev/Desktop/video_2024-06-27_09-41-42.mp4'

            # medias = [types.InputMediaPhoto('https://habrastorage.org/webt/61/99/de/6199de8312758776787774.png'),types.InputMediaPhoto(
            #               'https://habrastorage.org/getpro/habr/upload_files/1fd/40a/c44/1fd40ac441a0aee55fc90e67997437af.png')]

            f_media = InputMediaVideo()



            print (f_media)
            #bot.sendMediaGroup(RENDER_BOT_ID, media=[f_media, f_media])


            # bot = telepot.Bot(BOT_TOKEN)
            # with open(file_path, 'rb') as f:
            #     bot.sendVideo(RENDER_BOT_ID, f, caption=data['message'])
            #
            # if data['project'] == PROJECT_LIST[0]:
            #     with open(file_path, 'rb') as f:
            #         bot.sendVideo(ARDENA_BOT_ID, f, caption=data['message'])

        except Exception as message:
            print(message)

    @staticmethod
    def is_file_larger_than_45mb(file_path):
        file_size = os.path.getsize(file_path)
        size_in_bytes = 45 * 1024 * 1024  # 45 МБ в байтах
        return file_size > size_in_bytes


    def load_settings(self):
        """
        Load settings
        """
        try:
            if self.settings.contains("current project"):
                self.ui.project_combo_box.setCurrentIndex(int(self.settings.value("current project")))
        except Exception as message:
            print(message)

    def switch_project(self):
        self.settings.setValue("current project", self.ui.project_combo_box.currentIndex())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Messanger()  # Создаем экземпляр класса
    sys.exit(app.exec_())  # Запускаем цикл обработки событий
