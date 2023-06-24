import pygame
import sys
import random
import sqlite3
import time
from  ClaseTiburon import Tiburon
from define import *

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("UNDER THE SEA")

# MUSICA
pygame.mixer.music.load(RUTA_BASE.format("Sonidos\\under.mp3"))  ## Cargar canción
pygame.mixer.music.set_volume(0.0) # Ajustar volumen (EMTRE 0.0 A 1.0)


fondo = pygame.image.load(RUTA_BASE.format("imagenes\\fondo.PNG"))
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))


tiempo_colision = 3000

algoritmo_dificultad = 1.8 # (0.01 a 5) incremento dificultades


pez_amarillo_img = pygame.image.load(RUTA_BASE.format("imagenes\\pez_amarillo.png"))
pez_amarillo_img = pygame.transform.scale(pez_amarillo_img, (40, 40))
collision_pez_amarillo = pygame.mixer.Sound(RUTA_BASE.format("Sonidos\\pez_amarillo.mp3"))
collision_pez_amarillo_imagen = pygame.image.load(RUTA_BASE.format("imagenes\\mas10.png"))
collision_pez_amarillo_imagen = pygame.transform.scale(collision_pez_amarillo_imagen, (40, 40))
tiempo_inicio_colision_pez_amarillo = 0


pez_rojo_img = pygame.image.load(RUTA_BASE.format("imagenes\\pez_rojo.png"))
pez_rojo_img = pygame.transform.scale(pez_rojo_img, (40, 40))
collision_pez_rojo = pygame.mixer.Sound(RUTA_BASE.format("Sonidos\\pez_rojo.mp3"))
collision_pez_rojo_imagen = pygame.image.load(RUTA_BASE.format("imagenes\\pow.png"))
collision_pez_rojo_imagen = pygame.transform.scale(collision_pez_rojo_imagen, (40, 40))
tiempo_inicio_colision_pez_rojo = 0


def agregar_puntaje(nombre_elegido, puntos, vidas, tiempo):
    with sqlite3.connect(RUTA_BASE.format("puntajes.db")) as conexion:
        sentencia = "INSERT INTO puntajes (nombre, puntos, vidas, tiempo) VALUES (?, ?, ?, ?)"
        conexion.execute(sentencia, (nombre_elegido, puntos, vidas, tiempo))
        conexion.commit()  # Guardar los cambios en la base de datos

# Crear tabla SQLite si no existe
with sqlite3.connect(RUTA_BASE.format("puntajes.db")) as conexion:
    try:
        sentencia = '''CREATE TABLE IF NOT EXISTS puntajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            puntos INTEGER,
            vidas INTEGER,
            tiempo INTEGER
        )'''
        conexion.execute(sentencia)
        print("Se creó la tabla puntajes")
    except sqlite3.OperationalError:
        print("La tabla puntajes ya existe")

    # Verificar si la tabla está vacía
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM puntajes")
    resultado = cursor.fetchone()
    registros_existentes = resultado[0]

    if registros_existentes == 0:
        # Agregar los registros solo si la tabla está vacía
        agregar_puntaje("DAVIDF", 200, 2, 180)
        agregar_puntaje("MARINAC", 300, 2, 180)
        agregar_puntaje("RENATON", 150, 1, 180)
        agregar_puntaje("MATIASQ", 150, 2, 180)


# mostrar mejores 8 puntajes de la tabla puntajes
def mostrar_mejores_puntajes(nombre_elegido=""):
    with sqlite3.connect(RUTA_BASE.format("puntajes.db")) as conexion:
        sentencia = "SELECT nombre, puntos, vidas, tiempo FROM puntajes ORDER BY puntos DESC LIMIT 8"
        resultados = conexion.execute(sentencia).fetchall()

    print(resultados)

    # Mostrar los resultados en la ventana
    font = pygame.font.Font("couriernew.ttf", 30)
    #font.set_bold(True)  # Aplicar negrita a la fuente
    titulo = font.render("Mejores puntajes", True, COLOR_NEGRO)
    cabecera = font.render("Nombre          Puntos     Vidas", True, COLOR_NEGRO)

    # Variables para mostrar los puntajes
    puntajes_renderizados = []

    for i, resultado in enumerate(resultados):
        nombre = resultado[0]
        puntos = resultado[1]
        vidas = resultado[2]

        # Ajustar el nombre si es muy largo o vacío
        if len(nombre) > 15:
            nombre = nombre[:12] + "..."
        elif len(nombre) == 0:
            nombre = "N/A"

        # Renderizar los puntajes con formato
        posicion = font.render(f"{nombre:<15} {puntos:<10} {vidas}", True, COLOR_NEGRO)
        puntajes_renderizados.append(posicion)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return menu_principal()  # Regresar al menú principal al presionar la tecla Enter

        window.blit(fondo, (0, 0))
        window.blit(titulo, (100, 50))
        window.blit(cabecera, (100, 100))

        # Mostrar los puntajes en columnas
        posicion_y = 140
        for puntaje in puntajes_renderizados:
            window.blit(puntaje, (120, posicion_y))
            posicion_y += 40

        pygame.display.flip()


def pedir_nombre(nombre, puntos, vidas, tiempo):
    logo = pygame.image.load(RUTA_BASE.format("imagenes\\logo.PNG"))
    logo = pygame.transform.scale(logo, (600, 400))
    font = pygame.font.SysFont("Arial", 40)
    titulo = font.render("Juego Terminado", True, COLOR_NEGRO)
    eleccion = font.render("Elige tu nombre: {}".format(nombre), True, COLOR_ROJO)
    opcion_1 = font.render("Tus Puntos: {}".format(puntos), True, COLOR_NEGRO)
    opcion_2 = font.render("Tus vidas: {}".format(vidas), True, COLOR_NEGRO)
    opcion_3 = font.render("Enter para Guardar", True, COLOR_NEGRO)

    input_active = True  # Variable para indicar si el campo de entrada está activo
    input_text = ""  # Variable para almacenar el texto ingresado por el usuario

    while True:
        window.blit(fondo, (0, 0))
        window.blit(logo, (ANCHO_VENTANA / 3, 0))
        window.blit(titulo, (100, ALTO_VENTANA // 2 - 50))
        window.blit(eleccion, (100, ALTO_VENTANA // 2 - 0))
        window.blit(opcion_1, (120, ALTO_VENTANA // 2 + 50))
        window.blit(opcion_2, (120, ALTO_VENTANA // 2 + 100))
        window.blit(opcion_3, (120, ALTO_VENTANA // 2 + 150))
  
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        # Guardar el nombre ingresado y salir del bucle
                        nombre = input_text
                        return nombre
                    elif event.key == pygame.K_BACKSPACE:
                        # Eliminar el último carácter ingresado
                        input_text = input_text[:-1]
                    else:
                        # Agregar el carácter ingresado al texto
                        input_text += event.unicode

                eleccion = font.render("Elige tu nombre: {}".format(input_text), True, COLOR_ROJO)





tiburon = Tiburon()

# CREA LISTAS DE PECES 

peces_amarillos = []
peces_rojos = []

for pez in range(6):
    pez_amarillo_x = random.choice([-40, ANCHO_VENTANA])
    pez_amarillo_y = random.randint(ALTURA_ENCABEZADO, ALTO_VENTANA - ALTURA_ENCABEZADO)
    
    direccion_amarillo = None
    if pez_amarillo_x == -40:
        direccion_amarillo = 1
    else:
        direccion_amarillo = -1
    velocidad_amarillo = random.randint(1, 3) * direccion_amarillo        
    pez_amarillo_rect = pez_amarillo_img.get_rect()
    pez_amarillo_rect.topleft = (pez_amarillo_x, pez_amarillo_y)
    mostrar_colision_pez_amarillo = False
    peces_amarillos.append([pez_amarillo_rect, velocidad_amarillo, direccion_amarillo,mostrar_colision_pez_amarillo])


for pez in range(5):
    pez_rojo_x = random.choice([-40, ANCHO_VENTANA])
    pez_rojo_y = random.randint(ALTURA_ENCABEZADO, ALTO_VENTANA - ALTURA_ENCABEZADO)
    direccion_rojo = None
    if pez_rojo_x == -40:
        direccion_rojo = 1
    else:
        direccion_rojo = -1
    velocidad_rojo = random.randint(1, 3) * 1.2 * direccion_rojo
    pez_rojo_rect = pez_rojo_img.get_rect()
    pez_rojo_rect.topleft = (pez_rojo_x, pez_rojo_y)
    mostrar_colision_pez_rojo = False
    peces_rojos.append([pez_rojo_rect, velocidad_rojo, direccion_rojo,mostrar_colision_pez_rojo])



pygame.mixer.music.play(-1)

def subir_nivel():
    if tiburon.tiempo < 20:
        tiburon.nivel = 1
    elif tiburon.tiempo > 20 and tiburon.tiempo < 40:
        tiburon.nivel = 2
    elif tiburon.tiempo > 40 and tiburon.tiempo < 60:
        tiburon.nivel = 3
    elif tiburon.tiempo > 60:
        tiburon.nivel = 4



def comenzar():
    tiempo_inicial = pygame.time.get_ticks()
    tiburon.tiempo = (pygame.time.get_ticks() - tiempo_inicial) / 1000
    tiburon.puntos = 0
    tiburon.vidas = 5
    tiburon.nivel = 1
    posicion_tiburon = 1 # BANDERA PARA ESTABLECER POSICION DE LA BOCA
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(FPS)
        window.blit(fondo, (0, 0))

        # VERIFICA LA TECLA PRESIONADA    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            tiburon.move_up()
        if keys[pygame.K_DOWN]:
            tiburon.move_down()
        if keys[pygame.K_LEFT]:
            tiburon.move_left()
            posicion_tiburon = 0
        if keys[pygame.K_RIGHT]:
            tiburon.move_right()
            posicion_tiburon = 1
        if keys[pygame.K_ESCAPE ]:
            menu_principal()



        if posicion_tiburon:
            window.blit(tiburon.image, tiburon.rect.topleft)
        else:
            window.blit(tiburon.imgen_flipped, tiburon.rect.topleft)

        tiburon.update_boca() # ACTUALIZA RECTANGULO BOCA

        subir_nivel()

        # ACTUALIZA PEZ AMARILLO
        for pez_amarillo in peces_amarillos:
            pez_amarillo_rect, velocidad_amarillo, direccion_amarillo, colision = pez_amarillo
            pez_amarillo_rect.move_ip(abs(velocidad_amarillo) * direccion_amarillo , 0)

            if pez_amarillo_rect.right <= -40 or pez_amarillo_rect.left >= ANCHO_VENTANA:
                pez_amarillo_rect.topleft = (random.randint(-200, -50) if direccion_amarillo == 1 else random.randint(ANCHO_VENTANA, ANCHO_VENTANA + 200),
                                            random.randint(ALTURA_ENCABEZADO, ALTO_VENTANA - 50))
                
                direccion_amarillo = random.choice([-1, 1])
                velocidad_amarillo = random.choice([1, 3]) + tiburon.dificultad * tiburon.nivel * algoritmo_dificultad

            if direccion_amarillo == 1:
                pez_amarillo_img_flipped = pygame.transform.flip(pez_amarillo_img, True, False)
                window.blit(pez_amarillo_img_flipped, pez_amarillo_rect.topleft)
            else:
                window.blit(pez_amarillo_img, pez_amarillo_rect.topleft)
            

        # Colisión con pez amarillo
            if tiburon.boca_rect.colliderect(pez_amarillo_rect):
                window.blit(collision_pez_amarillo_imagen, pez_amarillo_rect.topleft)
                tiburon.puntos += 10
                pez_amarillo[3] = True
                mostrar_colision_pez_amarillo = True
    
                tiburon.tiempo_inicio_colision_pez_amarillo = pygame.time.get_ticks()
                tiempo_actual = pygame.time.get_ticks()
                
                if tiempo_actual - tiburon.tiempo_inicio_colision_pez_amarillo < tiempo_colision:
                    
                    mostrar_colision_pez_amarillo = False
                else:
                    window.blit(collision_pez_amarillo_imagen, pez_amarillo_rect.topleft)

                collision_pez_amarillo.play() # SONIDO COLISION

                direccion_amarillo = random.choice([-1, 1])
                velocidad_amarillo = random.randint(1, 3) * direccion_amarillo 
                pez_amarillo_rect.topleft = (random.randint(-200, -50) if direccion_amarillo == 1 else random.randint(ANCHO_VENTANA, ANCHO_VENTANA + 200),
                                            random.randint(ALTURA_ENCABEZADO, ALTO_VENTANA - 50)) # genera posiciones aleatorias para el pez amarillo en los ejes x, y
                
            pez_amarillo[1] = velocidad_amarillo
            pez_amarillo[2] = direccion_amarillo

        # ACTUALIZA PEZ ROJO
        for pez_rojo in peces_rojos:
            pez_rojo_rect, velocidad_rojo, direccion_rojo, mostrar_colision_pez_rojo = pez_rojo
            pez_rojo_rect.move_ip(velocidad_rojo * direccion_rojo, 0)

            if pez_rojo_rect.right < 0 or pez_rojo_rect.left > ANCHO_VENTANA:
                pez_rojo_rect.topleft = (random.randint(-200, -50) if direccion_rojo == 1 else random.randint(ANCHO_VENTANA, ANCHO_VENTANA + 200),
                                        random.randint(ALTURA_ENCABEZADO, ALTO_VENTANA - 50))
                velocidad_rojo = random.randint(1, 3) * 1.2 + tiburon.dificultad * tiburon.nivel * algoritmo_dificultad
                direccion_rojo = random.choice([-1, 1])
                
            if direccion_rojo == 1:
                pez_rojo_img_flipped = pygame.transform.flip(pez_rojo_img, True, False)
                window.blit(pez_rojo_img_flipped, pez_rojo_rect.topleft)
            else:
                window.blit(pez_rojo_img, pez_rojo_rect.topleft)
    

        # Colisión con pez rojo
            if tiburon.boca_rect.colliderect(pez_rojo_rect):
                tiburon.vidas -= 1
                pez_rojo[3] = True
                mostrar_colision_pez_rojo = True
                tiempo_inicio_colision_pez_rojo = pygame.time.get_ticks()
                if mostrar_colision_pez_rojo:
                    tiempo_actual_rojo = pygame.time.get_ticks()
                    if tiempo_actual_rojo - tiempo_inicio_colision_pez_rojo > tiempo_colision:
                        mostrar_colision_pez_rojo = False
                    else:
                        pez_rojo[3] = False
                    if mostrar_colision_pez_rojo:
                        window.blit(collision_pez_rojo_imagen, (pez_rojo_x, pez_rojo_y))
                
                collision_pez_rojo.play()
                
                pez_rojo_rect.topleft = (random.randint(-200, -50) if direccion_rojo == 1 else random.randint(ANCHO_VENTANA, ANCHO_VENTANA + 200),
                                        random.randint(ALTURA_ENCABEZADO, ALTO_VENTANA - 50))
                direccion_rojo = random.choice([-1, 1])
                velocidad_rojo = random.randint(1, 3) * direccion_rojo  * 1.2 + tiburon.dificultad * tiburon.nivel * algoritmo_dificultad
                    

            pez_rojo[1] = velocidad_rojo
            pez_rojo[2] = direccion_rojo


       # Almacenar valores
        if tiburon.tiempo == 80 or tiburon.vidas == 0:
            tu_puntaje = tiburon.puntos
            tu_tiempo = tiburon.tiempo
            tu_vidas = tiburon.vidas
            Tu_nombre = "ANONIMO"



            

            return Tu_nombre, tu_puntaje, tu_vidas, tu_tiempo
        
        
        # PARA VER RECTANGUNLOS
        #pygame.draw.rect(window, COLOR_NEGRO, tiburon.boca_rect)   # BOCA TIBURON
        #pygame.draw.rect(window, (255, 0, 0), tiburon.rect, 2)   # TIBURON
        

        # Mostrar texto en la parte superior de la pantalla
        font = pygame.font.Font(None, 36)
        puntos_texto = font.render("Puntos: " + str(tiburon.puntos), True, COLOR_NEGRO)
        nivel_texto = font.render("Nivel: " + str(tiburon.nivel), True, COLOR_NEGRO)
        tiburon.tiempo = (pygame.time.get_ticks() - tiempo_inicial) // 1000
        tiempo_texto = font.render("Tiempo: " + str(tiburon.tiempo), True, COLOR_NEGRO) # // para division entera de los segundos
        vidas_texto = font.render("Vidas: " + str(tiburon.vidas), True, COLOR_NEGRO)

        window.blit(puntos_texto, (20, 20))
        window.blit(nivel_texto, ((ANCHO_VENTANA // 3 - nivel_texto.get_width()  // 3, 20)))
        window.blit(tiempo_texto, (ANCHO_VENTANA * 2 // 3 - tiempo_texto.get_width() * 2 // 3, 20))
        window.blit(vidas_texto, (ANCHO_VENTANA - vidas_texto.get_width() - 20, 20))
    

        pygame.display.flip()

# Menú de opciones
def mostrar_menu():
    logo = pygame.image.load(RUTA_BASE.format("imagenes\\logo.PNG"))
    logo = pygame.transform.scale(logo, (600, 400))
    font = pygame.font.SysFont("Arial", 40)
    titulo = font.render("Debajo del mar", True, COLOR_NEGRO)
    opcion_1 = font.render("1. Comenzar", True, COLOR_NEGRO)
    opcion_2 = font.render("2. Ver mejores puntajes", True, COLOR_NEGRO)
    opcion_3 = font.render("3. Dificultad", True, COLOR_NEGRO)
    opcion_4 = font.render("4. Salir", True, COLOR_NEGRO)

    while True:
        window.blit(fondo, (0, 0))
        window.blit(logo, (ANCHO_VENTANA / 3, 0))
        window.blit(titulo, (100, ALTO_VENTANA // 2 - 50))
        window.blit(opcion_1, (120 , ALTO_VENTANA // 2 - 0))
        window.blit(opcion_2, (120, ALTO_VENTANA // 2 + 50))
        window.blit(opcion_3, (120, ALTO_VENTANA // 2 + 100))
        window.blit(opcion_4, (120, ALTO_VENTANA // 2 + 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                    return 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    return 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                    return 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                    return 4



# Elegir dificultad
def elegir_dificultad():
    logo = pygame.image.load(RUTA_BASE.format("imagenes\\logo.PNG"))
    logo = pygame.transform.scale(logo, (600, 400))
    font = pygame.font.SysFont("Arial", 40)
    titulo = font.render("Elegir Dificultad", True, COLOR_NEGRO)
    eleccion = font.render("Dificultad: {}".format(tiburon.dificultad), True, COLOR_ROJO)
    opcion_1 = font.render("1. Normal", True, COLOR_NEGRO)
    opcion_2 = font.render("2. Experto", True, COLOR_NEGRO)
    opcion_3 = font.render("3. Avanzado", True, COLOR_NEGRO)
    opcion_4 = font.render("4. Volver al menú principal", True, COLOR_NEGRO)

    while True:
        window.blit(fondo, (0, 0))
        window.blit(logo, (ANCHO_VENTANA / 3, 0))
        window.blit(titulo, (100, ALTO_VENTANA // 2 - 50))
        window.blit(eleccion, (100, ALTO_VENTANA // 2 - 0))
        window.blit(opcion_1, (120, ALTO_VENTANA // 2 + 50))
        window.blit(opcion_2, (120, ALTO_VENTANA // 2 + 100))
        window.blit(opcion_3, (120, ALTO_VENTANA // 2 + 150))
        window.blit(opcion_4, (120, ALTO_VENTANA // 2 + 200))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                    tiburon.dificultad = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    tiburon.dificultad  = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                    tiburon.dificultad  = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                    return 4

                eleccion = font.render("Dificultad: {}".format(tiburon.dificultad), True, COLOR_ROJO)



def menu_principal():
    opcion_menu = 0
    mostrar_menu_principal = True
    mostrar_menu_dificultad = False

    while mostrar_menu_principal:
        opcion_menu = mostrar_menu()
        

        if opcion_menu == 1:
            nombre, puntos, vidas, tiempo = comenzar()
            mostrar_menu_principal = False
            nombre_elegido = pedir_nombre(nombre, puntos, vidas, tiempo)
            opcion_menu = agregar_puntaje(nombre_elegido, puntos, vidas, int(tiempo))
            mostrar_mejores_puntajes(nombre_elegido)
            
        elif opcion_menu == 2:
            mostrar_menu_principal = False
            mostrar_mejores_puntajes()
        elif opcion_menu == 3:
            mostrar_menu_dificultad = True
            while mostrar_menu_dificultad:
                dificultad = elegir_dificultad()
                mostrar_menu_dificultad = False
        elif opcion_menu == 4:
            pygame.mixer.music.stop()
            mostrar_menu_principal = False
            mostrar_menu_dificultad = False
            pygame.quit()
            sys.exit()

menu_principal()
