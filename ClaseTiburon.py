import pygame
from define import *



class Tiburon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(RUTA_BASE.format("imagenes\\tiburon.png"))
        self.image = pygame.transform.scale(self.image, (170, 100))
        self.imgen_flipped = pygame.transform.flip(self.image, True, False) # INVIERTE IMAGEN DEL TIBURON
        self.rect = self.image.get_rect()
        self.rect.topleft = (150, ALTO_VENTANA // 2 - 50)
        self.velocidad = 1.5 # VELOCIDAD DEL TIBURON
        self.boca_rect = pygame.Rect(self.rect.left + 100, self.rect.centery - 25, 50, 50) # BOCA
        self.nombre = "nombre"
        self.puntos = 0
        self.vidas = 5
        self.tiempo = 0
        self.nivel = 1
        self.dificultad = 1

    def move_up(self):
        if self.rect.top > 0 + ALTURA_ENCABEZADO - 20:
            self.rect.move_ip(0, -5 * self.velocidad)

    def move_down(self):
        if self.rect.bottom < ALTO_VENTANA:
            self.rect.move_ip(0, 5 * self.velocidad)

    def move_left(self):
        if self.rect.left > 0:
            self.rect.move_ip(-5 * self.velocidad, 0)
            self.boca_rect.x = self.rect.left + 10

    def move_right(self):
        if self.rect.right < ANCHO_VENTANA - 10:
            self.rect.move_ip(5 * self.velocidad, 0)
            self.boca_rect.x = self.rect.left + 100

    def update_boca(self):
        self.boca_rect.y = self.rect.centery - 25
    
    def colision_pez_amarillo(self, x, y):
        self.colision = pygame.mixer.Sound(RUTA_BASE.format("Sonidos\\pez_amarillo.mp3"))
        self.colision_imagen = pygame.image.load(RUTA_BASE.format("\imagenes\\mas10.png"))
        self.colision_imagen = pygame.transform.scale(self.colision_pez_amarillo_imagen, (40, 40))
        self.tiempo_inicio_colision_pez_amarillo = 0
        return(self.colision_magen, (x, y))

    def colision_pez_rojo(self, x, y):
        self.colision_pez_rojo = pygame.mixer.Sound(RUTA_BASE.format("Sonidos\\pez_rojo.mp3"))
        self.colision_imagen = pygame.image.load(RUTA_BASE.format("imagenes\\pow.png"))
        self.colision_imagen = pygame.transform.scale(self.colision_pez_rojo_imagen, (40, 40))
        self.tiempo_inicio_colision_pez_rojo = 0
        return(self.colision_imagen, (x, y))
        

