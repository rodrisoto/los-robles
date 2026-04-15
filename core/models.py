from django.db import models


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=120)
    contrasena_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=9)
    estado = models.CharField(max_length=8, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        managed = False
        db_table = 'usuarios'


class Pacientes(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    rut = models.CharField(unique=True, max_length=15)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=4, blank=True, null=True)
    habitacion = models.CharField(max_length=20, blank=True, null=True)
    diagnostico_principal = models.CharField(max_length=255, blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=9, blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        managed = False
        db_table = 'pacientes'


class Medicamentos(models.Model):
    id_medicamento = models.AutoField(primary_key=True)
    nombre_generico = models.CharField(max_length=120)
    nombre_comercial = models.CharField(max_length=120, blank=True, null=True)
    concentracion = models.CharField(max_length=50, blank=True, null=True)
    forma_farmaceutica = models.CharField(max_length=50, blank=True, null=True)
    via_administracion = models.CharField(max_length=50, blank=True, null=True)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=8, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre_generico

    class Meta:
        managed = False
        db_table = 'medicamentos'


class LotesMedicamento(models.Model):
    id_lote = models.AutoField(primary_key=True)
    id_medicamento = models.ForeignKey(Medicamentos, models.CASCADE, db_column='id_medicamento')
    numero_lote = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    stock_actual = models.IntegerField()
    stock_minimo = models.IntegerField()
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=7, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Lote {self.numero_lote}"

    class Meta:
        managed = False
        db_table = 'lotes_medicamento'
        unique_together = (('id_medicamento', 'numero_lote'),)


class Tratamientos(models.Model):
    id_tratamiento = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(Pacientes, models.CASCADE, db_column='id_paciente')
    id_medicamento = models.ForeignKey(Medicamentos, models.CASCADE, db_column='id_medicamento')
    medico_indicador = models.CharField(max_length=120, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=10, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(Usuarios, models.SET_NULL, db_column='creado_por', blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tratamientos'


class HistorialDosis(models.Model):
    id_historial_dosis = models.AutoField(primary_key=True)
    id_tratamiento = models.ForeignKey(Tratamientos, models.CASCADE, db_column='id_tratamiento')
    dosis_descripcion = models.CharField(max_length=100)
    cantidad_por_dosis = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_dosis = models.CharField(max_length=30)
    frecuencia_horas = models.IntegerField(blank=True, null=True)
    tomas_por_dia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    horario_indicacion = models.CharField(max_length=150, blank=True, null=True)
    tipo_indicacion = models.CharField(max_length=4, blank=True, null=True)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField(blank=True, null=True)
    cobertura_estimada_dias = models.IntegerField(blank=True, null=True)
    motivo_cambio = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(Usuarios, models.SET_NULL, db_column='creado_por', blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial_dosis'


class Administraciones(models.Model):
    id_administracion = models.AutoField(primary_key=True)
    id_historial_dosis = models.ForeignKey(HistorialDosis, models.CASCADE, db_column='id_historial_dosis')
    id_usuario = models.ForeignKey(Usuarios, models.SET_NULL, db_column='id_usuario', blank=True, null=True)
    fecha_hora_programada = models.DateTimeField()
    fecha_hora_administrada = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=12, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administraciones'


class MovimientosStock(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey(LotesMedicamento, models.CASCADE, db_column='id_lote')
    tipo_movimiento = models.CharField(max_length=7)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=150, blank=True, null=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    id_usuario = models.ForeignKey(Usuarios, models.SET_NULL, db_column='id_usuario', blank=True, null=True)
    fecha_movimiento = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movimientos_stock'


class Alertas(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey(LotesMedicamento, models.CASCADE, db_column='id_lote')
    tipo_alerta = models.CharField(max_length=11)
    mensaje = models.CharField(max_length=255)
    estado = models.CharField(max_length=9, blank=True, null=True)
    fecha_alerta = models.DateTimeField(blank=True, null=True)
    fecha_resolucion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alertas'
