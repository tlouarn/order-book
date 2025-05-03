from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class OrderBookModel(QAbstractTableModel):
    ROWS = 5
    COLUMNS = 4
    HEADERS = ["BidQty", "Bid", "Ask", "AskQty"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bids = {}
        self.asks = {}

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.ROWS

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.COLUMNS

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | int:
        bids = sorted(self.bids.items(), key=lambda x: -x[0])[:5]
        asks = sorted(self.asks.items(), key=lambda x: x[0])[:5]

        if role == Qt.ItemDataRole.DisplayRole and bids and asks:
            match index.column():
                case 0:
                    bid_quantity = bids[index.row()][1]
                    return f"{bid_quantity:.6f}"
                case 1:
                    bid_price = bids[index.row()][0]
                    return f"{bid_price:,.0f}"
                case 2:
                    ask_price = asks[index.row()][0]
                    return f"{ask_price:,.0f}"
                case 3:
                    ask_quantity = asks[index.row()][1]
                    return f"{ask_quantity:.6f}"

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole) -> str:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]

    def add_snapshot(self, snapshot: list[list]) -> None:
        for update in snapshot:
            self.add_update(update)

    def add_update(self, update: list) -> None:
        price, count, amount = update

        if count == 0 and amount > 0:
            self.bids.pop(price, None)
            return

        if count > 0 and amount > 0:
            self.bids[price] = amount
            return

        if count == 0 and amount < 0:
            self.asks.pop(price, None)
            return

        if count > 0 and amount < 0:
            self.asks[price] = -1 * amount
            return

    def clear(self) -> None:
        self.bids = {}
        self.asks = {}
