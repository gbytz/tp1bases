#!/usr/local/bin/python

from datetime import date
from random import choice, randint

from detective import *


class TipoCaso:
    Pendiente = 0
    Congelado = 1
    Descartado = 2
    Resuelto = 3

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
            idcaso=0, # El primer caso que creo a mano
            idcategoria=76, # Robo de medialunas
            lugar="La juntada de TP",
            tipo=TipoCaso.Pendiente
        )
        # Defino el principal sospechoso
        involucra_sospechoso = Involucra.create(
            dni=33843285,
            idcaso=0,
            idrol=0,
        )
        # Defino el testigo
        involucra_testigo = Involucra.create(
            dni=49198438,
            idcaso=0,
            idrol=7,
        )
        # Defino investigador principal
        involucra_investigador = Involucra.create(
            dni=47274813,
            idcaso=0,
            idrol=2,
        )
        # Defino investigador auxiliar
        involucra_auxiliar = Involucra.create(
            dni=49146016,
            idcaso=0,
            idrol=3,
        )

        # Creo un testimonio
        testimonio = Testimonio.create(
            dnioficial=involucra_auxiliar.dni.dni,
            dnipersona=involucra_testigo.dni.dni,
            fecha=date(2016, 9, 10),
            idcaso=caso.idcaso,
            idtestimonio=0,
            texto="Entre a la cocina y lo vi a Pepito sospechosamente parado cerca del plato de medialunas",
        )

        evidencia0 = Evidencia.create(
            descripcion="Servilleta manchada con almibar",
            fechahallazgo=date(2016, 9, 4),
            fechaingreso=date(2016, 9, 4),
            fechasellado=date(2016, 9, 4),
            idcaso=caso.idcaso,
            iddireccionactual=involucra_auxiliar.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=0,
        )

        evidencia1 = Evidencia.create(
            descripcion="Envoltorio de la panaderia 'El gran canon' ",
            fechahallazgo=date(2016, 9, 4),
            fechaingreso=date(2016, 9, 4),
            fechasellado=date(2016, 9, 4),
            idcaso=caso.idcaso,
            iddireccionactual=involucra_auxiliar.dni.oficial_set.get().iddepto.iddireccion,
            idevidencia=evidencia0.idevidencia + 1,
        )

    except Exception, e:
        print e
    else:
        pass


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