from PySide6.QtWidgets import QPushButton, QSizePolicy

GREEN_STYLE = """
    QPushButton {
        background-color: #ccffcc;
        border: 1px solid #009900;
        border-radius: 0;
        padding: 6px 12px;
        font: bold 9pt "Calibri";
    }
    
    QPushButton:pressed {
        background-color: #b2ffb2;
    }
"""

RED_STYLE = """
    QPushButton {
        background-color: #ffcccc;
        border: 1px solid #cc0000;
        border-radius: 0;
        padding: 6px 12px;
        font: bold 9pt "Calibri";
    }
    
    QPushButton:pressed {
        background-color: #ffb2b2;
    }
"""


class ToggleButton(QPushButton):

    def __init__(self):
        super().__init__()
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.set_start()
        self.clicked.connect(self.toggle)

    def set_start(self) -> None:
        self.setChecked(False)
        self.setText("START")
        self.setStyleSheet(GREEN_STYLE)

    def set_stop(self) -> None:
        self.setChecked(True)
        self.setText("STOP")
        self.setStyleSheet(RED_STYLE)

    def toggle(self) -> None:
        self.set_start() if self.isChecked() else self.set_stop()
