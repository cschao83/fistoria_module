# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_shopplace(models.Model):

    _name='fi.shopplace'
    _description='Puestos'


    def _default_campaign(self):
        return self.env['fi.campaign'].search([('state','=','activa')])


    name = fields.Char(string='Nombre')
    artisan = fields.Boolean('Artesano')
    campaign_id = fields.Many2one('fi.campaign',string="Fiesta",required=True, default=_default_campaign)
    partner_id = fields.Many2one('res.partner',string="Propietario",required=True)
    notes = fields.Text("Notas Internas")
    state = fields.Selection([('activo','Activo'),('cerrado','Cerrado')],default='activo')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
