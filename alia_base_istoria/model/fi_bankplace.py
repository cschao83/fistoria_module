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
        self.co_total_difference = total + self.co_total_e_paycard


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
    co_total_e_paycard = fields.Float('Total euros by paycard (cashing out)')

    #rt operations
    total_m_changed = fields.Float(compute='_total_changed',string='Total Maravedies changed')
    total_e_returned = fields.Float(compute='_total_returned',string='Total Euros returned')



class fi_return_bankplace(models.Model):

    _inherits = {'fi.bankplace': 'bankplace_id'}
    _name = 'fi.return.bankplace'
    _description = 'Return Banks'

    @api.one
    @api.depends('state')
    def action_open_bank(self):
        self.write({'state':'open'})
        return True

    @api.one
    @api.depends('state')
    def action_close_bank(self):
        self.co_total_difference = self.total_received_euros - self.co_total_e_got
        self.write({'state':'closed'})
        vals = {}
        vals['type'] = 'receive'
        vals['turn_id'] = self.id
        vals['centralbank_id'] = self.bankplace_id.centralbank_id.id
        vals['origin_bank_id'] = self.bankplace_id.id
        vals['maravedies_amount'] = 0.0
        vals['euros_amount'] = self.co_total_e_got
        self.env['fi.bankoperation'].create(vals)
        return True

    @api.one
    def _get_total_received_euros(self):
        total = 0.00
        for op in self.operations:
            if op.type in ['send'] and op.origin_bank_id == self.bankplace_id:
                total = total + op.euros_amount
        self.total_received_euros = total


    bankplace_id = fields.Many2one('fi.bankplace', 'Bankplace', required=True, ondelete="cascade", select=True, auto_join=True)
    total_received_euros = fields.Float('Total euros received',compute='_get_total_received_euros')
    co_total_e_got = fields.Float('Total euros obtained (cashing out)')
    co_total_difference = fields.Float('Total euros difference (cashing out)')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
