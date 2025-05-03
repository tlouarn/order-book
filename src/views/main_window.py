from PySide6.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QHBoxLayout, QStatusBar
from qasync import asyncSlot

from src.handlers.bitfinex_handler import BitfinexHandler
from src.models.order_book import OrderBookModel
from src.views.order_book import OrderBookView
from src.views.toggle_button import ToggleButton


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BTC/USD")
        self.resize(420, 190)

        # Adapter
        self.handler = BitfinexHandler()
        self.handler.register_callback(self.handle_message)
        self.handler.connected.connect(self.show_connected_status)
        self.handler.disconnected.connect(self.show_disconnected_status)

        # Model
        self.order_book = OrderBookModel()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Layout
        self.toggle_button = ToggleButton()
        self.toggle_button.clicked.connect(self.toggle)
        self.button_bar = QHBoxLayout()
        self.button_bar.addWidget(self.toggle_button)
        self.button_bar.addStretch()
        self.table = OrderBookView()
        self.table.setModel(self.order_book)
        layout = QVBoxLayout()
        layout.addLayout(self.button_bar)
        layout.addWidget(self.table)
        self.main_widget = QWidget()
        self.main_widget.setLayout(layout)
        self.setCentralWidget(self.main_widget)

    def toggle(self):
        if not self.toggle_button.isChecked():
            self.start()
            self.toggle_button.set_stop()
        else:
            self.stop()
            self.toggle_button.set_start()

    @asyncSlot()
    async def start(self):
        self.toggle_button.setDisabled(True)
        self.status_bar.showMessage("Status: Connecting...")
        await self.handler.open()
        await self.handler.listen()

    @asyncSlot()
    async def stop(self):
        self.order_book.clear()
        self.toggle_button.setDisabled(True)
        self.status_bar.showMessage("Status: Disconnecting...")
        await self.handler.close()

    def handle_message(self, message: list | dict) -> None:
        if isinstance(message, list) and message[1] == "hb":
            return

        if isinstance(message, list):
            if len(message[1]) == 50:
                self.order_book.add_snapshot(snapshot=message[1])
                self.order_book.layoutChanged.emit()
            elif len(message[1]) == 3:
                self.order_book.add_update(update=message[1])
                self.order_book.layoutChanged.emit()

    def show_connected_status(self):
        self.status_bar.showMessage("Status: Connected")
        self.toggle_button.setDisabled(False)

    def show_disconnected_status(self):
        self.status_bar.showMessage("Status: Disconnected")
        self.toggle_button.setDisabled(False)
