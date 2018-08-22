# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_place(models.Model):

    _name = 'fi.place'
    _description = 'Base placement'


    def _default_campaign(self):
        return self.env['fi.campaign'].search([('state','=','activa')])

    name = fields.Char(string='Nombre')
    campaign_id = fields.Many2one('fi.campaign',string="Fiesta",required=True, default=_default_campaign)
    notes = fields.Text("Notas Internas")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
