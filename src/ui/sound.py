# sound.py
import pygame
import os

class SoundManager:
    def __init__(self):
        # Инициализируем микшер только если он ещё не запущен
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        # Путь к фоновой музыке
        self.music_path = "assets/sounds/music.mp3" 

        # Загружаем и запускаем музыку
        if os.path.exists(self.music_path):
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.set_volume(0.4)  
                pygame.mixer.music.play(-1) 
            except pygame.error as e:
                print(f"⚠️ Не удалось загрузить музыку: {e}")
                self.music_path = None
        else:
            print("ℹ️ Файл фоновой музыки не найден:", self.music_path)
            self.music_path = None

    def stop_music(self):
        """Остановить фоновую музыку."""
        if self.music_path:
            pygame.mixer.music.stop()

    def resume_music(self):
        """Возобновить музыку (если была остановлена)."""
        if self.music_path and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def set_volume(self, volume):
        """Установить громкость (0.0 – 1.0)."""
        if self.music_path:
            pygame.mixer.music.set_volume(volume)