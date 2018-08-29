# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_bankloan(models.Model):

    _name = 'fi.bankloan'
    _description = 'Bank Loan'


    centralbank_id = fields.Many2one('fi.bank')
    name = fields.Char('Loan Name')
    amount = fields.Float('Loan Amount')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
