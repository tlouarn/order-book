from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableView, QHeaderView

STYLE_SHEET = """
   QTableView {
        background-color: white;
        border: 1px solid #CCC;
        font: 9pt "Calibri";
        gridline-color: #EEE;
    }
    
    QHeaderView::section {
        font-weight: bold;
        font-size: 9pt;
        text-align: center;
        background-color: #f0f0f0;
    }
    
    QTableView::item {
        text-align: center;
    }
"""


class OrderBookView(QTableView):
    def __init__(self):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(10)
        self.setFixedSize(400, 150)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet(STYLE_SHEET)

