import pilas
import random
import os
import sys
sys.path.insert(0, "..")

Bomba = pilas.actores.Bomba

class BombaConMovimiento(Bomba):

    def __init__(self, x=0, y=0):
        Bomba.__init__(self, x, y)

        cx = random.randrange(-320, 320)
        cy = random.randrange(-240, 240)

        self.x = cx
        if self.x < 50 and self.x > -50:
            self.x = cx * 5

        self.y = cy
        if self.y < 50 and self.y > -50:
            self.y = cy * 5

        self.difx=0
        self.dify=0

    def actualizar(self):
        if self.x > 320:
            self.difx=1 
        if self.x < -320:
            self.difx=0

        if self.y > 240:
            self.dify=1
        if self.y < -240:
            self.dify=0

        if self.difx == 0:
            self.x += 1
        else:
            self.x -= 1

        if self.dify == 0:
            self.y += 1
        else:
            self.y -= 1

class BombaConOtroMovimiento(Bomba):

    def __init__(self, x=0, y=0):
        Bomba.__init__(self, x, y)

        cx = random.randrange(-320, 320)
        cy = random.randrange(-240, 240)

        self.x = cx
        if self.x < 50 and self.x > -50:
            self.x = cx * 5

        self.y = cy
        if self.y < 50 and self.y > -50:
            self.y = cy * 5

    def actualizar(self):
        self.x += 1.8
        self.y += 1.8

        if self.x > 320:
            self.x = -320

        if self.y > 240:
            self.y = -240

class MiObjetivo(Bomba):

    def __init__(self, x=0, y=0):
        Bomba.__init__(self, x, y)
        self.radio_de_colision = 20
        self.image_normal = pilas.imagenes.cargar('esquivar_bombas/patito.png')
        self.definir_imagen(self.image_normal)

        cx = random.randrange(-320, 320)
        cy = random.randrange(-240, 240)

        self.x = cx
        if self.x < 50 and self.x > -50:
            self.x = cx * 5

        self.y = cy
        if self.y < 50 and self.y > -50:
            self.y = cy * 5

        self.difx=0
        self.dify=0

    def actualizar(self):

        if self.x > 320:
            self.difx=1 
        if self.x < -320:
            self.difx=0

        if self.y > 240:
            self.dify=1
        if self.y < -240:
            self.dify=0

        if self.difx == 0:
            self.x += 3
        else:
            self.x -= 3

        if self.dify == 0:
            self.y += 3
        else:
            self.y -= 3

class MiProtagonista(pilas.actores.Zanahoria):
    
    def __init__(self, x=0, y=0):
        pilas.actores.Zanahoria.__init__(self, x=x, y=y)
        self.radio_de_colision = 37
        self.vidas = 3
        self.image_normal = pilas.imagenes.cargar('esquivar_bombas/player.png')
        self.image_accion = pilas.imagenes.cargar('esquivar_bombas/perder.png')
        self.image_perdio = pilas.imagenes.cargar('esquivar_bombas/perdio.png')
        self.image_gano = pilas.imagenes.cargar('esquivar_bombas/gano.png')
        self.definir_imagen(self.image_normal)
        # Aprende
        self.aprender(pilas.habilidades.SeguirAlMouse)
        # self.aprender(pilas.habilidades.SeMantieneEnPantalla, permitir_salida=True)

    def perder_vida(self):
        self.vidas = self.vidas - 1

    def accion(self):
        self.definir_imagen(self.image_accion)                      # Cambia la imagen
        pilas.mundo.agregar_tarea_una_vez(0.55 , self.volverNormal) # por 0.55 seg

    def volverNormal(self):
        self.definir_imagen(self.image_normal)

    def perder(self, mensaje):
        self.vidas = 3
        pilas.actores.Actor.decir(self, mensaje)
        self.definir_imagen(self.image_perdio)
        pilas.avisar("Para regresar al menu presione la tecla 'Esc'")
        mensaje = pilas.actores.Texto("Perdiste!!!")
        pilas.escena_actual().tareas.eliminar_todas()

    def win(self, mensaje):
        pilas.actores.Actor.decir(self, mensaje)
        self.definir_imagen(self.image_gano)
        pilas.avisar("Para regresar al menu presione la tecla 'Esc'")
        mensaje = pilas.actores.Texto("Ganaste!!!")
        pilas.escena_actual().tareas.eliminar_todas()

pilas.iniciar(gravedad=(0,0))
musica = pilas.musica.cargar("esquivar_bombas/cancion.mp3")
musica.reproducir()

########################################################### Escena Menu #################################################################
class EscenaDeMenu(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        fondo= pilas.fondos.DesplazamientoHorizontal()
        fondo.agregar("esquivar_bombas/fondoMenu.jpg", velocidad=0)

        opciones = [
		    ('Pablito Games', self.juego1),
		    ('Pitbull Games', self.juego2),
            ('Salir', self.salir)]

        self.menu = pilas.actores.Menu(opciones)
        pilas.actores.Sonido()

    def juego1(self):
        pilas.cambiar_escena(EscenaDeJuego())

    def juego2(self):
        pilas.cambiar_escena(EscenaDeJuego2())

    def salir(self):
        exit()
########################################################## JUEGO 1 #####################################################################
class EscenaDeJuego(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        protagonista = MiProtagonista()
        objetivo = MiObjetivo()

        pilas.mundo.motor.ocultar_puntero_del_mouse()

        # Creacion de las bombas
        bomba = BombaConMovimiento()
        bomba2 = BombaConOtroMovimiento()
        bombas = (bomba * 11 + bomba2 * 11)

        def pasar_por_bomba(protagonista, bomba):
            protagonista.perder_vida()
            bomba.explotar()
            puntos.escala = 0
            puntos.escala = pilas.interpolar(1, duracion=0.5, tipo='rebote_final')
            puntos.aumentar(-1) # Disminuye el contador de puntos
            if (protagonista.vidas == 0):
                for bomba in bombas:
                    bomba.eliminar()
                protagonista.perder("Game Over") # Perdio las 3 vidas
                objetivo.eliminar()
            else:
                protagonista.accion() # Cuando tenga alguna de las 3 vidas
                bombas.append(BombaConMovimiento())
                bombas.append(BombaConOtroMovimiento())

        def pasar_por_objetivo(protagonista, objetivo):
            for bomba in bombas:
                bomba.eliminar()
            objetivo.explotar()
            protagonista.win(":D")

        pilas.escena_actual().colisiones.agregar(protagonista, bombas, pasar_por_bomba)
        pilas.escena_actual().colisiones.agregar(protagonista, objetivo, pasar_por_objetivo)

        puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.azul)
        puntos.magnitud = 40
        puntos.aumentar(3) # Empieza en 3 el contador

        fondo= pilas.fondos.DesplazamientoHorizontal()
        fondo.agregar("esquivar_bombas/fondo.jpg", velocidad=0)

        def crear_bomba():
            bombita = BombaConMovimiento()
            bombas.append(bombita)
            pilas.mundo.agregar_tarea(3.3, crear_bomba)

        pilas.mundo.agregar_tarea(3.3, crear_bomba) # Cada 3 segundos nueva bomba

        pilas.eventos.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla)

    def cuando_pulsa_tecla(self, evento):
        pilas.cambiar_escena(EscenaDeMenu())
########################################################### JUEGO 2 ####################################################################
class EscenaDeJuego2(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        mapa = pilas.actores.MapaTiled('pelado/parque.tmx')
        pelado = pilas.actores.personajes_rpg.Maton(mapa)
        pelado.radio_de_colision = 20
        pelado.aprender(pilas.habilidades.SeMantieneEnPantalla, permitir_salida=False)
        pelado.aprender(pilas.habilidades.Disparar)

        self.vidas = 3
        self.TotalBananas = 0
        def perdio_vida():
            self.vidas = self.vidas - 1

        ban = pilas.actores.Banana()
        bananas = (ban * 11)

        bomb= BombaConMovimiento()
        bombas = (bomb * 7)

        def pasar_por_banana(mono, banana):
            banana.eliminar()
            self.TotalBananas = self.TotalBananas + 1
            if (self.TotalBananas == 5):
                self.TotalBananas = 0
                self.vidas = self.vidas + 1
                puntos.escala = 0
                puntos.escala = pilas.interpolar(1, duracion=1.5, tipo='rebote_final')
                puntos.aumentar(1) # Aumenta una vida en el contador de puntos

        def pasar_por_bomba(mono, bomba):
            perdio_vida()
            bomba.explotar()
            puntos.escala = 0
            puntos.escala = pilas.interpolar(1, duracion=0.5, tipo='rebote_final')
            puntos.aumentar(-1) # Disminuye una vida en el contador de puntos
            if (self.vidas == 0):
                for bomba in bombas:
                    bomba.eliminar()
                for banana in bananas:
                    banana.eliminar()
                pilas.escena_actual().tareas.eliminar_todas()
                mensaje = pilas.actores.Texto("Pitbull murio, perdiste...")
                pilas.avisar("Para regresar al menu presione la tecla 'Esc'")

        def eliminar_bomba():
            bomba.eliminar()

        pilas.escena_actual().colisiones.agregar(pelado, bananas, pasar_por_banana)
        pilas.escena_actual().colisiones.agregar(pelado, bombas, pasar_por_bomba)
        # pilas.escena_actual().colisiones.agregar(balas, bombas, eliminar_bomba)

        puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.rojo)
        puntos.magnitud = 35
        puntos.aumentar(3)
        pilas.avisar("Para aumentar vidas debes juntar bananas")

        def crear_banana():
            bananita = pilas.actores.Banana(x = random.randrange(-320, 320), y = random.randrange(-240, 240))
            bananas.append(bananita)
            pilas.mundo.agregar_tarea(3.5, crear_banana)
            # print "se creo banana"

        def crear_bomba():
            bombita = BombaConMovimiento()
            bombas.append(bombita)
            pilas.mundo.agregar_tarea(3.4, crear_bomba)

        pilas.mundo.agregar_tarea(3.4, crear_bomba)
        pilas.mundo.agregar_tarea(3.5, crear_banana)
        pilas.eventos.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla)

    def cuando_pulsa_tecla(self, evento):
        pilas.cambiar_escena(EscenaDeMenu())

# Carga la primera Escena
pilas.cambiar_escena(EscenaDeMenu())
pilas.ejecutar()
