
import pygame

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
ALTURA_ENCABEZADO = 100

FPS = 90
RUTA_BASE = ".vscode\\PYGAME\\JUEGO\\{0}"

window = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))


fondo = pygame.image.load(RUTA_BASE.format("imagenes\\fondo.PNG"))
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))



COLOR_NEGRO = (0, 0, 0)
COLOR_BLANCO = (255, 255, 255)
COLOR_VERDE = (0, 255, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_GRIS = (128, 128, 128)
COLOR_AMARILLO = (255, 255, 0)
COLOR_CELESTE = (0, 0, 128)
COLOR_AZUL = (0, 0, 255)
COLOR_PERSONAL_1 = (75, 50, 50)