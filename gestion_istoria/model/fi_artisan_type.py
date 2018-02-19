# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_artisan_type(models.Model):

    _name='fi.artisan.type'
    _description='Tipos de artesanos'

    name = fields.Char(string='Name')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
