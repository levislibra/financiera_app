# -*- coding: utf-8 -*-

import openerp
from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging
import json
import base64

class ExtendsResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	app_estado_portal = fields.Char("Estado portal")
	app_estado_bloqueado = fields.Boolean("Usuario bloqueado")
	app_ip_registro = fields.Char("IP al registrarse")
	app_ip_registro_no_confiable = fields.Boolean("IP no confiable")
	# Datos Personales
	app_nombre = fields.Char('Nombre')
	app_apellido = fields.Char('Apellido')
	app_documento = fields.Char('Documento')
	app_nacimiento = fields.Date('Nacimiento')
	app_edad = fields.Integer('Edad')
	# Datos Domicilio
	app_direccion = fields.Char('Direccion')
	app_numero = fields.Char('Numero')
	app_cp = fields.Char('CP')
	app_telefono = fields.Char('Telefono fijo')
	app_localidad = fields.Char('Ciudad')
	app_provincia_id = fields.Many2one('res.country.state', "Provincia")
	# Datos Egreso e Ingreso
	app_deuda = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Le debes a otra entidad financiera?")
	app_deuda_monto_mensual = fields.Char("Deuda que paga mensual")
	app_deuda_estado = fields.Selection([
		('al_dia', 'Al dia'),
		('con_atraso', 'Con atraso')
	], "Estado de la deuda")
	app_ingreso_fijo = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Tienes un ingreso fijo?")
	app_dia_cobro = fields.Integer("Dia de cobro")
	app_ingreso = fields.Char("Ingreso")
	app_ingreso_pareja = fields.Char("Ingreso de la pareja")
	app_asignaciones = fields.Char("Ingrso por asignaciones")
	app_otros_ingresos = fields.Char("Otros ingresos")
	app_monto_de_cuota = fields.Float("Monto de cuota que puedes pagar")
	app_ocupacion = fields.Char("Ocupacion")
	app_ocupacion_anos = fields.Integer("Años que trabajas ahi?")
	app_puesto = fields.Char("Puesto")
	# Datos vivienda y transporte
	app_vivienda = fields.Selection([
		('alquilada', 'Alquilada'),
		('propia', 'Propia')
	], "Vivienda")
	app_alquiler = fields.Char("Monto alquiler")
	app_hipoteca = fields.Char("Credito hipotecario")
	app_vivienda_tiempo = fields.Char("Anos que vive ahi")
	app_vivienda_hijos = fields.Char("Hijos que conviven")
	app_transporte = fields.Selection([
		('publico', 'Publico'),
		('auto', 'Auto'),
		('moto', 'Moto')
	], "Medio de transporte frecuente")
	app_prendario = fields.Selection([
		('si', 'Si tengo'),
		('no', 'No tengo')
	], "Tienes credito prendario?")
	app_vehiculo = fields.Selection([
		('si', 'Si tengo'),
		('no', 'No tengo')
	], 'Tiene un vehículo a su nombre?')
	app_vehiculo_modelo = fields.Integer('Modelo del vehículo')
	# Nivel de estudios
	app_nivel_estudio = fields.Selection([('sin_estudios', 'Sin estudios'), ('primario', 'Primario'), ('secundario', 'Secundario'), ('terciario', 'Terciario'), ('universitario', 'Universitario')], "Nivel de estudio")
	# Preguntas De comportamiento
	app_dia_de_pago = fields.Selection([('primer_dia_mes', 'Primer día del mes'), ('apenas_cobro', 'Apenas cobro'), ('dia_vencimiento', 'El mismo dia que vence')], "¿Tiene que realizar un pago el 20 de cada mes, cuando lo haces?")
	app_utiliza_mercado_pago = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Utilizas Mercado Pago?")
	app_utiliza_uala = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Utilizas Uala?")
	app_utiliza_cabal = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Utilizas Cabal?")
	app_utiliza_cencosud = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Utilizas Cencosud?")
	app_historial_prestamos = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Tuviste prestamos en el pasado?")
	app_historial_prestamos_incumplimientos = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Tuviste incumplimientos sobre prestamos en el pasado?")
	app_historial_alquileres_incumplimientos = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Tuviste incumplimientos sobre alquileres en el pasado?")
	app_historial_tarjetas_incumplimientos = fields.Selection([('si', 'Si'), ('no', 'No')], "¿Tuviste incumplimientos sobre tarjetas de credito en el pasado?")
	# DNI frente
	app_dni_frontal = fields.Binary("DNI frontal")
	app_dni_frontal_completo = fields.Boolean("DNI frontal completo", compute='_compute_app_dni_frontal_completo')
	app_dni_frontal_download = fields.Binary("", related="app_dni_frontal")
	app_dni_frontal_download_name = fields.Char("", default="dni-frontal.jpeg")
	# DNI dorso
	app_dni_posterior = fields.Binary("DNI dorso")
	app_dni_posterior_completo = fields.Boolean("DNI dorso completo", compute='_compute_app_dni_posterior_completo')
	app_dni_posterior_download = fields.Binary("", related="app_dni_posterior")
	app_dni_posterior_download_name = fields.Char("", default="dni-dorso.jpeg")
	# Selfie
	app_selfie = fields.Binary("Selfie")
	app_selfie_completo = fields.Boolean("Selfie completo", compute='_compute_app_selfie_completo')
	app_selfie_download = fields.Binary("", related="app_selfie")
	app_selfie_download_name = fields.Char("", default="selfie.jpeg")
	# CBU
	app_banco_haberes_numero_entidad = fields.Char("Numero entidad bancaria")
	app_banco_haberes = fields.Char('Banco', compute='_compute_app_banco_haberes')
	app_cbu = fields.Char("CBU")
	app_alias = fields.Char("Alias")
	# Celular
	app_numero_celular = fields.Char("Numero de celular", related='mobile')
	app_numero_celular_validado = fields.Boolean("Celular validado?")
	app_codigo_introducido_usuario = fields.Char("Codigo")
	app_codigo = fields.Char("Codigo generado")
	app_button_solicitar_codigo_fecha_reset = fields.Datetime("Fecha fin")
	# Otros datos a adjuntar
	app_recibo_sueldo = fields.Binary("Recibo de sueldo")
	app_recibo_sueldo_download = fields.Binary("", related="app_recibo_sueldo")
	app_recibo_sueldo_download_name = fields.Char("", default="recibo.jpeg")
	
	app_servicio = fields.Binary("Servicio")
	app_servicio_download = fields.Binary("", related="app_servicio")
	app_servicio_download_name = fields.Char("", default="servicio.jpeg")
	app_observaciones = fields.Char("Observaciones")
	# alertas
	alerta_ultima_actualizacion = fields.Date("Alertas actualizadas al")
	alerta_ip_multiple_registros = fields.Integer('Registros desde la misma IP')
	alerta_ip_multiple_registros_ids = fields.Many2many('res.partner', 'alerta_ip_multiple_registros_rel', 'partner_id', 'partner2_id', string='Registros desde la misma IP')

	alerta_celular_multiple_partner = fields.Integer('Clientes con el mismo celular')
	alerta_celular_multiple_partner_ids = fields.Many2many('res.partner', 'alerta_celular_multiple_partner_rel', 'partner_id', 'partner2_id', string='Clientes con el mismo celular')

	alerta_celular_como_contacto = fields.Integer('Contactos con el mismo celular')
	alerta_celular_como_contacto_ids = fields.Many2many('res.partner.contacto', 'alerta_celular_como_contacto_rel', 'partner_id', 'partner2_id', string='Contactos con el mismo celular')

	alerta_domicilio_similar = fields.Integer('Clientes con domicilio similar')
	alerta_domicilio_similar_ids = fields.Many2many('res.partner', 'alerta_domicilio_similar_rel', 'partner_id', 'partner2_id', string='Clientes con domicilio similar')

	alerta_prestamos_activos = fields.Integer('Prestamos activos')
	alerta_prestamos_cobrados = fields.Integer('Prestamos cobrados')
	
	alerta_cuotas_activas = fields.Integer('Cuotas activas')
	alerta_cuotas_cobradas = fields.Integer('Cuotas cobradas')
	alerta_cuotas_normal = fields.Integer('Cuotas normal')
	alerta_cuotas_preventivas = fields.Integer('Cuotas en preventiva')
	alerta_cuotas_temprana = fields.Integer('Cuotas en mora temprana')
	alerta_cuotas_media = fields.Integer('Cuotas en mora media')
	alerta_cuotas_tardia = fields.Integer('Cuotas en mora tardia')
	alerta_cuotas_incobrable = fields.Integer('Cuotas incobrable')
	alerta_fecha_ultimo_pago = fields.Char('Fecha ultimo pago')
	alerta_dias_ultimo_pago = fields.Integer('Dias del ultimo pago')
	# Datos compartidos entre financieras
	alerta_ver_y_compartir = fields.Boolean('Ver y compartir', compute='_app_ver_y_compartir_riesgo_cliente')
	alerta_registrado_financieras = fields.Integer('Registros')
	alerta_prestamos_activos_financieras = fields.Integer('Prestamos activos (otras fin.)')
	alerta_cuotas_vencidas_financieras = fields.Integer('Cuotas en mora (otras fin.)')
	alerta_compromiso_mensual_financieras = fields.Float('Compromiso mensual (otras fin.)')
	alerta_ip_no_confiable_financieras = fields.Integer('IP no confiable (otras fin.)')

	@api.one
	def button_confirmar_datos_numero_celular(self):
		if not self.app_numero_celular_validado:
			if self.app_codigo_introducido_usuario and self.app_codigo_introducido_usuario == self.app_codigo:
				self.app_numero_celular_validado = True
				self.mobile = self.app_numero_celular
				# self.app_codigo = None
			else:
				raise UserError("El codigo no coincide.")

	@api.one
	def button_modificar_celular(self):
		self.app_numero_celular_validado = False

	# @api.onchange('mobile')
	# def _onchange_validar_celular_cambiar_movil(self):
	# 	self.app_numero_celular_validado = False

	@api.multi
	def button_solicitar_codigo_portal(self):
		if self.app_button_solicitar_codigo_fecha_reset == False or self.app_button_solicitar_codigo_fecha_reset == None:
			self.sudo().button_solicitar_codigo()
			self.app_button_solicitar_codigo_fecha_reset = datetime.now() + timedelta(seconds=+120)
		else:
			fecha_fin = datetime.strptime(self.app_button_solicitar_codigo_fecha_reset, '%Y-%m-%d %H:%M:%S')
			if datetime.now() < fecha_fin:
				diferencia = fecha_fin - datetime.now()
				raise UserError("Vuelva a intentarlo en: "+str(diferencia.seconds // 60)+":"+str(diferencia.seconds % 60).zfill(2)+" segundos")
			else:
				self.app_button_solicitar_codigo_fecha_reset = None
				self.app_codigo = None
				self.button_solicitar_codigo_portal()
	

	@api.multi
	def wizard_datos_celular_validado_manual(self):
		self.ensure_one()
		self.app_codigo_introducido_usuario = False
		view_id = self.env.ref('financiera_app.datos_celular_validado_form', False)
		return {
			'name': 'Validar celular',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'res.partner',
			'res_id': self.id,
			'views': [(view_id.id, 'form')],
			'view_id': view_id.id,
			'target': 'new',
		}

	@api.multi
	def do_nothing(self):
		return {'type': 'ir.actions.do_nothing'}

	# Docuementada en la API - Para simulacion real de prestamo
	def obtener_datos_simulador(self):
		ret = []
		cr = self.env.cr
		uid = self.env.uid
		app_id = self.company_id.app_id
		planes_obj = self.pool.get('financiera.prestamo.plan')
		planes_ids = planes_obj.search(cr, uid, [
			('state', '=', 'confirmado'),
			('es_refinanciacion', '=', False),
			# ('id', 'in', planes_disponibles_ids),
			# '|', ('prestamo_tipo_ids', '=', False), ('prestamo_tipo_ids.id', '=', self.prestamo_tipo_id.id),
			'|', ('partner_tipo_ids', '=', False), ('partner_tipo_ids.id', '=', self.partner_tipo_id.id),
			'|', ('recibo_de_sueldo', '=', False), ('recibo_de_sueldo', '=', self.recibo_de_sueldo),
			('company_id', '=', self.company_id.id)], order="cuotas asc")
		seguros_obj = self.pool.get('financiera.prestamo.seguro')
		seguros_ids = seguros_obj.search(cr, uid, [
			('state', '=', 'confirmado'),
			('company_id', '=', self.company_id.id)])
		planes_disponibles_ids = [g.id for g in app_id.planes_disponibles_ids]
		for _id in planes_ids:
			if len(planes_disponibles_ids) == 0 or _id in planes_disponibles_ids:
				plan_id = self.env['financiera.prestamo.plan'].browse(_id)
				if plan_id.seguro_calcular:
					for i in seguros_ids:
						seguro_id = self.env['financiera.prestamo.seguro'].browse(i)
						# Compute indice
						indice = self.simular_indice_plan(plan_id, seguro_id)
						ret.append({
							'plan_id': plan_id.id,
							'nombre': plan_id.name,
							'cuotas': plan_id.cuotas,
							'indice': indice,
							'seguro_id': seguro_id.id,
						})
				else:
						indice = self.simular_indice_plan(plan_id, False)
						ret.append({
							'plan_id': plan_id.id,
							'nombre': plan_id.name,
							'cuotas': plan_id.cuotas,
							'indice': indice,
							'seguro_id': False,
						})
		return ret
	
	@api.multi
	def button_wizard_set_password(self):
		return self.wizard_set_password(False)

	@api.multi
	def wizard_set_password(self, password=None):
		params = {
			'partner_id': self.id,
			'nuevo_password': password,
		}
		view_id = self.env['res.partner.set.password.wizard']
		new = view_id.create(params)
		return {
			'type': 'ir.actions.act_window',
			'name': 'Nueva contraseña',
			'res_model': 'res.partner.set.password.wizard',
			'view_type': 'form',
			'view_mode': 'form',
			'res_id': new.id,
			'view_id': self.env.ref('financiera_app.set_password', False).id,
			'target': 'new',
		}

	@api.one
	def button_send_mail_password_generate(self):
		nuevo_password = self.password_generate()
		self.send_mail_password_generate(nuevo_password)

	@api.one
	def _compute_app_dni_frontal_completo(self):
		self.app_dni_frontal_completo = False
		if self.app_dni_frontal:
			self.app_dni_frontal_completo = True

	@api.one
	def _compute_app_dni_posterior_completo(self):
		self.app_dni_posterior_completo = False
		if self.app_dni_posterior:
			self.app_dni_posterior_completo = True

	@api.one
	def _compute_app_banco_haberes(self):
		if self.app_banco_haberes_numero_entidad:
			bank_obj = self.pool.get('res.bank')
			bank_ids = bank_obj.search(self.env.cr, self.env.uid, [
				('code', '=', self.app_banco_haberes_numero_entidad)])
			if len(bank_ids) > 0:
				self.app_banco_haberes = bank_obj.browse(self.env.cr, self.env.uid, bank_ids[0]).name

	@api.one
	def _compute_app_selfie_completo(self):
		self.app_selfie_completo = False
		if self.app_selfie:
			self.app_selfie_completo = True

	@api.one
	def button_asignar_selfie_como_perfil(self):
		self.image = self.app_selfie

	@api.one
	def alerta_actualizar(self):
		self.alerta_ultima_actualizacion = datetime.now()
		# Datos de registro
		self.compute_alerta_ip_multiple_registros()
		self.compute_alerta_celular_multiple_partner()
		self.compute_alerta_celular_como_contacto()
		self.compute_alerta_domicilio_similar()
		# Datos de prestamos y cuotas
		self.compute_alerta_prestamos_activos()
		self.compute_alerta_prestamos_cobrados()
		self.compute_alerta_cuotas_activas()
		self.compute_alerta_cuotas_cobradas()
		self.compute_alerta_cuotas_normal()
		self.compute_alerta_cuotas_preventivas()
		self.compute_alerta_cuotas_mora_temprana()
		self.compute_alerta_cuotas_mora_media()
		self.compute_alerta_cuotas_mora_tardia()
		self.compute_alerta_cuotas_mora_incobrable()
		self.compute_alerta_fecha_ultimo_pago()
		# Datos compartidos
		self.compute_alerta_registrado_financieras()
		self.compute_alerta_prestamos_activos_financieras()
		self.compute_alerta_cuota_vencidas_financieras()
		self.compute_alerta_compromiso_mensual_financieras()
		self.compute_alerta_ip_no_confiable_financieras()

	@api.one
	def compute_alerta_ip_multiple_registros(self):
		if self.app_ip_registro:
			partner_obj = self.pool.get('res.partner')
			partner_ids = partner_obj.search(self.env.cr, self.env.uid, [
				('app_ip_registro', '=', self.app_ip_registro),
				('main_id_number', '!=', False),
				('main_id_number', '!=', self.main_id_number),
				('main_id_number', '!=', self.dni),
				'|', ('active', '=', True), ('active', '=', False),
				('company_id', '=', self.company_id.id)])
			self.alerta_ip_multiple_registros = len(partner_ids)
			self.alerta_ip_multiple_registros_ids = [(6, 0, partner_ids)]
	
	@api.one
	def button_app_ip_registro_no_confiable(self):
		self.app_ip_registro_no_confiable = True
		self.compute_alerta_ip_multiple_registros()
		for partner_id in self.alerta_ip_multiple_registros_ids:
			partner_id.app_ip_registro_no_confiable = True

	@api.one
	def button_app_ip_registro_confiable(self):
		self.app_ip_registro_no_confiable = False
		self.compute_alerta_ip_multiple_registros()
		for partner_id in self.alerta_ip_multiple_registros_ids:
			partner_id.app_ip_registro_no_confiable = False


	@api.one
	def button_app_estado_bloqueado(self):
		self.app_estado_bloqueado = True
		self.app_estado_portal = "Bloqueado por ip no confiable."

	@api.one
	def button_app_estado_no_bloqueado(self):
		self.app_estado_bloqueado = False
		self.app_estado_portal = ""

	@api.one
	def compute_alerta_celular_multiple_partner(self):
		if self.mobile and self.dni:
			partner_obj = self.pool.get('res.partner')
			partner_ids = partner_obj.search(self.env.cr, self.env.uid, [
				('mobile', '=', self.mobile),
				('id', '!=', self.id),
				('main_id_number', '!=', self.main_id_number),
				('main_id_number', '!=', self.dni),
				('company_id', '=', self.company_id.id)])
			self.alerta_celular_multiple_partner = len(partner_ids)
			self.alerta_celular_multiple_partner_ids = [(6, 0, partner_ids)]
	
	@api.one
	def compute_alerta_celular_como_contacto(self):
		if self.mobile and self.dni:
			contacto_obj = self.pool.get('res.partner.contacto')
			contacto_ids = contacto_obj.search(self.env.cr, self.env.uid, [
				'|', ('telefono', '=', self.mobile), ('movil', '=', self.mobile),
				('company_id', '=', self.company_id.id)])
			self.alerta_celular_como_contacto = len(contacto_ids)
			self.alerta_celular_como_contacto_ids = [(6, 0, contacto_ids)]

	@api.one
	def compute_alerta_domicilio_similar(self):
		if self.street and self.state_id and self.zip:
			street = self.street.split(" ")[0]
			partner_obj = self.pool.get('res.partner')
			partner_ids = partner_obj.search(self.env.cr, self.env.uid, [
				('street', '=ilike', street+'%'),
				('state_id', '=', self.state_id.id),
				('zip', '=', self.zip),
				('id', '!=', self.id),
				('main_id_number', '!=', self.main_id_number),
				('main_id_number', '!=', self.dni),
				('company_id', '=', self.company_id.id)])
			self.alerta_domicilio_similar = len(partner_ids)
			self.alerta_domicilio_similar_ids = [(6, 0, partner_ids)]

	@api.one
	def compute_alerta_prestamos_activos(self):
		if self.prestamo_ids:
			prestamo_obj = self.pool.get('financiera.prestamo')
			prestamo_ids = prestamo_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'acreditado'),
				('company_id', '=', self.company_id.id)])
			self.alerta_prestamos_activos = len(prestamo_ids)

	@api.one
	def compute_alerta_prestamos_cobrados(self):
		if self.prestamo_ids:
			prestamo_obj = self.pool.get('financiera.prestamo')
			prestamo_ids = prestamo_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'pagado'),
				('company_id', '=', self.company_id.id)])
			self.alerta_prestamos_cobrados = len(prestamo_ids)

	@api.one
	def compute_alerta_cuotas_activas(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_activas = len(cuota_ids)

	@api.one
	def compute_alerta_cuotas_cobradas(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				'|', ('state', '=', 'cobrada'), ('state', '=', 'precancelada'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_cobradas = len(cuota_ids)

	@api.one
	def compute_alerta_cuotas_normal(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'normal'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_normal = len(cuota_ids)

	@api.one
	def compute_alerta_cuotas_preventivas(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'preventiva'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_preventivas = len(cuota_ids)
	
	@api.one
	def compute_alerta_cuotas_mora_temprana(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'moraTemprana'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_temprana = len(cuota_ids)

	@api.one
	def compute_alerta_cuotas_mora_media(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'moraMedia'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_media = len(cuota_ids)
	
	@api.one
	def compute_alerta_cuotas_mora_tardia(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'moraTardia'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_tardia = len(cuota_ids)

	@api.one
	def compute_alerta_cuotas_mora_incobrable(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'incobrable'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_incobrable = len(cuota_ids)

	@api.one
	def compute_alerta_fecha_ultimo_pago(self):
		if self.cuota_ids:
			self.alerta_fecha_ultimo_pago = 'N/A'
			payment_obj = self.pool.get('account.payment')
			payment_ids = payment_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('payment_type', '=', 'inbound'),
				('state', 'in', ['posted','reconciled']),
				('company_id', '=', self.company_id.id)],
				order='payment_date desc')
			if len(payment_ids) > 0:
				ultimo_pago_id = payment_obj.browse(self.env.cr, self.env.uid, payment_ids[0])
				fecha_ultimo_pago = datetime.strptime(ultimo_pago_id.payment_date, '%Y-%m-%d')
				self.alerta_fecha_ultimo_pago = fecha_ultimo_pago.strftime('%d-%m-%Y')
				diferencia = datetime.now() - fecha_ultimo_pago
				self.alerta_dias_ultimo_pago = diferencia.days

	# Alertas compartidas
	@api.one
	def button_alerta_ver_y_compartir(self):
		self.alerta_ver_y_compartir = True

	@api.one
	def compute_alerta_registrado_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0:
			partner_obj = self.sudo().pool.get('res.partner')
			partner_ids = partner_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				'|', ('main_id_number', '=', self.main_id_number), ('main_id_number', '=', self.dni),
				('company_id', 'in', company_ids)])
			self.alerta_registrado_financieras = len(partner_ids)

	@api.one
	def compute_alerta_prestamos_activos_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0 and self.main_id_number:
			prestamo_obj = self.sudo().pool.get('financiera.prestamo')
			prestamo_ids = prestamo_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				'|', ('partner_id.main_id_number', '=', self.main_id_number), ('partner_id.main_id_number', '=', self.dni),
				('state', '=', 'acreditado'),
				('company_id', 'in', company_ids)])
			self.alerta_prestamos_activos_financieras = len(prestamo_ids)

	@api.one
	def compute_alerta_cuota_vencidas_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0 and self.main_id_number:
			cuota_obj = self.sudo().pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				'|', ('partner_id.main_id_number', '=', self.main_id_number), ('partner_id.main_id_number', '=', self.dni),
				('state', 'in', ['activa','judicial','incobrable']),
				('state_mora', 'in', ['moraTemprana','moraMedia','moraTardia','incobrable']),
				('company_id', 'in', company_ids)])
			self.alerta_cuotas_vencidas_financieras = len(cuota_ids)

	@api.one
	def compute_alerta_compromiso_mensual_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0 and self.main_id_number:
			partner_obj = self.sudo().pool.get('res.partner')
			partner_ids = partner_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				'|', ('main_id_number', '=', self.main_id_number), ('main_id_number', '=', self.dni),
				('cuota_ids.state', '=', 'activa'),
				('company_id', 'in', company_ids)])
			alerta_compromiso_mensual_financieras = 0
			for _id in partner_ids:
				partner_id = self.sudo().env['res.partner'].browse(_id)
				if partner_id.saldo > 0 and partner_id.capacidad_pago_mensual > 0:
					alerta_compromiso_mensual_financieras += partner_id.capacidad_pago_mensual-partner_id.capacidad_pago_mensual_disponible
			self.alerta_compromiso_mensual_financieras = alerta_compromiso_mensual_financieras
	
	@api.one
	def compute_alerta_ip_no_confiable_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0:
			partner_obj = self.sudo().pool.get('res.partner')
			partner_ids = partner_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				('app_ip_registro', '=', self.app_ip_registro),
				('app_ip_registro_no_confiable', '=', True),
				('company_id', 'in', company_ids)])
			company_alerta_ip_no_confiable = []
			for _id in partner_ids:
				partner_id = self.sudo().env['res.partner'].browse(_id)
				if partner_id.company_id.id not in company_alerta_ip_no_confiable:
					company_alerta_ip_no_confiable.append(partner_id.company_id.id)
			self.alerta_ip_no_confiable_financieras = len(company_alerta_ip_no_confiable)

	@api.one
	def _app_ver_y_compartir_riesgo_cliente(self):
		self.alerta_ver_y_compartir = self.company_id.app_id.app_ver_y_compartir_riesgo_cliente

class ExtendsResUser(models.Model):
	_name = 'res.users'
	_inherit = 'res.users'

	def user_report(self, rec_id, report_name):
		if rec_id and report_name:
			pdf = self.pool['report'].get_pdf(self._cr, self._uid, [rec_id], report_name, context=None)
			return base64.encodestring(pdf)