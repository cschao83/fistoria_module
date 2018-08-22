# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_money_line(models.Model):
    _name = 'fi.money.line'
    _description = 'Money line'

    centralbank_id = fields.Many2one('fi.bank')
    money_type = fields.Many2one('fi.money.type',string='Money type')
    qty = fields.Integer('Quantity')



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
