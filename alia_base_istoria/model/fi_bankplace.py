# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_bankplace(models.Model):

    _inherits = {'fi.place': 'place_id'}
    _name = 'fi.bankplace'
    _description = 'Banks'


    @api.one
    @api.depends('operations')
    def _total_changed(self):
        total = 0.0
        for op in self.operations:
            if op.type in ['change']:
                total = total + op.maravedies_amount
        self.total_m_changed = total

    @api.one
    @api.depends('operations')
    def _total_returned(self):
        pass
        #for op in self.regular_operations:

    @api.one
    @api.depends('state')
    def action_close_bank(self):
        self.write({'state':'closed'})
        return True

    @api.one
    @api.depends('state')
    def action_open_bank(self):
        self.write({'state':'open'})
        return True


    place_id = fields.Many2one('fi.place', 'Place', required=True, ondelete="cascade", select=True, auto_join=True)
    responsible_id = fields.Many2one('res.partner',string = "Responsible", required=True)
    operations = fields.One2many('fi.bankoperation','origin_bank_id')
    bank_turns = fields.One2many('fi.bankturn','bankplace_id')
    total_m_changed = fields.Float(compute='_total_changed',string='Total Maravedies changed')
    total_e_returned = fields.Float(compute='_total_returned',string='Total Euros returned')
    type = fields.Selection([('central','Central'),('change','Change'),('return','Return'),('change-return','Change-Return')])
    state = fields.Selection([('draft','Draft'),('open','Open'),('closed','Closed')],default='draft')
    change_ratio = fields.Float(related='campaign_id.change_ratio')
    centralbank_id = fields.Many2one('fi.bank')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
