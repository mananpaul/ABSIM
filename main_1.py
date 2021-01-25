
"""Libraries"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from KilnDialog import *
from Component import *

# ===================== Class OurMimeData ======================
class OurMimeData(QMimeData):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def getName(self):
        return self.name

# ===================== Class QDragLabel ======================
class QDragLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, mimeName, parent=None):
        # super().__init__()
        super(QDragLabel, self).__init__(parent)
        self.mimeName = mimeName

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            data = QByteArray()
            mime_data = OurMimeData(self.mimeName)
            mime_data.setData(self.mimeName, data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(self.rect().topLeft())  # where do we drag from
            if QT_VERSION_STR < '5':
                drop_action = drag.start(Qt.MoveAction)  # drag starts
            else:
                drop_action = drag.exec(Qt.MoveAction)  # drag starts

# ===================== Class ToolbarArrow ======================

class ToolbarArrow(QDragLabel):
    def __init__(self, pos):
        if pos == "left":
            super().__init__("left")
            self.arrow_left()
        elif pos == "right":
            super().__init__("right")
            self.arrow_rigth()
        elif pos == "top":
            super().__init__("top")
            self.arrow_top()
        elif pos == "down":
            super().__init__("down")
            self.arrow_down()

    def arrow_left(self):
        picture = QPixmap("images//left.png")
        self.setPixmap(picture.scaled(20, 10))
        self.mimetext = "application/x-arrow"

    def arrow_rigth(self):
        picture = QPixmap("images//right.png")
        self.setPixmap(picture.scaled(20, 10))
        self.mimetext = "application/x-arrow"

    def arrow_top(self):
        picture = QPixmap("images//top.png")
        self.setPixmap(picture.scaled(10, 20))
        self.mimetext = "application/x-arrow"

    def arrow_down(self):
        picture = QPixmap("images//down.png")
        self.setPixmap(picture.scaled(10, 20))
        self.mimetext = "application/x-arrow"

# ===================== Class CustomQGraphicsPixmapItem ======================
class CustomQGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, q, label):
        super().__init__(q)
        self.setAcceptHoverEvents(True)
        self.label = label
        self.create_popup()
        if q == QPixmap("images/left.png"):
            self.current_graphic = QPixmap(q)
            self.setPixmap(self.current_graphic.scaledToWidth(150))
            self.setAcceptHoverEvents(True)
        elif q == QPixmap("images/right.png"):
            self.current_graphic = QPixmap(q)
            self.setPixmap(self.current_graphic.scaledToWidth(150))
            self.setAcceptHoverEvents(True)
        elif q == QPixmap("images/top.png"):
            self.current_graphic = QPixmap(q)
            self.setPixmap(self.current_graphic.scaledToWidth(150))
            self.setAcceptHoverEvents(True)
        elif q == QPixmap("images/down.png"):
            self.current_graphic = QPixmap(q)
            self.setPixmap(self.current_graphic.scaledToWidth(150))
            self.setAcceptHoverEvents(True)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            orig_cursor_position = event.lastScenePos()
            updated_cursor_position = event.scenePos()
            orig_position = self.scenePos()
            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    def create_popup(self):
        self.dg = KilnDialog()

    def mouseDoubleClickEvent(self, event):
        self.dg.exec_()

# ===================== Class DrawingPanel ======================
class DrawingPanel(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.background_brush = QBrush()
        self.background_picture = QPixmap("images/if_we_want_bg_image")
        self.background_brush.setTexture(self.background_picture)
        self.setBackgroundBrush(self.background_brush)
        self.kilns = []

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def drop_position(self, item):
        cursor_position = QCursor.pos()
        current_view = self.views()[0]
        scene_position = current_view.mapFromGlobal(cursor_position)
        width = item.boundingRect().width()
        height = item.boundingRect().height()
        width_offset = width / .5
        height_offset = height / .5
        drop_x = scene_position.x() - width_offset
        drop_y = scene_position.y() - height_offset
        return drop_x, drop_y

    def visualise_graphic_item(self, name):
        # if len(self.kilns)> = 1:return
        print(name)
        kiln = CustomQGraphicsPixmapItem(QPixmap("images/" + name), name)
        kiln.setFlags(QGraphicsItem.ItemIsMovable)
        self.kilns.append(kiln)
        x, y = self.drop_position(self.kilns[-1])
        self.kilns[-1].setPos(x, y)
        self.kilns[-1].setOffset(10, 20)
        self.addItem(self.kilns[-1])

    def dropEvent(self, event):
        event.accept()
        name = event.mimeData().getName()
        if len(name) == 0: return
        self.visualise_graphic_item(name)

    def removeKilns(self):
        if len(self.kilns) <= 0:
            return None
        else:
            item = self.kilns.pop()
            self.removeItem(item)
            return item

    def addKilns(self, item):
        self.addItem(item)
        self.kilns.append(item)

# ===================== Class App ======================
class App(QMainWindow):

    """init"""
    def __init__(self):
        super().__init__()
        self.title = 'AB SIM'
        self.left = 0
        self.top = 0
        self.width = 2000
        self.height = 1000
        #self.initUI()
        self.items = []

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_Menu()
        self.tool_Bar()
        self.module_toolbox()
        self.model_toollist()
        self.draw_Board()

        self.show()

    # ============ Undo Method ============

    def undo(self):
        item = self.drawingBoard.removeKilns()
        if item == None: return
        self.items.append(item)

    # ============ Redo Method ============
    def redo(self):
        if len(self.items) == 0: return
        item = self.items.pop()
        self.drawingBoard.addKilns(item)

    # ============ Test Method ============
    def test(self, toolbar, image):
        button_action = QAction(QIcon(image), "Your button", self)
        toolbar.addAction(button_action)
        toolbar.addSeparator()

    # ============ create_push_button Method ============
    def create_push_button(self, image):
        button = QPushButton()
        button.setIcon(QIcon(image))
        button.setMaximumWidth(20)
        button.setFixedWidth(25)
        return button

    # ============ create_qlabel_with_images Method ============
    def create_qlabel_with_images(self, image):
        label = QLabel()
        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmap)
        return label

    # ============ create_qlabel_with_images Method ============
    def add_model_images(self, mimeName, image, name2, layout_image, ratio1=100, ratio2=100):
        kiln = QDragLabel(mimeName)
        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(ratio1, ratio2, Qt.KeepAspectRatio, Qt.FastTransformation)
        kiln.setPixmap(pixmap)
        layout_image.addWidget(kiln)
        bold_name1 = QLabel(name2)
        bold_name1.setStyleSheet("font-weight:bold")
        layout_image.addWidget(bold_name1)

    def main_Menu(self):

        menulyt = QGridLayout(self)
        mainMenu = self.menuBar()
        #mainMenu.setMinimumSize(self.width,20)
        menulyt.addWidget(mainMenu,0,0)

        """File Menu"""
        fileMenu = mainMenu.addMenu('File')
        newAction = QAction('&New', self)
        #newAction.setShortcut('CTRL+N')
        newAction.setStatusTip('New Document')
        # newAction.triggered.connect(self.newCall)
        fileMenu.addAction(newAction)

        """ Open Menu """
        openAction = QAction('&Open', self)
        #openAction.setShortcut('CTRL+O')
        openAction.setStatusTip('Open Document')
        # openAction.triggered.connect(self.OpenCall)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()

        """Settings Menu"""
        setAction = QAction('&Settings', self)
        #setAction.setShortcut('CTRL+A')
        setAction.setStatusTip('Initial Settings')
        fileMenu.addAction(setAction)
        fileMenu.addSeparator()

        """Exit Menu"""
        exitAction = QAction('&Exit', self)
        #exitAction.setShortcut('CTRL+Q')
        exitAction.setStatusTip('Exit Application')
        # exitAction.triggered.connect(self.ExitCall)
        fileMenu.addAction(exitAction)

        """Edit menu"""
        editMenu = mainMenu.addMenu('Edit')

        """Undo"""

        undoAction = QAction('&Undo', self)
        undoAction.setStatusTip('Undo')
        #undoAction.triggered.connect()
        editMenu.addAction(undoAction)

        """Redo"""

        redoAction = QAction('&Redo', self)
        redoAction.setStatusTip('Redo')
        #redoAction.triggered.connect()
        editMenu.addAction(redoAction)

        """Compound"""

        #self._Component = Component()
        compAction = QAction('&Compound', self)
        compAction.setStatusTip('Connect to Component Database')
        #compAction.triggered.connect(self._Component.exec_)
        editMenu.addAction(compAction)

        eleAction = QAction('&Element', self)
        eleAction.setStatusTip('Connect to Element Database')
        # eleAction.triggered.connect()
        editMenu.addAction(eleAction)

        """Debug menu"""
        debugMenu = mainMenu.addMenu('Debug')

        """ Tools menu"""
        toolsMenu = mainMenu.addMenu('Tools')

        """GIS menu"""
        gisMenu = mainMenu.addMenu('GIS')

        """help menu"""
        helpMenu = mainMenu.addMenu('Help')

    def tool_Bar(self):

        # Menu Tool bar

        toolblyt = QHBoxLayout(self)
        
        toolbar = QToolBar(self)
        toolblyt.addWidget(toolbar,0,0)
        #self.addWidget(toolbar)
        toolbar.setIconSize(QSize(20, 20))
        #toolbar.move(0,50)
        buttons = []

        ii = 13
        for i in range(6):
            buttons.append(self.create_push_button("images/image_" + str(ii)))
            ii += 1

        #toolblyt.addWidget(label)
        toolbar.addWidget(buttons[0])

        toolbar.addWidget(buttons[1])
        toolbar.addWidget(buttons[2])
        toolbar.addWidget(buttons[3])
        toolbar.addWidget(buttons[4])
        toolbar.addWidget(buttons[5])

        for i in range(18):
           self.test(toolbar, "images/image" + str(i))
        # create toolbar

        """Arrow for adding Stream later"""

        self.right = ToolbarArrow("right")
        self.right.setToolTip("Right Arrow")
        # add label to toolbars
        toolbar.addWidget(self.right)
        toolbar.addSeparator()

        # undo redo
        buttons[5].clicked.connect(self.redo)
        buttons[4].clicked.connect(self.undo)

        # add toolbars to window
        #self.addToolBar(self.toolbar)

    def model_toollist(self):

        mtllyt = QVBoxLayout(self)
        mtllyt.setSpacing(5)
        #toollist = QToolBar(self)

        name_label = QLabel("Project")
        name_label.setStyleSheet("font-weight:bold")
        mtllyt.addWidget(name_label)
        mtllyt.setAlignment(Qt.AlignLeft)

    def module_toolbox(self):

        mtoolblyt = QVBoxLayout(self)
        toolbox = QToolBar(self)

        toolbox.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)  # <= Toolbuttonstyle
        mtoolblyt.setAlignment(self, Qt.AlignRight)
        kilnAction = QAction('kiln', self)
        #kilnAction.icon("images/kiln.png")
        toolbox.addAction(kilnAction)
        toolbox.setIconSize(QSize(50, 50))
        toolbox.move(400,100)



        #toolbar.addActions((fileNewAction, faultAction, scheduleAction, storeAction, localAction, settingAction))
        #settings = QtCore.QSettings()
        #self.restoreGeometry(settings.value("Geometry").toByteArray())

        """
        mtoolbox = QListWidget(self)
        tbname = QLabel("ToolBox")
        tbname.setStyleSheet("font-weight:bold")
        #mtoolblyt.setAlignment(self, Qt.AlignRight)

        # setting geometry to it
        mtoolbox.setGeometry(50, 70, 150, 60)

        mtoolblyt.addWidget(tbname)
        mtoolblyt.addWidget(mtoolbox)

        kiln = QListWidgetItem("Kiln")
        dryer = QListWidgetItem("Dryer")
        mtoolbox.addItem(kiln)
        mtoolbox.addItem(dryer)
        
        #self.add_model_images("kiln", "images/kiln.png", "Kiln", layout_image)
        #self.add_model_images("kiln2", "images/kiln2", "Kiln2", layout_image)

        # setting current item
        mtoolbox.setCurrentItem(kiln)

        # creating a label
        label = QLabel("Toolbox", self)

        # setting geometry to the label
        label.setGeometry(230, 80, 280, 80)

        # making label multi line
        label.setWordWrap(True)

        # getting current item
        value = mtoolbox.currentItem()

        # setting text to the label
       # label.setText("Current Item : " + str(value))

        #layout_image.addStretch()

        feature_images = []
        """

    """initUI - Used for UI calling - important to keep the function name the same"""

    def draw_Board(self):

        dblyt = QGridLayout(self)
        dblyt.setRowStretch(0, 1)
        dblyt.setRowStretch(1, 9)
        textEdit = DrawingPanel()

        # adding a property dynamically
        self.drawingBoard = textEdit
        textEdit = QGraphicsView(textEdit)
        rcontent = textEdit.contentsRect()
        textEdit.setSceneRect(0, 0, rcontent.width(), rcontent.height())

        #dblyt.addLayout(toolblyt, 0, 0)
        #dblyt.addLayout(mtoolblyt, 1, 0)

        widget = QWidget()
        widget.setLayout(dblyt)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
