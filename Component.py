from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
import pymysql
import ast


def MyConverter(mydata):
    def cvt(data):
        try:
            return ast.literal_eval(data)
        except Exception:
            return str(data)

    return tuple(map(cvt, mydata))


# read only class for table widget
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        print('cells are readonly')
        return


class Component(QDialog):
    def __init__(self):
        super().__init__()
        self.inItUi()
        self.loadData()
        self.tableWidget.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            index = self.tableWidget.indexAt(event.pos())
            data = self.textbox.text()
            if index.data():
                self.textbox.setText(data + index.data())
        return super().eventFilter(source, event)

    def addButton(self):
        textboxData = self.textbox.text()
        textboxData = textboxData + " + "
        self.textbox.setText(textboxData)

    # =========== Database connection function =================
    def loadData(self):
        db = pymysql.connect(host='35.223.238.107', user='root', password='aryabhat', database='Component')
        # db = pymysql.connect(
        #     host='localhost',
        #     user='root',
        #     password='',
        #     database='testdb'
        # )
        with db:
            cur = db.cursor()
            cur.execute("select Name from Compound")
            # cur.execute("SELECT Formula FROM mytable")
            data = cur.fetchall()

            for row in data:
                self.addTable(MyConverter(row))
            cur.close()

    # read table data from QtableWidget
    def readTableData(self):
        rowCount = self.tableWidget.rowCount()
        columnCount = self.tableWidget.columnCount()

        for row in range(rowCount):
            rowData = ''
            for column in range(columnCount):
                widgetItem = self.tableWidget.item(row, column)
                if widgetItem and widgetItem.text:
                    rowData = rowData + '+' + widgetItem.text()
                else:
                    rowData = rowData + '+' + 'NULL'
            print(rowData + '\n')

    def addTable(self, columns):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        for i, column in enumerate(columns):
            self.tableWidget.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))

    def inItUi(self):
        self.resize(271, 269)
        self.widget = QWidget(self)
        self.widget.setGeometry(QtCore.QRect(10, 10, 251, 251))

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout = QHBoxLayout()

        # Create textbox & "+" button
        self.textbox = QLineEdit(self.widget)
        self.horizontalLayout.addWidget(self.textbox)
        self.add_button = QPushButton(self.widget)
        self.add_button.setText(" + ")
        self.add_button.clicked.connect(self.addButton)
        self.horizontalLayout.addWidget(self.add_button)
        self.equal_button = QPushButton(self.widget)
        self.equal_button.setText(" = ")
        self.horizontalLayout.addWidget(self.equal_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(self.widget)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        delegate = ReadOnlyDelegate(self)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        # self.tableWidget.setItemDelegateForColumn(1, delegate)

        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)

        # item = QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(1, item)

        self.verticalLayout.addWidget(self.tableWidget)
        self.add_row = QPushButton(self.widget)
        self.add_row.setText("Add Row")
        self.verticalLayout.addWidget(self.add_row)

        self.del_row = QPushButton(self.widget)
        self.del_row.setText("Delete row")
        self.verticalLayout.addWidget(self.del_row)

        self.setWindowTitle("Components")
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("Compound Formula")
        # item = self.tableWidget.horizontalHeaderItem(1)
        # item.setText("Name")

