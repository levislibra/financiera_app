# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AppConfig(models.Model):
	_name = 'app.config'

	name = fields.Char('Nombre')
	# Parametros de la solicitud
	desactivar_solicitud_prestamo = fields.Boolean('Desactivar solicitud de prestamo')
	monto_minimo_solicitud = fields.Float('Monto minimo de solicitud')
	monto_maximo_solicitud = fields.Float('Monto maximo de solicitud')
	ingreso_minimo_solicitud = fields.Float('Ingreso minimo requerido', help='Inferior a este monto bloqueara al dni solicitante.')
	mensaje_sin_ofertas = fields.Text('Mensaje sin ofertas')
	numero_whatsapp_soporte = fields.Char('Numero whatsapp para soporte')
	app_ver_y_compartir_riesgo_cliente = fields.Boolean("Ver y compartir riesgo cliente")
	# deprecate
	monto_incremento = fields.Integer('Monto incremento')
	# deprecate
	monto_inicial = fields.Float('Monto inicial')
	# deprecate
	cuotas_minimas_solicitud = fields.Float('Cantidad minima de cuotas en solicitud')
	# deprecate
	cuotas_maximas_solicitud = fields.Float('Cantidad maxima de cuotas en solicitud')
	# deprecate
	cuotas_incremento = fields.Integer('Cantidad de incremento')
	# deprecate
	cuotas_inicial = fields.Float('Cantidad de cuotas inicial')
	# Opciones movil
	app_sucursal_id = fields.Many2one('financiera.entidad', 'Entidad')
	app_responsable_id = fields.Many2one('res.users', 'Responsable')
	app_origen_id = fields.Many2one('financiera.prestamo.origen', 'Origen del prestamo en movil')
	# Opciones portal
	portal_sucursal_id = fields.Many2one('financiera.entidad', 'Entidad')
	portal_responsable_id = fields.Many2one('res.users', 'Responsable')
	portal_origen_id = fields.Many2one('financiera.prestamo.origen', 'Origen del prestamo en portal')
	# unique_documentation_report = fields.Char('Nombre del reporte unico a firmar por el cliente')
	company_id = fields.Many2one('res.company', 'Empresa', required=False)
	planes_disponibles_ids = fields.Many2many('financiera.prestamo.plan', 'financiera_config_plan_rel', 'plan_id', 'config_id', string='Planes disponibles')
	comprobar_codigo_prestamo = fields.Boolean("Comprobar codigo del prestamo adjunto en email o sms")
	comprobar_mensaje_original = fields.Boolean("Comprobar si la respuesta por mail contiene el mensaje original")
	# Requisitos prestamo portal
	app_requiere_direccion = fields.Boolean("Requiere direccion")
	app_requiere_cbu = fields.Boolean("Requiere CBU")
	app_requiere_trabajo_actual = fields.Boolean("Requiere trabajo actual")
	app_requiere_contactos = fields.Integer("Requiere contactos")
	app_requeire_tarjeta_debito = fields.Boolean("Requiere trajeta de debito")
	app_requiere_dni_frontal = fields.Boolean("requiere DNI frontal")
	app_requiere_dni_dorso = fields.Boolean("requiere DNI dorso")
	app_requiere_selfie = fields.Boolean("Requiere selfie")
	app_requiere_recibo_sueldo = fields.Boolean("Requiere recibo de sueldo")
	app_requiere_servicio = fields.Boolean("Requiere servicio")
	app_requiere_firma = fields.Boolean("Requiere firma")
	app_requiere_banco = fields.Boolean("Requiere Banco de cobro")
	app_requiere_fecha_cobro = fields.Boolean("Requiere fecha de cobro")