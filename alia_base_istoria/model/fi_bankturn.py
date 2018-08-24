# -*- coding: utf-8 -*-

from openerp import models, fields, api


class fi_bankturn(models.Model):

    _name = 'fi.bankturn'
    _description = 'Bank Turn'

    @api.one
    @api.depends('bankoperations','bankplace_id')
    def action_change_ten(self):
        vals = {}
        vals['type'] = 'change'
        vals['turn_id'] = self.id
        vals['origin_bank_id'] = self.bankplace_id.id
        vals['maravedies_amount'] = 10.0 * self.bankplace_id.change_ratio
        vals['euros_amount'] = 10.0
        self.env['fi.bankoperation'].create(vals)

    @api.one
    @api.depends('bankoperations','bankplace_id')
    def action_change_twenty(self):
        vals = {}
        vals['type'] = 'change'
        vals['turn_id'] = self.id
        vals['centralbank_id'] = self.bankplace_id.centralbank_id.id
        vals['origin_bank_id'] = self.bankplace_id.id
        vals['maravedies_amount'] = 20.0 * self.bankplace_id.change_ratio
        vals['euros_amount'] = 20.0
        self.env['fi.bankoperation'].create(vals)

    @api.one
    @api.depends('bankoperations','bankplace_id')
    def action_change_fifty(self):
        vals = {}
        vals['type'] = 'change'
        vals['turn_id'] = self.id
        vals['centralbank_id'] = self.bankplace_id.centralbank_id.id
        vals['origin_bank_id'] = self.bankplace_id.id
        vals['maravedies_amount'] = 50.0 * self.bankplace_id.change_ratio
        vals['euros_amount'] = 50.0
        self.env['fi.bankoperation'].create(vals)

    @api.one
    @api.depends('state')
    def action_active_turn(self):
        self.write({'state':'active'})
        return True

    @api.one
    @api.depends('state')
    def action_close_turn(self):
        #calculate cashing out
        self.co_total_m_changed = self.co_total_m_received - self.co_total_m_remains
        self.co_estimated_euros = (self.co_total_m_changed * 10)/9
        self.co_euros_difference = self.co_estimated_euros - self.co_total_e_got
        self.write({'state':'closed'})
        vals = {}
        vals['type'] = 'receive'
        vals['turn_id'] = self.id
        vals['centralbank_id'] = self.bankplace_id.centralbank_id.id
        vals['origin_bank_id'] = self.bankplace_id.id
        vals['maravedies_amount'] = self.co_total_m_remains
        vals['euros_amount'] = self.co_total_e_got
        self.env['fi.bankoperation'].create(vals)
        return True


    @api.one
    def _maravedies_remains(self):
        toret = 0.00
        for op in self.bankoperations:
            if op.type in ['return','send'] and op.turn_id.id == self.id:
                toret = toret + op.maravedies_amount
            if op.type in ['receive'] and op.turn_id.id == self.id:
                toret = toret - op.maravedies_amount
        self.maravedies_remains = toret - self.turn_total_m_changed

    @api.one
    def _euros_remains(self):
        toret = 0.00
        for op in self.bankoperations:
            if op.type in ['change','send'] and op.turn_id.id == self.id:
                toret = toret + op.euros_amount
            if op.type in ['receive'] and op.turn_id.id == self.id:
                toret = toret - op.euros_amount
        self.euros_remains = toret - self.turn_total_e_returned


    @api.one
    def _turn_total_changed(self):
        toret = 0.00
        for op in self.bankoperations:
            if op.type in ['change']:
                toret = toret + op.maravedies_amount
        self.turn_total_m_changed = toret

    @api.one
    def _turn_total_returned(self):
        toret = 0.00
        for op in self.bankoperations:
            if op.type in ['return']:
                toret = toret + op.euros_amount
        self.turn_total_e_returned = toret

    @api.one
    def _co_get_total_maravedies_received(self):
        toret = 0.00
        for op in self.bankoperations:
            if op.type in ['send'] and op.turn_id.id == self.id:
                toret = toret + op.maravedies_amount
        self.co_total_m_received = toret


    name = fields.Char('Turn name',required=True)
    time_init = fields.Datetime('Time init')
    time_finish = fields.Datetime('Time finish')
    bankoperators = fields.Many2many('res.partner','turn_partner_rel','turn_id','partner_id',string='Bank operators')
    bankplace_id = fields.Many2one('fi.bankplace',required=True)
    turn_total_m_changed = fields.Float(compute='_turn_total_changed',string='Total Maravedies changed')
    turn_total_e_returned = fields.Float(compute='_turn_total_returned',string='Total Euros returned')
    maravedies_remains = fields.Float(string='Maravedies remains',compute='_maravedies_remains')
    euros_remains = fields.Float(string='Euros remains',compute='_euros_remains')
    bankoperations = fields.One2many('fi.bankoperation','turn_id')
    campaign_id = fields.Many2one(related='bankplace_id.campaign_id')
    notes = fields.Text()
    state = fields.Selection([('draft','Draft'),('active','Active'),('closed','Closed')],default='draft')

    #cashing out attributes for change
    co_total_m_received = fields.Float('Maravedies received',compute='_co_get_total_maravedies_received')
    co_total_m_remains = fields.Float('Total Maravedies remained (cashing out)')
    co_total_m_changed = fields.Float('Total Maravedies changed (cashing out)')
    co_estimated_euros = fields.Float('Estimated euros')
    co_total_e_got = fields.Float('Total euros obtained (cashing out)')
    co_euros_difference = fields.Float('Total euros difference')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
