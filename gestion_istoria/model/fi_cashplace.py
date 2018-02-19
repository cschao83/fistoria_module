# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_cashplace(models.Model):

    _name='fi.cashplace'
    _description='Cajas'

    name = fields.Char(string='Name')
    campaign_id = fields.Many2one('fi.campaign',string="Fiesta",required=True)
    state = fields.Selection([('activo','Activo'),('cerrado','Cerrado')],default='activo')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
