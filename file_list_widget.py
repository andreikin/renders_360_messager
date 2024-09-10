import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListView, QWidget, QHBoxLayout, QPushButton, QAbstractItemView
from PyQt5.QtCore import Qt


class DeleteItemButton(QWidget):
    def __init__(self, in_item, in_widget, parent=None):
        super(DeleteItemButton, self).__init__(parent)
        self.in_widget = in_widget
        self.item = in_item
        layout = QHBoxLayout(self)

        self.button = QPushButton("x")
        self.button.clicked.connect(self.btn_function)
        self.button.setFixedSize(self.in_widget.item_height-2, self.in_widget.item_height-2, )
        layout.addWidget(self.button, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.setContentsMargins(0, 0, 5, 0)
        self.button.setStyleSheet("background-color:#1f232a; color:#fff;")


    def btn_function(self):
        try:
            self.in_widget.model.removeRow(self.item.row())
            self.in_widget.set_height()

        except Exception as message:
            print(message)

class FileListWidget(QListView):
    """
    class creates a list of files with a button to delete each of them
    """

    def __init__(self, files_list, parent=None):
        super(FileListWidget, self).__init__(parent=parent)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.item_height = 30
        self.min_height = self.item_height * 2
        self.model = QStandardItemModel(self)

        self.setModel(self.model)
        self.setStyleSheet("QListView {padding: 10px 10px 2px 20px;"
                           "border-radius: 5px;"
                           "background-color:#1f232a;}"
                           "QListView:item {"
                           "color:#fff;"
                           "height: " + str(self.item_height) + "px;}")
        if files_list:
            self.add_files_list(files_list)
        self.set_height()

    def remove_item(self, file_path):
        try:
            for index in range(self.model.rowCount()):
                item = self.model.item(index)
                path = item.data(role=Qt.ToolTipRole)
                if file_path == path:
                    self.model.removeRow(item.row())
                    self.set_height()
        except Exception as message:
            print(message)

    def create_item(self, file_path):
        try:
            if not self.is_file_in_widget(file_path):
                file_name = os.path.basename(file_path)
                label = file_name if len(file_name) < 30 else file_name[:29] + "..."
                item = QStandardItem(label)
                item.setData(file_path, role=Qt.ToolTipRole)
                self.model.appendRow(item)
                self.setIndexWidget(item.index(), DeleteItemButton(item, self))
                self.set_height()
        except Exception as message:
            print(message)

    def is_file_in_widget(self, file):
        return file in self.get_list()

    def add_file(self, file_path):
        self.create_item(file_path)

    def add_files_list(self, files_list):
        for file_path in files_list:
            self.create_item(file_path)

    def get_list(self):
        path_list = []
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            path_list.append(item.data(role=Qt.ToolTipRole))
        return path_list

    def set_height(self):
        """
        sets the height of the widget according to the amount of content
        """
        files_list = self.get_list()
        content_height = len(files_list) * self.item_height
        if self.min_height < content_height + 20:
            self.setFixedHeight(content_height + 20)
        else:
            self.setFixedHeight(self.min_height + 20)

    def clear(self):
        self.model.clear()
        self.set_height()

    def dropEvent(self, event):
        mimedata = event.mimeData()
        if mimedata.hasUrls():
            for f in mimedata.urls():
                self.add_file(f.path()[1:])

    def dragEnterEvent(self, event):
        if event.source() is self:
            event.ignore()
        else:
            mimedata = event.mimeData()
            if mimedata.hasUrls():
                event.accept()
            else:
                event.ignore()

    def dragMoveEvent(self, event):
        if event.source() is self:
            event.ignore()
        else:
            mimedata = event.mimeData()
            if mimedata.hasUrls():
                event.accept()
            else:
                event.ignore()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    f_list = ['ghjfghjfg', "fkjfkf", "ghgkghjkgh"]

    window = FileListWidget(f_list) # Создаем экземпляр класса
    window.setWindowTitle("ООП-стиль создания окна")
    window.resize(500, 70)
    window.show() # Отображаем окно
    sys.exit(app.exec_()) # Запускаем цикл обработки событий