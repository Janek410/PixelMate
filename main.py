
import sys

from PySide6.QtWidgets import QApplication
from core.pet_window import PetWindow

app = QApplication(sys.argv)

pet = PetWindow()
pet.show()

sys.exit(app.exec())
