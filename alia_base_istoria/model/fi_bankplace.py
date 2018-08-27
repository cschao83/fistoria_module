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

    @api.one
    def _co_get_total_maravedies_changed(self):
        total = 0.00
        for t in self.bank_turns:
            if t.state in ['closed']:
                total = total + t.co_total_m_changed
        self.co_total_m_changed = total

    @api.one
    def _co_get_total_euros_obtained(self):
        total = 0.00
        for t in self.bank_turns:
            if t.state in ['closed']:
                total = total + t.co_total_e_got
        self.co_total_e_got = total

    @api.one
    def _co_get_total_difference(self):
        total = 0.00
        for t in self.bank_turns:
            if t.state in ['closed']:
                total = total + t.co_euros_difference
        self.co_total_difference = total


    place_id = fields.Many2one('fi.place', 'Place', required=True, ondelete="cascade", select=True, auto_join=True)
    responsible_id = fields.Many2one('res.partner',string = "Responsible", required=True)
    operations = fields.One2many('fi.bankoperation','origin_bank_id')
    bank_turns = fields.One2many('fi.bankturn','bankplace_id')

    type = fields.Selection([('cr2010','Quick Change 20 and 10'),('cr20','Quick Change 20'),('cr50','Quick Change 50'),('return','Return'),('mixed','Mixed Change')])
    state = fields.Selection([('draft','Draft'),('open','Open'),('closed','Closed')],default='draft')
    change_ratio = fields.Float(related='campaign_id.change_ratio')
    centralbank_id = fields.Many2one('fi.bank')

    #cashing out
    co_total_m_changed = fields.Float('Total Maravedies changed (cashing out)',compute='_co_get_total_maravedies_changed')
    co_total_e_got = fields.Float('Total euros obtained (cashing out)',compute='_co_get_total_euros_obtained')
    co_total_difference = fields.Float('Total euros difference (cashing out)',compute='_co_get_total_difference')


    #rt operations
    total_m_changed = fields.Float(compute='_total_changed',string='Total Maravedies changed')
    total_e_returned = fields.Float(compute='_total_returned',string='Total Euros returned')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
