# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time
import math

class InvoiceRefacturarlWizards(models.TransientModel):
	_name = 'invoice.refacturar.wizard'

	date_invoice = fields.Date('Fecha de factura')
	
	@api.one
	def refacturar(self):
		# obtenes los ids seleccionados
		context = dict(self._context or {})
		active_ids = context.get('active_ids')
		print("active_ids: ", active_ids)
		for _id in active_ids:
			invoice_id = self.env['account.invoice'].browse(_id)
			move_id = invoice_id.move_id
			move_id.button_cancel()
			invoice_id.move_id = None
			move_id.unlink()
			invoice_id.state = 'cancel'
			invoice_id.action_cancel_draft()
			invoice_id.date_invoice = self.date_invoice
			invoice_id.date_due = self.date_invoice
			# validar en afip
			invoice_id.validate_invoice()
