# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_money_type(models.Model):

    _name='fi.money.type'
    _description='Tipos de billetes'

    name = fields.Char(string='Name',required=True)
    value = fields.Float(string='Value',required=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
