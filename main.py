import sys
from PyQt6.QtWidgets import QApplication
from .core import optimizers

from gui.app_window import MultidimOptApp
from gui import InputSection, ResultSection


def main():
    app = QApplication(sys.argv)
    window = MultidimOptApp(
        input_section=InputSection(optimizers.keys()),
        results_section=ResultSection(),
        optimizers=optimizers,
    )
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()