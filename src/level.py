# level.py
import pygame

def create_level():
    platforms = []
    
    # Земля
    platforms.append(pygame.Rect(0, 500, 800, 50))
    
    # Горизонтальные платформы (для прыжков)
    platforms.append(pygame.Rect(200, 400, 100, 20))
    platforms.append(pygame.Rect(400, 300, 100, 20))
    platforms.append(pygame.Rect(600, 200, 100, 20))
    
    # === СТЕНЫ для паркур-механик ===
    # Левая стена (высокая, узкая)
    platforms.append(pygame.Rect(100, 200, 20, 300))  # x=100, y=200, ширина=20, высота=300
    
    # Правая стена
    platforms.append(pygame.Rect(700, 150, 20, 350))  # x=700, y=150, ширина=20, высота=350
    
    # Дополнительно: "ящик" или уступ у стены для теста wall jump
    platforms.append(pygame.Rect(120, 350, 60, 20))   # рядом с левой стеной
    platforms.append(pygame.Rect(620, 250, 60, 20))   # рядом с правой стеной

    return platforms