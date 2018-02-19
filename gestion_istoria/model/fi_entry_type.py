# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_entry_type(models.Model):

    _name='fi.entry.type'
    _description='Tipos de ingresos'

    name = fields.Char(string='Name')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
