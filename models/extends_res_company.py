# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)
class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	app_id = fields.Many2one('app.config', 'Configuracion Plataforma web y App Movil')
	fecha_actualizacion_alertas = fields.Datetime('Fecha ultima actualizacion de alertas')
	app_is_contracted = fields.Boolean('Esta contratado?')


	@api.model
	def _cron_actualizar_alerta_partners(self):
		company_obj = self.pool.get('res.company')
		comapny_ids = company_obj.search(self.env.cr, self.env.uid, [])
		for _id in comapny_ids:
			company_id = company_obj.browse(self.env.cr, self.env.uid, _id)
			print("company_id: ", str(company_id.name))
			if company_id.app_is_contracted:
				company_id._actualizar_alerta_partners()
				company_id.fecha_actualizacion_alertas = datetime.now()
		
	@api.model
	def _actualizar_alerta_partners(self):
		partner_obj = self.pool.get('res.partner')
		total = 0
		count = 0
		today = datetime.now()
		today_menos_10 = today - timedelta(days=+10)
		while True:
			partner_ids = partner_obj.search(self.env.cr, self.env.uid, [
				('active', '=', True),
				('company_id.id', '=', self.id),
				'|', ('cuota_ids.state', '=', 'activa'), ('alerta_prestamos_activos', '>', 0),
				'|', ('alerta_ultima_actualizacion', '=', False), ('alerta_ultima_actualizacion', '<', str(today)),
			], limit=200)
			print("partner_ids: ", partner_ids)
			# Buscamos partner que tengan cuotas con pagos en los ultimos 10 dias y sin cuotas activas
			partner_pagos_recientes_ids = partner_obj.search(self.env.cr, self.env.uid, [
				('active', '=', True),
				('company_id.id', '=', self.id),
				('cuota_ids.state', '!=', 'activa'),
				('cuota_ids.payment_ids.create_date', '>', str(today_menos_10)),
				'|', ('alerta_ultima_actualizacion', '=', False), ('alerta_ultima_actualizacion', '<', str(today)),
			], limit=200)
			print("partner_pagos_recientes_ids: ", partner_pagos_recientes_ids)
			# unir listas
			partner_ids = partner_ids + partner_pagos_recientes_ids
			if not partner_ids:
				break
			try:
				total += len(partner_ids)
				partner_obj_ids = partner_obj.browse(self.env.cr, self.env.uid, partner_ids)
				_logger.info('Init Actualizar alerta partners sobre prestamos y cuotas: %s', str(len(partner_ids)))
				for partner_id in partner_obj_ids:
					print("partner_id: ", partner_id)
					# partner_id = partner_obj.browse(self.env.cr, self.env.uid, _id)
					partner_id.alerta_actualizar()
					count += 1
					print("Actualizado / Total: ", count, total)
				partner_obj_ids.write({'alerta_ultima_actualizacion': today})
				self.env.cr.commit()
			except Exception as e:
				_logger.error('Error Actualizar alerta partners sobre prestamos y cuotas: %s', str(e))
				self.env.cr.rollback()
		_logger.info('Finish Actualizar alerta partners: %s partners actualizadas', count)
		self.fecha_actualizacion_alertas = today