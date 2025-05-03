import asyncio

from qasync import QApplication, QEventLoop

from src.views.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication()
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()
