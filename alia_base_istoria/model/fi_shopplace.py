# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_shopplace(models.Model):

    _inherits = {'fi.place': 'place_id'}
    _name = 'fi.shopplace'
    _description = 'Shops'



    @api.multi
    def action_reserve_place(self):
        pass
    
    
    @api.multi
    def action_activate_place(self):
        pass
    

    place_id = fields.Many2one('fi.place', 'Place', required=True, ondelete="cascade", select=True, auto_join=True)
    partner_id = fields.Many2one('res.partner',string = "Owner", required=True)
    type = fields.Selection([('artisan','Artisan'),('fixed','Fixed'),('draw','Draw')])
    guaranty = fields.Float('Guaranty (€)')
    m_cash_asigned = fields.Float('Cash assigned (Maravedies)')
    state = fields.Selection([('draft','Draft'),('reserved','Reserved'),('active','Active'),('closed','Closed')],default='draft')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
