# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):

    #herencia
    _inherit = 'res.partner'

    #nuevos atributos
    volunteer = fields.Boolean('Voluntario')
    artisan = fields.Boolean('Artesano')
    shopplaces = fields.One2many('fi.shopplace','partner_id',copy=True)
    dni = fields.Char('Dni')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
