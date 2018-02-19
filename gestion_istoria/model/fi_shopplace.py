# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_shopplace(models.Model):

    _name='fi.shopplace'
    _description='Puestos'

    name = fields.Char(string='Name')
    campaign_id = fields.Many2one('fi.campaign',string="Fiesta",required=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
