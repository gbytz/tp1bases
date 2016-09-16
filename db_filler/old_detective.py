from peewee import *

database = MySQLDatabase('detective', **{'host': '192.168.1.104', 'port': 3306, 'user': 'monsi'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Categoria(BaseModel):
    descripcion = TextField()
    idcategoria = PrimaryKeyField(db_column='idCategoria')

    class Meta:
        db_table = 'categoria'

class Caso(BaseModel):
    descripcion = TextField()
    fecha = DateTimeField()
    fechaingreso = DateTimeField(db_column='fechaIngreso')
    idcaso = PrimaryKeyField(db_column='idCaso')
    idcategoria = ForeignKeyField(db_column='idCategoria', rel_model=Categoria, to_field='idcategoria')
    lugar = CharField()
    tipo = CharField(null=True)

    class Meta:
        db_table = 'caso'

class Direccion(BaseModel):
    calle = CharField(null=True)
    departamento = CharField(null=True)
    iddireccion = PrimaryKeyField(db_column='idDireccion')
    localidad = CharField(null=True)
    numero = IntegerField(null=True)
    piso = CharField(null=True)
    provincia = CharField(null=True)

    class Meta:
        db_table = 'direccion'

class Persona(BaseModel):
    apellido = CharField()
    dni = PrimaryKeyField()
    fechanacimieto = DateField(db_column='fechaNacimieto')
    iddireccion = ForeignKeyField(db_column='idDireccion', rel_model=Direccion, to_field='iddireccion')
    nombre = CharField()
    tipo = IntegerField()

    class Meta:
        db_table = 'persona'

class Rol(BaseModel):
    descripcion = TextField()
    idrol = PrimaryKeyField(db_column='idRol')

    class Meta:
        db_table = 'rol'

class Involucra(BaseModel):
    dni = ForeignKeyField(db_column='dni', rel_model=Persona, to_field='dni')
    idcaso = ForeignKeyField(db_column='idCaso', rel_model=Caso, to_field='idcaso')
    idrol = ForeignKeyField(db_column='idRol', rel_model=Rol, to_field='idrol')

    class Meta:
        db_table = 'involucra'
        indexes = (
            (('dni', 'idcaso'), True),
        )
        primary_key = CompositeKey('dni', 'idcaso')

class Evento(BaseModel):
    descripcion = TextField()
    fecha = DateTimeField()
    idcaso = ForeignKeyField(db_column='idCaso', rel_model=Caso, to_field='idcaso')
    idevento = IntegerField(db_column='idEvento')

    class Meta:
        db_table = 'evento'
        indexes = (
            (('idcaso', 'idevento'), True),
        )
        primary_key = CompositeKey('idcaso', 'idevento')

class Compromete(BaseModel):
    dni = ForeignKeyField(db_column='dni', rel_model=Involucra, to_field='dni')
    idcaso = ForeignKeyField(db_column='idCaso', rel_model=Evento, related_name='involucra_idcaso_set', to_field='idcaso')
    idevento = ForeignKeyField(db_column='idEvento', rel_model=Evento, related_name='evento_idevento_set', to_field='idevento')

    class Meta:
        db_table = 'compromete'
        indexes = (
            (('idcaso', 'dni'), False),
            (('idcaso', 'idevento', 'dni'), True),
        )
        primary_key = CompositeKey('dni', 'idcaso', 'idevento')

class Congelado(Caso):
    comentario = CharField()
    fecha = DateTimeField()
    # idcaso = ForeignKeyField(db_column='idCaso', primary_key=True, rel_model=Caso, to_field='idcaso')

    class Meta:
        db_table = 'congelado'

class Culpable(BaseModel):
    dni = ForeignKeyField(db_column='dni', rel_model=Involucra, to_field='dni')
    idcaso = ForeignKeyField(db_column='idCaso', rel_model=Involucra, related_name='involucra_idcaso_set', to_field='idcaso')

    class Meta:
        db_table = 'culpable'
        indexes = (
            (('idcaso', 'dni'), False),
            (('idcaso', 'dni'), True),
        )
        primary_key = CompositeKey('dni', 'idcaso')

class Rango(BaseModel):
    idrango = PrimaryKeyField(db_column='idRango')
    nombre = CharField()

    class Meta:
        db_table = 'rango'

class Departamento(BaseModel):
    iddepartamento = PrimaryKeyField(db_column='idDepartamento')
    iddireccion = ForeignKeyField(db_column='idDireccion', rel_model=Direccion, to_field='iddireccion')
    idsupervisor = ForeignKeyField(db_column='idSupervisor', null=True, rel_model='self', to_field='iddepartamento')
    nombre = CharField()

    class Meta:
        db_table = 'departamento'

class Servicio(BaseModel):
    idservicio = PrimaryKeyField(db_column='idServicio')
    nombre = CharField()

    class Meta:
        db_table = 'servicio'

class Oficial(Persona):
    # dni = ForeignKeyField(db_column='dni', primary_key=True, rel_model=Persona, to_field='dni')
    fechaingreso = DateField(db_column='fechaIngreso')
    iddepto = ForeignKeyField(db_column='idDepto', rel_model=Departamento, to_field='iddepartamento')
    idrango = ForeignKeyField(db_column='idRango', rel_model=Rango, to_field='idrango')
    idservicio = ForeignKeyField(db_column='idServicio', rel_model=Servicio, to_field='idservicio')
    numeroescritorio = IntegerField(db_column='numeroEscritorio')
    numeroplaca = IntegerField(db_column='numeroPlaca', unique=True)

    class Meta:
        db_table = 'oficial'

class Evidencia(BaseModel):
    descripcion = TextField()
    fechahallazgo = DateTimeField(db_column='fechaHallazgo')
    fechaingreso = DateTimeField(db_column='fechaIngreso')
    fechasellado = DateTimeField(db_column='fechaSellado')
    idcaso = ForeignKeyField(db_column='idCaso', rel_model=Caso, to_field='idcaso')
    iddireccionactual = ForeignKeyField(db_column='idDireccionActual', rel_model=Direccion, to_field='iddireccion')
    idevidencia = PrimaryKeyField(db_column='idEvidencia')

    class Meta:
        db_table = 'evidencia'

class Custodia(BaseModel):
    comentario = TextField()
    fecha = DateTimeField()
    idcustodia = IntegerField(db_column='idCustodia')
    iddireccion = ForeignKeyField(db_column='idDireccion', rel_model=Direccion, to_field='iddireccion')
    idevidencia = ForeignKeyField(db_column='idEvidencia', rel_model=Evidencia, to_field='idevidencia')
    idoficial = ForeignKeyField(db_column='idOficial', rel_model=Oficial, to_field='dni')

    class Meta:
        db_table = 'custodia'
        indexes = (
            (('idcustodia', 'idevidencia'), True),
        )
        primary_key = CompositeKey('idcustodia', 'idevidencia')

class Descartado(Caso):
    fecha = DateTimeField(null=True)
    # idcaso = ForeignKeyField(db_column='idCaso', primary_key=True, rel_model=Caso, to_field='idcaso')
    motivos = CharField(null=True)

    class Meta:
        db_table = 'descartado'

class Oficialescustodios(BaseModel):
    dni = IntegerField()
    idcaso = IntegerField(db_column='idCaso')

    class Meta:
        db_table = 'oficialesCustodios'

class Oficialescustodiosmasdeuncaso(BaseModel):
    dni = IntegerField()

    class Meta:
        db_table = 'oficialesCustodiosMasDeUnCaso'

class Ranking(BaseModel):
    cantidades = BigIntegerField()
    dni = IntegerField()

    class Meta:
        db_table = 'ranking'

class Resuelto(Caso):
    descripcion = CharField(null=True)
    dnioficial = ForeignKeyField(db_column='dniOficial', rel_model=Involucra, to_field='dni')
    fecha = DateTimeField()
    # idcaso = ForeignKeyField(db_column='idCaso', primary_key=True, rel_model=Involucra, related_name='involucra_idcaso_set', to_field='idcaso')

    class Meta:
        db_table = 'resuelto'
        indexes = (
            (('idcaso', 'dnioficial'), False),
        )

class Sospechosos(BaseModel):
    apellido = CharField()
    dni = IntegerField()
    domicilio = IntegerField()
    fechanacimieto = DateField(db_column='fechaNacimieto')
    nombre = CharField()
    tipo = IntegerField()

    class Meta:
        db_table = 'sospechosos'

class Telefonodepartamento(BaseModel):
    iddepartamento = ForeignKeyField(db_column='idDepartamento', rel_model=Departamento, to_field='iddepartamento')
    telefono = CharField()

    class Meta:
        db_table = 'telefonoDepartamento'
        indexes = (
            (('iddepartamento', 'telefono'), True),
        )
        primary_key = CompositeKey('iddepartamento', 'telefono')

class Telefonopersona(BaseModel):
    dni = ForeignKeyField(db_column='dni', rel_model=Persona, to_field='dni')
    telefono = CharField()

    class Meta:
        db_table = 'telefonoPersona'
        indexes = (
            (('dni', 'telefono'), True),
        )
        primary_key = CompositeKey('dni', 'telefono')

class Testimonio(BaseModel):
    dnioficial = ForeignKeyField(db_column='dniOficial', rel_model=Oficial, to_field='dni')
    dnipersona = ForeignKeyField(db_column='dniPersona', rel_model=Persona, related_name='persona', to_field='dni')
    fecha = DateTimeField()
    idcaso = ForeignKeyField(db_column='idCaso', rel_model=Caso, related_name='caso', to_field='idcaso')
    idtestimonio = IntegerField(db_column='idTestimonio')
    texto = TextField()

    class Meta:
        db_table = 'testimonio'
        indexes = (
            (('dnioficial', 'idcaso'), False),
            (('idcaso', 'dnipersona'), False),
            (('idcaso', 'idtestimonio'), True),
        )
        primary_key = CompositeKey('idcaso', 'idtestimonio')

