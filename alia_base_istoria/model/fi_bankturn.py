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
    @api.depends
    def action_close_turn(self):
        self.write({'state':'closed'})
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
        toret = 0.0
        for op in self.bankoperations:
            if op.type in ['change']:
                toret = toret + op.maravedies_amount
        self.turn_total_m_changed = toret

    @api.one
    def _turn_total_returned(self):
        toret = 0.0
        for op in self.bankoperations:
            if op.type in ['return']:
                toret = toret + op.euros_amount
        self.turn_total_e_returned = toret

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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
