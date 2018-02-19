# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_payment_type(models.Model):

    _name='fi.payment.type'
    _description='Tipos de pagos'

    name = fields.Char(string='Name')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
