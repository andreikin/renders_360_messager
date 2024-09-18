import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QPushButton, QLabel, QHBoxLayout, \
    QVBoxLayout

from constants import FILE_LIST_ROW_HEIGHT


class FileItemWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.delete_button = QPushButton("x")
        self.delete_button.setFixedSize(30, FILE_LIST_ROW_HEIGHT)
        self.label = QLabel(text)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.label)
        self.setLayout(layout)
        css = '''   QPushButton {	
                        color:#fff;
                        background-color: #272a33;
                        font: normal 12pt "Segoe UI";
                        border: none;
                        }
                    QPushButton:hover {
                        color: #40a7e3;
                        }
                    QLabel{color:#fff;
                        background-color:  #272a33;
                        font: normal 12pt "Segoe UI";
                        }
                    '''
        self.setStyleSheet(css)


class FileListWidget(QListWidget):
    def __init__(self, ):
        super().__init__()
        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.update_height()
        self.setStyleSheet("QListWidget {padding: 10px 10px 2px 20px;"
                           "border-radius: 5px;"
                           "background-color:  #272a33;}")

    def clear(self):
        super().clear()
        self.update_height()

    def update_height(self):
        items_number = len(self.get_data())
        height = max(FILE_LIST_ROW_HEIGHT * 2, FILE_LIST_ROW_HEIGHT * (items_number+1))
        self.setFixedHeight(height)

    def create_item(self, text):
        list_item = QListWidgetItem(self)
        item_widget = FileItemWidget(text)
        list_item.setSizeHint(item_widget.sizeHint())
        self.setItemWidget(list_item, item_widget)
        list_item.setData(Qt.UserRole, text)
        item_widget.delete_button.clicked.connect(lambda: self.remove_list_item(list_item))
        self.update_height()

    def remove_list_item(self, list_item):
        row = self.row(list_item)
        self.takeItem(row)
        self.update_height()

    def get_data(self):
        """
        Method to get all file paths
        """
        paths = []
        for index in range(self.count()):
            list_item = self.item(index)
            file_path = list_item.data(Qt.UserRole)
            paths.append(file_path)
        return paths

    def dragEnterEvent(self, event):
        """
        Allow drops only for files
        """
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """
        Allow the drop to continue if these are files
        """
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Handling the drop event
        """
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                try:
                    if file_path not in self.get_data():
                        self.create_item(file_path)
                        self.update_height()

                except Exception as e:
                    print(e)
        else:
            event.ignore()


if __name__ == '__main__':
    class MainWindow(QWidget):
        def __init__(self):
            super().__init__()
            layout = QVBoxLayout()
            self.list_widget = FileListWidget()
            self.list_widget.setMinimumHeight(60)
            layout.addWidget(self.list_widget)
            self.setLayout(layout)

            test_button = QPushButton("Показать все пути файлов")
            test_button.clicked.connect(self.show_paths)
            layout.addWidget(test_button)

        def show_paths(self):
            paths = self.list_widget.get_data()
            print("Пути всех файлов:", paths)


    app = QApplication(sys.argv)
    # Создаем главное окно
    window = MainWindow()
    window.setWindowTitle("Список с удаляемыми элементами и дропом файлов")
    window.resize(600, 400)
    window.show()

    sys.exit(app.exec_())
