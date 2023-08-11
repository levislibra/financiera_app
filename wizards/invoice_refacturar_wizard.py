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
		# search invoices ids and order by document_number
		invoice_ids = self.env['account.invoice'].search([('id', 'in', active_ids)])
		tuple_invoice_ids = [(invoice_id, invoice_id.invoice_number) for invoice_id in invoice_ids]
		tuple_invoice_ids.sort(key=lambda x: x[1])
		print("tuple_invoice_ids: ", tuple_invoice_ids)
		for tuble_invoice_id in tuple_invoice_ids:
			invoice_id = tuble_invoice_id[0]
			print("invoice_id.invoice_number: ", invoice_id.invoice_number)
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
