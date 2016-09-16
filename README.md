# tp1bases

************************************************************************************************************************

¿Cómo instalar peewee?

0) Instalar las herramientas de compilacion. (Algunos paquetes de python necesitan compilar algunas de sus dependencias)

	sudo apt-get install build-essential

1) Instalar pip. (Se usa para instalar paquetes de python de manera automágica)

Bajar el script get-pip.py de acá: https://bootstrap.pypa.io/get-pip.py
En una terminal, se paran en el directorio donde bajaron el script y lo ejecutan (por las dudas con 'sudo')

	sudo python get-pip.y

3) Instalar mysql_config. (Se necesita para que pueda compilar el paquete que instalamos en el paso siguiente)

	sudo apt-get install libmysqlclient-dev

4) Instalar MySQL-python. (Este es el módulo que contiene el driver de MySQL que peewee necesita)

	sudo pip install MySQL-python

5) Instalar peewee. (Este es el ORM mágico)

	sudo pip install peewee

************************************************************************************************************************

¿Cómo generar el archivo detective.py?

Una vez instalado peewee es posible utilizar el modulo pwiz para escanerar una base de datos existente y generar automágicamente código python
que se puede usar para manipular la base de manera programática.
Para eso en una terminar ejecutamos:

	python -m pwiz -e mysql -u losdensos -H db4free.net tp1bases

Les va a pedir un password, el cual es 'tp1bases'

Los explico parte por parte de este comando

	python -m pwiz 		<--- Le dice al interprete de python que ejecute el módulo especificado, en este caso es 'pwiz'
	-e mysql			<--- pwiz recibe el parametro -e que define el motor de base de datos que va a utilizar, en este caso es 'mysql'
	-u losdensos 		<--- pwiz recibe el parámetro -u que define el nombre de usuario que se usa para conectarse a la base de datos, en este caso es 'losdensos'
	-H db4free.net		<--- pwiz recibe el parámetro -H que define la dirección del host de la base de datos, en este caso 'db4free.net'
	tp1bases 			<--- pwiz recibe como último parametro el nombre de la base de datos a la que se va a conectar, en este caso 'tp1bases'

Al ejecutarlo va a escupir por salida estandar el código generado automágicamente. Pueden redireccionar la salida a un archivo, así:

	python -m pwiz -e mysql -u losdensos -H db4free.net tp1bases > detective.py

Eso debería generarles un archivo 'detective.py' con el código mágico de peewee.

************************************************************************************************************************

¿Cómo usar detective.py?

Primero tienen que cargar el modulo. Estando en el directorio donde tienen el archivo detective.py abren una consola de python y hacen:

	from detective import *

Si no hay ningún problema al importar el modulo ya deberían poder usarlo.
Un ejemplo de uso: imprimir nombre y apellido de todas las personas:

	for persona in Persona.select():
		print persona.nombre, persona.apellido

************************************************************************************************************************

¿Qué es db_filler.py?

Es un script con varias funciones que llenan la base de datos con algunos datos de prueba, ahí pueden ver otros ejemplos de uso de detective.py.

