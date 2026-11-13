from PySide6.QtCore import Qt, QTimer

from pathlib import Path
from PySide6.QtGui import QPixmap, QPainter

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

class PetWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PixelMate")
        self.setFixedSize(192,192)
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True
        )

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.drag_position = None

        sprite_path = (Path(__file__).parent.parent
        /"assets"
        /"sprites"
        /"idle"
        /"base1.png"
        )

        self.base_sprite = QPixmap(str(sprite_path))
        self.sprite = self.base_sprite

        blink_path = (Path(__file__).parent.parent
        /"assets"
        /"sprites"
        /"idle"
        /"blink1.png"
        )

        self.blink_sprite = QPixmap(str(blink_path))

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink)
        self.blink_timer.start(3000)

        fall_path = (Path(__file__).parent.parent
        /"assets"
        /"sprites"
        /"idle"
        /"fall"
        )

        self.fall_sprites = [
            QPixmap(str(fall_path / f"falling{i}.png"))
            for i in range(1,5)
        ]

        self.fall_frame = 0

        self.fall_timer = QTimer(self)
        self.fall_timer.timeout.connect(self.animate_fall)
        self.fall_timer.start(120)

        #grawitacja
        self.velocity_y = 0
        self.gravity = 1800
        self.is_dragging = False

        self.physics_timer = QTimer(self)
        self.physics_timer.timeout.connect(self.apply_gravity)
        self.physics_timer.start(16)



    def mousePressEvent(self, event):

        self.is_dragging = True
        self.physics_timer.stop()

        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (event.globalPosition().toPoint() - self.frameGeometry().topLeft())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):

        self.is_dragging = False
        self.velocity_y = 0
        self.physics_timer.start(16)

        #uruchom animacje po puszczeniu
        self.fall_timer.start(120)

        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform,
            False
        )

        scaled_sprite = self.sprite.scaled(
            192,
            192,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        x = (self.width() - scaled_sprite.width()) // 2
        y = (self.height() - scaled_sprite.height()) // 2

        painter.drawPixmap(x, y, scaled_sprite)

    #mruganie
    def blink(self):
        self.sprite = self.blink_sprite
        self.update()

        QTimer.singleShot(180, self.open_eyes)

    def open_eyes(self):
        self.sprite = self.base_sprite
        self.update()

    #spadanie
    def apply_gravity(self):
        if self.is_dragging:
            return

        screen = self.screen().availableGeometry()

        ground_y = screen.y() + screen.height() - self.height() + 10

        if self.y() >= ground_y:
            self.move(self.x(), ground_y)
            self.velocity_y = 0
            self.physics_timer.stop()

            #do animacji spadania
            self.fall_timer.stop()
            self.sprite = self.base_sprite
            self.update()

            return

        self.velocity_y += self.gravity * 0.016

        new_y = self.y() + int(self.velocity_y * 0.016)

        self.move(self.x(), min(new_y, ground_y))

    def animate_fall(self):
        if self.is_dragging:
            return

        if self.physics_timer.isActive():
            self.fall_frame = (self.fall_frame + 1) % len(self.fall_sprites)
            self.sprite = self.fall_sprites[self.fall_frame]
            self.update()

