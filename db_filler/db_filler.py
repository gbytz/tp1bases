#!/usr/local/bin/python

from datetime import date
from random import choice, randint

from detective import *


class TipoCaso:
    Pendiente = 0
    Congelado = 1
    Descartado = 2
    Resuelto = 3

class TipoRol:
    Sospechoso = 0
    Fiscal = 1
    Principal = 2
    Auxiliar = 3
    Juez = 4
    Perito = 5 
    Custodio = 6
    Testigo = 7

ID_DICT = {}

def get_current_id(entidad):
    return ID_DICT[entidad]

def get_new_id(entidad):
    if entidad in ID_DICT:
        ID_DICT[entidad] = ID_DICT[entidad] + 1
    else:
        ID_DICT[entidad] = 0
    return ID_DICT[entidad]

def vaciar_base():
    ''' Vacia la base de datos  '''
    # Persona.delete().execute()
    # Direccion.delete().execute()
    # Rol.delete().execute()
    # Categoria.delete().execute()
    # Rango.delete().execute()
    # Servicio.delete().execute()
    # Departamento.delete().execute()
    # Oficial.delete().execute()
    Culpable.delete().execute()
    Congelado.delete().execute()
    Descartado.delete().execute()
    Resuelto.delete().execute()
    Evento.delete().execute()
    Custodia.delete().execute()
    Testimonio.delete().execute()
    Evidencia.delete().execute()
    Involucra.delete().execute()
    Caso.delete().execute()

def crear_categorias():
    ''' Rellena la tabla "Categoria" a partir de una lista de delitos guardada en delitos.txt '''
    print "Creando Categorias"
    f_delitos = open("delitos.txt", "r")

    # Usar este for es medio ineficiente pero por ahora va
    for index, line in enumerate(f_delitos.readlines()):
        striped_line = line.strip()  #  Borros los espacios en blaco adelante y el final de la linea
        try:
            c = Categoria.create(idcategoria=index, descripcion=striped_line)
        except Exception, e:
            print e
        else:
            print "\tCreada categoria: id: {}, descripcion: {}".format(c.idcategoria, c.descripcion)

def crear_roles():
    ''' Rellena la tabla "Rol" a partir de una lista de delitos guardada en delitos.txt '''
    print "Creando Roles"
    f_roles = open("roles.txt", "r")

    # Usar este for es medio ineficiente pero por ahora va
    for index, line in enumerate(f_roles.readlines()):
        striped_line = line.strip()  #  Borros los espacios en blaco adelante y el final de la linea
        try:
            r = Rol.create(idrol=index, descripcion=striped_line)
        except Exception, e:
            print e
        else:
            print "\tCreado rol: id: {}, descripcion: {}".format(r.idrol, r.descripcion)

def crear_direcciones():
    ''' Rellena la tabla "Direccion" eligiendo los atributos de cada persona de manera aleatorea '''
    print "Creando Direcciones"
    f_calles = open("calles.txt", "r")
    calles = f_calles.readlines()

    for index, calle in enumerate(calles):
        calle = calle.strip()
        try:
            d = Direccion.create(
                calle=calle,
                departamento=choice(["A", "B", "C", "D", "E", "F", "G"]),
                localidad="CABA",
                numero=randint(1, 2000),
                piso=randint(1, 12),
                provincia="Buenos Aires",
                iddireccion=index
            )
        except Exception, e:
            print e
        else:
            print "\tCreada direccion: calle:{} numero:{} piso:{} id:{}".format(d.calle, d.numero, d.piso, d.iddireccion)


def crear_personas():
    ''' Rellena la tabla "Persona" eligiendo los atributos de cada persona de manera aleatorea '''
    print "Creando Personas"
    f_nombres = open("nombres.txt", "r")
    nombres = f_nombres.readlines()

    f_apellidos = open("apellidos.txt", "r")
    apellidos = f_apellidos.readlines()

    for index in xrange(20):
        dni = randint(30000000, 50000000)
        nombre = choice(nombres).strip()
        apellido = choice(apellidos).strip()
        iddireccion = choice(Direccion.select()).iddireccion
        tipo = randint(0, 1)
        try:
            p = Persona.create(
                dni=dni,
                nombre=nombre,
                apellido=apellido,
                tipo=tipo,
                fechanacimieto=date(randint(1900, 2016), randint(1, 12), randint(1, 28)),
                iddireccion=iddireccion
            )
        except Exception, e:
            print e
        else:
            print "\tCreada persona: dni: {} nombre: {} apellido: {} tipo: {}".format(p.dni, p.nombre, p.apellido, p.tipo)

def crear_oficiales():
    ''' Crea las entradas necesarias para definir los oficiales '''
    personas_oficiales = Persona.select().where(Persona.tipo==1)
    for persona in personas_oficiales:
        dni = persona.dni
        fechaingreso = date(randint(2000, 2016), randint(1, 8), randint(1, 28))
        numeroescritorio = randint(1, 20)
        numeroplaca = randint(0, 99999)
        iddepto = choice(Departamento.select()).iddepartamento
        idrango = choice(Rango.select()).idrango
        idservicio = choice(Servicio.select()).idservicio
        try:
            oficial = Oficial.create(
                dni=dni,
                fechaingreso=fechaingreso,
                iddepto=iddepto,
                idrango=idrango,
                idservicio=idservicio,
                numeroescritorio=numeroescritorio,
                numeroplaca=numeroplaca,
            )
        except Exception, e:
            print e
        else:
            print "\tCreado oficial: dni:{} nombre:{} apellido:{} placa:{} escritorio:{}".format(oficial.dni.dni, persona.nombre, persona.apellido, oficial.numeroplaca, oficial.numeroescritorio)

def crear_rangos():
    ''' Rellena la tabla "Rango" a partir de una lista de delitos guardada en delitos.txt '''
    print "Creando Rangos"
    f_rangos = open("rangos.txt", "r")

    # Usar este for es medio ineficiente pero por ahora va
    for index, line in enumerate(f_rangos.readlines()):
        striped_line = line.strip()  #  Borros los espacios en blaco adelante y el final de la linea
        try:
            r = Rango.create(idrango=index, nombre=striped_line)
        except Exception, e:
            print e
        else:
            print "\tCreado rango: id: {}, nombre: {}".format(r.idrango, r.nombre)

def crear_servicios():
    ''' Rellena la tabla "Rango" a partir de una lista de delitos guardada en delitos.txt '''
    print "Creando Rangos"
    f_servicios = open("servicios.txt", "r")

    # Usar este for es medio ineficiente pero por ahora va
    for index, line in enumerate(f_servicios.readlines()):
        striped_line = line.strip()  #  Borros los espacios en blaco adelante y el final de la linea
        try:
            s = Servicio.create(idservicio=index, nombre=striped_line)
        except Exception, e:
            print e
        else:
            print "\tCreado servicio: id: {}, nombre: {}".format(s.idservicio, s.nombre)

def crear_departamentos():
    ''' Rellena la tabla "Departamento" '''
    for index in range(1, 10):
        try:
            iddireccion = choice(Direccion.select()).iddireccion
            departamento = Departamento.create(
                iddepartamento=index,
                iddireccion=iddireccion,
                nombre="Departamento #{}".format(index)
            )
        except Exception, e:
            print e
        else:
            print "\tCreado departamento: id: {}, nombre: {}".format(departamento.iddepartamento, departamento.nombre)

def crear_caso_medialunas():
    ''' Crea el terrible caso de robo de medialunas '''
    try:
        caso = Caso.create(
            descripcion="Alguien se robo las medialunas que compramos para comer haciendo el TP de bases",
            fecha=date(2016, 9, 3),
            fechaingreso= date.today(),
            idcaso=get_new_id("caso"),
            idcategoria=76, # Robo de medialunas
            lugar="La juntada de TP",
            tipo=TipoCaso.Pendiente
        )
        # Defino el principal sospechoso
        involucra_sospechoso = Involucra.create(
            dni=33843285,
            idcaso=get_current_id("caso"),
            idrol=0,
        )
        # Defino el testigo
        involucra_testigo = Involucra.create(
            dni=49198438,
            idcaso=get_current_id("caso"),
            idrol=TipoRol.Testigo,
        )
        # Defino investigador principal
        involucra_investigador = Involucra.create(
            dni=47274813,
            idcaso=get_current_id("caso"),
            idrol=2,
        )
        # Defino investigador auxiliar
        involucra_auxiliar = Involucra.create(
            dni=49146016,
            idcaso=get_current_id("caso"),
            idrol=3,
        )

        # Creo un testimonio
        testimonio = Testimonio.create(
            dnioficial=involucra_auxiliar.dni.dni,
            dnipersona=involucra_testigo.dni.dni,
            fecha=date(2016, 9, 10),
            idcaso=get_current_id("caso"),
            idtestimonio=get_new_id("testimonio"),
            texto="Entre a la cocina y lo vi a Pepito sospechosamente parado cerca del plato de medialunas",
        )

        # Creo la primer evidencia y dos custodias para la misma
        evidencia0 = Evidencia.create(
            descripcion="Servilleta manchada con almibar",
            fechahallazgo=date(2016, 9, 4),
            fechaingreso=date(2016, 9, 4),
            fechasellado=date(2016, 9, 4),
            idcaso=get_current_id("caso"),
            iddireccionactual=involucra_auxiliar.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_new_id("evidencia"),
        )
        custodia0 = Custodia.create(
            comentario="Registro inicial de esta evidencia",
            fecha=date(2016, 9, 6),
            idcustodia=get_new_id("custodia"),
            iddireccion=involucra_auxiliar.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_current_id("evidencia"),
            idoficial=involucra_auxiliar.dni.dni
        )
        custodia1 = Custodia.create(
            comentario="Paso a manos del investigador principal",
            fecha=date(2016, 9, 7),
            idcustodia=get_new_id("custodia"),
            iddireccion=involucra_investigador.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_current_id("evidencia"),
            idoficial=involucra_investigador.dni.dni
        )

        # Creo otra evidencia con una custodia
        evidencia1 = Evidencia.create(
            descripcion="Envoltorio de la panaderia 'El gran canon' ",
            fechahallazgo=date(2016, 9, 4),
            fechaingreso=date(2016, 9, 4),
            fechasellado=date(2016, 9, 4),
            idcaso=get_current_id("caso"),
            iddireccionactual=involucra_auxiliar.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_new_id("evidencia"),
        )
        custodia2 = Custodia.create(
            comentario="Ingreso inicial de la evidencia",
            fecha=date(2016, 9, 6),
            idcustodia=get_new_id("custodia"),
            iddireccion=involucra_investigador.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_current_id("evidencia"),
            idoficial=involucra_investigador.dni.dni
        )

        # Creo tres eventos
        evento0 = Evento.create(
            descripcion="Se vio al sospechoso comiendo medialunas",
            fecha=date(2016, 9, 8),
            idcaso=get_current_id("caso"),
            idevento=get_new_id("evento"),
        )
        evento1 = Evento.create(
            descripcion="Se presenta un posible testigo",
            fecha=date(2016, 9, 9),
            idcaso=get_current_id("caso"),
            idevento=get_new_id("evento"),
        )
        evento2 = Evento.create(
            descripcion="Se le toma testimonio al testigo",
            fecha=date(2016, 9, 10),
            idcaso=get_current_id("caso"),
            idevento=get_new_id("evento"),
        )
    except Exception, e:
        print e
    else:
        pass


def crear_caso_ayudante():
    ''' Crea el terrible caso del asesinato del ayudante de 2da '''
    try:
        caso = Caso.create(
            descripcion="La victima fue misteriosamente asesinada despues de recibir muy buenas criticas en las encuestas",
            fecha=date(2016, 9, 1),
            fechaingreso= date.today(),
            idcaso=get_new_id("caso"),
            idcategoria=33, # Delito politico, porque si
            lugar="Laboratorio 2 del DC",
            tipo=TipoCaso.Pendiente
        )
        # Defino el principal sospechoso
        involucra_sospechoso = Involucra.create(
            dni=33843285,
            idcaso=get_current_id("caso"),
            idrol=0,
        )
        # Defino el testigo
        involucra_testigo = Involucra.create(
            dni=41355325,
            idcaso=get_current_id("caso"),
            idrol=TipoRol.Testigo,
        )
        # Defino investigador principal
        involucra_investigador = Involucra.create(
            dni=47846467,
            idcaso=get_current_id("caso"),
            idrol=2,
        )
        # Defino investigador auxiliar
        involucra_auxiliar = Involucra.create(
            dni=44236876,
            idcaso=get_current_id("caso"),
            idrol=3,
        )

        # Creo un testimonio
        testimonio = Testimonio.create(
            dnioficial=involucra_auxiliar.dni.dni,
            dnipersona=involucra_testigo.dni.dni,
            fecha=date(2016, 9, 12),
            idcaso=get_current_id("caso"),
            idtestimonio=get_new_id("testimonio"),
            texto="Vi a Juancito a solas con Pepito en un puesto de bondiola en la costanera",
        )

        # Creo la primer evidencia y dos custodias para la misma
        evidencia0 = Evidencia.create(
            descripcion="Sanguche de bondiola mordido",
            fechahallazgo=date(2016, 9, 13),
            fechaingreso=date(2016, 9, 14),
            fechasellado=date(2016, 9, 13),
            idcaso=get_current_id("caso"),
            iddireccionactual=involucra_auxiliar.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_new_id("evidencia"),
        )
        custodia0 = Custodia.create(
            comentario="El sanguche esta en buen estado",
            fecha=date(2016, 9, 14),
            idcustodia=get_new_id("custodia"),
            iddireccion=involucra_auxiliar.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_current_id("evidencia"),
            idoficial=involucra_auxiliar.dni.dni
        )
        custodia1 = Custodia.create(
            comentario="El sanguche se esta descomponiendo",
            fecha=date(2016, 9, 15),
            idcustodia=get_new_id("custodia"),
            iddireccion=involucra_investigador.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_current_id("evidencia"),
            idoficial=involucra_investigador.dni.dni
        )

        # Creo otra evidencia con una custodia
        evidencia1 = Evidencia.create(
            descripcion="El cuerpo muerto del ayudente",
            fechahallazgo=date(2016, 9, 13),
            fechaingreso=date(2016, 9, 14),
            fechasellado=date(2016, 9, 13),
            idcaso=get_current_id("caso"),
            iddireccionactual=involucra_auxiliar.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_new_id("evidencia"),
        )
        custodia2 = Custodia.create(
            comentario="Ingreso del cuerpo a la morgue",
            fecha=date(2016, 9, 14),
            idcustodia=get_new_id("custodia"),
            iddireccion=involucra_investigador.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=get_current_id("evidencia"),
            idoficial=involucra_investigador.dni.dni
        )

        # Creo tres eventos
        evento0 = Evento.create(
            descripcion="Se vio al sospechoso escondiendo un cuerpo",
            fecha=date(2016, 9, 17),
            idcaso=get_current_id("caso"),
            idevento=get_new_id("evento"),
        )
        evento1 = Evento.create(
            descripcion="Se vio al sospechoso leyendo el libro 'como cometer el climen perfecto'",
            fecha=date(2016, 9, 18),
            idcaso=get_current_id("caso"),
            idevento=get_new_id("evento"),
        )
        evento2 = Evento.create(
            descripcion="El sospechoso fue visto en la escena del crimen comiendo un choripan",
            fecha=date(2016, 9, 19),
            idcaso=get_current_id("caso"),
            idevento=get_new_id("evento"),
        )

        # Creo el caso resuelto
        caso_resuelto = Resuelto.create(
            descripcion=caso.descripcion,
            dnioficial=involucra_investigador.dni.dni,
            fecharesolucion=date(2019, 9, 20),
            idcaso=get_current_id("caso")
        )

        # Defino el culpable
        culpable = Culpable.create(
            dni=involucra_sospechoso.dni.dni,
            idcaso=get_current_id("caso")
        )

    except Exception, e:
        print e
    else:
        pass

def crear_caso_congelado():
    caso = Caso.create(
        descripcion="Alguien esta vendiendo fernet en la Noriega", 
        fecha=date(2016, 1, 1), 
        fechaingreso=date(2016, 1, 3), 
        idcaso=get_new_id("caso"), 
        idcategoria=5, 
        lugar="La Biblioteca Noriega", 
        tipo=TipoCaso.Pendiente, 
    )

    involucra_investigador = Involucra.create(
        dni=42348958, 
        idcaso=get_current_id("caso"), 
        idrol=2, 
    )

    caso_congelado = Congelado.create(
        comentario="No hay hielo :(",
        fechacancelacion=date.today(),
        idcaso=get_current_id("caso"),
    )

def crear_caso_descartado():
    caso = Caso.create(
        descripcion="Abandono de grupo de TP",
        fecha=date(2016, 9, 1),
        fechaingreso= date.today(),
        idcaso=get_new_id("caso"),
        idcategoria=7, # Alta traicion
        lugar="Iglesia",
        tipo=TipoCaso.Pendiente
    )

    caso_descartado = Descartado.create(
        motivos="Esto paso el cuatrimestre pasado",
        fechadescarte=date.today(),
        idcaso=get_current_id("caso")
    )

if __name__ == "__main__":
    vaciar_base()
    # crear_categorias()
    # crear_roles()
    # crear_direcciones()
    # crear_personas()
    # crear_rangos()
    # crear_servicios()
    # crear_departamentos()
    # crear_oficiales()
    crear_caso_medialunas()
    crear_caso_ayudante()
    crear_caso_congelado()
    crear_caso_descartado()