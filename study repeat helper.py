import sys
from PyQt5.QtWidgets import QApplication, QTableView, QAbstractItemView
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QAbstractItemView, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QFileDialog

import csv
from PyQt5.QtWidgets import QFileDialog




def save_data(model):
    file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "CSV Files (*.csv);;All Files (*)")
    if file_name:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in range(model.rowCount()):
                row_data = []
                for column in range(model.columnCount()):
                    cell_value = model.index(row, column).data()
                    row_data.append(cell_value)
                writer.writerow(row_data)


def load_data(model):
    file_name, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)")
    if file_name:
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            model.set_data(data)


class SpreadsheetModel(QAbstractTableModel):
    def __init__(self, rows, columns, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.columns = columns
        self.data = {}

    def rowCount(self, parent=None):
        return self.rows

    def columnCount(self, parent=None):
        return self.columns

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self.data.get((index.row(), index.column()))
            if value is not None:
                return value
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            base_row = index.row()
            target_rows = [base_row + offset for offset in [0, 2, 6, 13, 29, 59]]
            for row in target_rows:
                if row < self.rowCount():
                    existing_value = self.data.get((row, index.column()), "")
                    new_value = existing_value + value
                    self.data[(row, index.column())] = new_value
                    self.dataChanged.emit(self.createIndex(row, index.column()),
                                          self.createIndex(row, index.column()))
            return True
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return f"행  {section + 1}"
            elif orientation == Qt.Vertical:
                return f"열 {section + 1}"
        return None



def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    
   
    view = QTableView()
    model = SpreadsheetModel(10000, 10000)
    view.setModel(model)
    view.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
    view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)


    save_button = QPushButton("저장")
    open_button = QPushButton("열기")


    save_button.clicked.connect(save_data)
    open_button.clicked.connect(load_data)


    button_layout = QHBoxLayout()
    button_layout.addStretch()
    button_layout.addWidget(save_button)
    button_layout.addWidget(open_button)


    main_layout = QVBoxLayout()
    main_layout.addWidget(view)
    main_layout.addLayout(button_layout)


    
    
    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    main_window.setCentralWidget(central_widget)
    main_window.showMaximized()
    main_window.show()
    

    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
