# camera.py
class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target):
        # Центрируем камеру на игроке
        self.x = target.x + target.width // 2 - self.width // 2
        self.y = target.y + target.height // 2 - self.height // 2

        # Ограничение (опционально)
        self.x = max(0, self.x)
        self.y = max(0, self.y)