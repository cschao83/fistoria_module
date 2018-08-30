# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_bank(models.Model):

    _name = 'fi.bank'
    _description = 'Bank'

    @api.one
    def _get_total_maravedies_provided(self):
        total = 0.0
        for line in self.total_new_money:
            total = total + line.money_type.value * line.qty
        self.amount_maravedies_provided = total

    @api.one
    def _get_amount_available_maravedies(self):
        total = self.amount_maravedies_provided - self.amount_maravedies_for_shops
        for op in self.operations:
            if op.type in ['send']:
                total = total - op.maravedies_amount
            if op.type in ['receive']:
                total = total + op.maravedies_amount
        self.amount_maravedies_for_banking = total

    @api.one
    def _get_amount_available_euros(self):
        total = 0.0
        for op in self.operations:
            if op.type in ['send']:
                total = total - op.euros_amount
            if op.type in ['receive']:
                total = total + op.euros_amount
        total = total + self.vouchers_balance
        self.amount_euros_cash_euros_results = total + self.total_loans

    @api.one
    def _get_maravedies_reserved(self):
        total = 0.0
        for op in self.operations:
            if op.type in ['reserve']:
                total = total + op.maravedies_amount
        self.amount_maravedies_for_shops = total

    @api.one
    def _get_total_maravedies_changed_by_operations(self):
        total = 0.0
        for bankplace in self.cashplaces:
            total = total + bankplace.total_m_changed
        self.total_maravedies_changed = total

    @api.one
    def _get_total_payments(self):
        total = 0.0
        for v in self.vouchers_payment:
            total = total + v.amount
        self.total_payments = total

    @api.one
    def _get_total_entries(self):
        total = 0.0
        for v in self.vouchers_entry:
            total = total + v.amount
        self.total_entries = total

    @api.one
    def _get_vouchers_balance(self):
        self.vouchers_balance = self.total_entries - self.total_payments

    @api.one
    def _get_vouchers_payment(self):
        vouchers = self.env['account.voucher'].search([('type','=','payment'),('centralbank_id','=',self.id)])
        self.vouchers_payment = vouchers

    @api.one
    def _get_vouchers_entry(self):
        vouchers = self.env['account.voucher'].search([('type','=','receipt'),('centralbank_id','=',self.id)])
        self.vouchers_entry = vouchers


    @api.multi
    def action_reserve_maravedies_to_shops(self):
        view = self.env.ref('alia_base_istoria.new_central_bank_reserve_operation_popup_form')
        dict = {
            'name':'Reserva de Maravedies para Puestos',
            'res_model': 'fi.bankoperation',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target':'new',
            'flags': {'form': {'action_buttons': True}},
            'context': {'centralbank_id':self.id,'type':'reserve'},
        }

        return dict


    @api.multi
    def action_send_maravedies_to_turn(self):
        view = self.env.ref('alia_base_istoria.new_central_bank_send_m_operation_popup_form')
        dict = {
            'name':'Envío de Maravedies a un turno',
            'res_model': 'fi.bankoperation',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target':'new',
            'flags': {'form': {'action_buttons': True}},
            'context': {'centralbank_id':self.id,'type':'send'},
        }

        return dict


    @api.multi
    def action_send_euros_to_turn(self):
        view = self.env.ref('alia_base_istoria.new_central_bank_send_e_operation_popup_form')
        dict = {
            'name':'Envío de Euros de un turno',
            'res_model': 'fi.bankoperation',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target':'new',
            'flags': {'form': {'action_buttons': True}},
            'context': {'centralbank_id':self.id,'type':'send'},
        }

        return dict


    @api.multi
    def action_register_payment(self):
        view = self.env.ref('alia_base_istoria.view_vendor_payment_form_inherit')
        dict = {
            'name':'Registro de un pago',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target':'new',
            'flags': {'form': {'action_buttons': True}},
            'context': {'centralbank_id':self.id,'type':'payment'},
        }

        return dict


    @api.multi
    def action_register_entry(self):
        view = self.env.ref('alia_base_istoria.view_vendor_receipt_form_inherit')
        print self.id
        dict = {
            'name':'Registro de un cobro',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target':'new',
            'flags': {'form': {'action_buttons': True}},
            'context': {'centralbank_id':self.id,'type':'receipt'},
        }

        return dict


    @api.one
    @api.depends('cashplaces')
    def _co_get_total_m_changed(self):
        total = 0.0
        for c in self.cashplaces:
            total = total + c.co_total_m_changed
        self.co_total_m_changed = total

    @api.one
    @api.depends('cashplaces')
    def _co_get_total_e_obtained(self):
        total = 0.0
        for c in self.cashplaces:
            total = total + c.co_total_e_got + c.co_total_e_paycard
        self.co_total_e_got = total

    @api.one
    @api.depends('cashplaces')
    def _co_get_total_e_obtained_without_paycard(self):
        total = 0.0
        for c in self.cashplaces:
            total = total + c.co_total_e_got
        self.co_total_e_cash_got = total

    @api.one
    @api.depends('return_cashplaces')
    def _co_get_total_e_returned(self):
        total = 0.0
        for c in self.return_cashplaces:
            total = total + c.co_total_difference
        self.co_total_e_returned = total

    @api.one
    def _co_get_total_e_not_returned(self):
        self.co_total_e_not_returned = (self.co_total_e_got * 0.9) - self.co_total_e_returned

    @api.one
    def _get_bank_benefit(self):
        benefit = self.co_total_e_got * 0.1
        benefit = benefit + self.co_total_e_not_returned
        self.bank_benefit = benefit

    @api.one
    def _co_get_lost_and_mistakes(self):
        total = 0.0
        for c in self.cashplaces:
            total += c.co_euros_difference
        self.co_total_e_lost = total

    @api.one
    def _get_total_loans(self):
        total = 0.0
        for l in self.bankloans:
            total += l.amount
        self.total_loans = total

    name = fields.Char('Name')
    campaign_id = fields.Many2one('fi.campaign',string='Campaign')
    total_new_money = fields.One2many('fi.money.line','centralbank_id')
    amount_maravedies_provided = fields.Float('Total maravedies provided',compute='_get_total_maravedies_provided')
    amount_maravedies_for_shops = fields.Float('Amount maravedies for shops',compute='_get_maravedies_reserved')
    amount_maravedies_for_banking = fields.Float(compute='_get_amount_available_maravedies',string="Amount maravedies in Central Bank")
    amount_euros_cash_euros_results = fields.Float(compute='_get_amount_available_euros',string="Amount cash euros in Central Bank")
    total_maravedies_changed = fields.Float('Total maravedies changed (Real Time)',compute='_get_total_maravedies_changed_by_operations')
    cashplaces = fields.One2many('fi.bankplace','centralbank_id')
    return_cashplaces = fields.One2many('fi.return.bankplace','centralbank_id')
    operations = fields.One2many('fi.bankoperation','centralbank_id')
    bankloans = fields.One2many('fi.bankloan','centralbank_id')
    total_loans = fields.Float('Total initial loans',compute='_get_total_loans')
    vouchers_payment = fields.One2many('account.voucher','centralbank_id',compute='_get_vouchers_payment')
    vouchers_entry = fields.One2many('account.voucher','centralbank_id',compute='_get_vouchers_entry')
    total_entries = fields.Float('Total entries',compute='_get_total_entries')
    total_payments = fields.Float('Total payments',compute='_get_total_payments')
    vouchers_balance = fields.Float('Vouchers Balance',compute='_get_vouchers_balance')
    bank_benefit = fields.Float('Bank Benefit',compute='_get_bank_benefit')
    bank_conclusions = fields.Text('Bank conclusions')

    #cashing out
    co_total_e_lost = fields.Float('Lost or Mistakes (€)',compute='_co_get_lost_and_mistakes')
    co_total_m_changed = fields.Float('Total Maravedies changed (cashing out)',compute='_co_get_total_m_changed')
    co_total_e_cash_got = fields.Float('Total euros obtained in cash (cashing out)',compute='_co_get_total_e_obtained_without_paycard')
    co_total_e_got = fields.Float('Total euros obtained adding paycard (cashing out)',compute='_co_get_total_e_obtained')
    co_total_e_returned = fields.Float('Total euros returned (cashing out)',compute='_co_get_total_e_returned')
    co_total_e_not_returned = fields.Float('Total euros not returned',compute='_co_get_total_e_not_returned')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
