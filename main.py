import pygame
from pygame import mixer
import random
import math

# Inicializar pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo,  icono y fondo de pantalla
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.jpg")

# Agregar musica de fondo, el -1 es para que se repita cada vez que termina
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Variables de la nave protagonista del juego
img_jugador = pygame.image.load("cohete.png")
# Posicion inicial de la nave en el eje x
jugador_x = 368
# Posicion iicial de la nave en el eje y
jugador_y = 500
# Variable para usar en los movimientos
jugador_x_cambio = 0


# Listas para cargar las variables del enemigo
img_enemigo = []
# Posicion de la nave en el eje x
enemigo_x = []
# Posicion de la nave en el eje y
enemigo_y = []
# Variable para usar en los movimientos
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_de_enemigos = 8

# Cargando las variables del enemigo
for e in range (cantidad_de_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    # Posicion de la nave en el eje x
    enemigo_x.append(random.randint(0, 736))
    # Posicion de la nave en el eje y
    enemigo_y.append(random.randint(50, 200))
    # Variable para usar en los movimientos
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variables de la bala
img_bala = pygame.image.load("bala.png")
# Posicion de la bala en el eje x
bala_x = 0
# Posicion de la bala en el eje y
bala_y = 500
# Variable para usar en los movimientos
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# Variable para puntaje
puntaje = 0
# Elegimos fuente para puntaje: nombre y tamano de la fuente
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# Texto de final de juego
fuente_final = pygame.font.Font("freesansbold.ttf", 90)

# Funcion de texto de fin de juego
def texto_final():
    mi_fuente_final = fuente_final.render("Fin del juego!!!", True,  (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    # Con las fuentes no se usa blit, se debe crear una variable que sera la que se tirara a la pantalla. El True es un antialias, que no explico que es
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    # Ahora si podemos arrojar el texto a la pantalla
    pantalla.blit(texto, (x, y))


#funcion que arroja la nave a la pantalla, debe llamarse en el loop del juego antes del update y despues de que se pinte la pantalla
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#funcion que arroja el enemigo  a la pantalla
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

#  Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False

# Loop que mantiene el juego en ejecucion
se_ejecuta = True
while se_ejecuta:

    # Color lila al fondo de la pantalla RGB
    # pantalla.fill((205, 144, 228))

    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iteracion de eventos
    for evento in pygame.event.get():
        # Pregunta si se pulso la cruz de cierre de la ventana
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Pregunta si se pulso una tecla
        if evento.type == pygame.KEYDOWN:
            # Pregunta si se presiono la flecha izquierda
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            # Pregunta si se presiono la flecha izquierda
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Pregunta si se solto la tecla
        if evento.type == pygame.KEYUP:
            # Pregunta si se solto una flecha
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar la posicion de la nave ppal
    jugador_x += jugador_x_cambio

    # Mantener a la nave ppal dentro de la pantalla
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736


# Modificar la ubicacion del enemigo
    for e in range(cantidad_de_enemigos):
        # Fin del juego
        if enemigo_y[e] >= 436:
            for k in range(cantidad_de_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]
    # Mantener al enemigo dentro de la pantalla
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]

        # Llamar a la funcion colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("golpe.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            # Posicion de la nave en el eje x
            enemigo_x[e] = random.randint(0, 736)
            # Posicion de la nave en el eje y
            enemigo_y[e] = random.randint(50, 200)
        # Llamar a funcion enemigo
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento de la bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio



    # llamada a funcion que hace visible a la nave protagonista
    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    # Actualizar
    pygame.display.update()