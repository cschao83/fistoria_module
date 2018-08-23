# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_bank(models.Model):

    _name = 'fi.bank'
    _description = 'Bank'


    def _get_total_maravedies_provided(self):
        total = 0.0
        for line in self.total_new_money:
            total = total + line.money_type.value * line.qty
        self.amount_maravedies_provided = total


    def _get_amount_available_maravedies(self):
        total = self.amount_maravedies_provided - self.amount_maravedies_for_shops
        for op in self.operations:
            if op.type in ['send']:
                total = total - op.maravedies_amount
            if op.type in ['receive']:
                total = total + op.maravedies_amount
        self.amount_maravedies_for_banking = total


    def _get_amount_available_euros(self):
        total = 0.0
        for op in self.operations:
            if op.type in ['send']:
                total = total - op.euros_amount
            if op.type in ['receive']:
                total = total + op.euros_amount
        self.amount_euros_for_banking = total


    def _get_maravedies_reserved(self):
        total = 0.0
        for op in self.operations:
            if op.type in ['reserve']:
                total = total + op.maravedies_amount
        self.amount_maravedies_for_shops = total


    def _get_total_maravedies_changed_by_operations(self):
        total = 0.0
        for bankplace in self.cashplaces:
            total = total + bankplace.total_m_changed
        self.total_maravedies_changed = total


    def _get_total_maravedies_changed_by_cashing_out(self):
        total = 0.0
        for bankplace in self.cashplaces:
            total = total + bankplace.total_m_changed
        self.total_maravedies_changed = total


    def _get_total_payments(self):
        total = 0.0
        for v in self.vouchers_payment:
            total = total + v.amount
        self.total_payments = total


    def _get_total_entries(self):
        total = 0.0
        for v in self.vouchers_entry:
            total = total + v.amount
        self.total_entries = total


    def _get_vouchers_payment(self):
        vouchers = self.env['account.voucher'].search([('type','=','payment'),('centralbank_id','=',self.id)])
        self.vouchers_payment = vouchers


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
    def action_receive_maravedies_from_turn(self):
        view = self.env.ref('alia_base_istoria.new_central_bank_receive_m_operation_popup_form')
        dict = {
            'name':'Recibo de Maravedies de un turno',
            'res_model': 'fi.bankoperation',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target':'new',
            'flags': {'form': {'action_buttons': True}},
            'context': {'centralbank_id':self.id,'type':'receive'},
        }

        return dict
    
    @api.multi
    def action_receive_euros_from_turn(self):
        view = self.env.ref('alia_base_istoria.new_central_bank_receive_e_operation_popup_form')
        dict = {
            'name':'Recibo de Euros de un turno',
            'res_model': 'fi.bankoperation',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target':'new',
            'flags': {'form': {'action_buttons': True}},
            'context': {'centralbank_id':self.id,'type':'receive'},
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


    name = fields.Char('Name')
    campaign_id = fields.Many2one('fi.campaign',string='Campaign')
    total_new_money = fields.One2many('fi.money.line','centralbank_id')
    amount_maravedies_provided = fields.Float('Total maravedies provided',compute='_get_total_maravedies_provided')
    amount_maravedies_for_shops = fields.Float('Amount maravedies for shops',compute='_get_maravedies_reserved')
    amount_maravedies_for_banking = fields.Float(compute='_get_amount_available_maravedies',string="Amount maravedies in Central Bank")
    amount_euros_for_banking = fields.Float(compute='_get_amount_available_euros',string="Amount euros in Central Bank")
    total_maravedies_changed = fields.Float('Total maravedies changed (Real Time)',compute='_get_total_maravedies_changed_by_operations')
    total_maravedies_changed_fixed = fields.Float('Total maravedies changed (Cashing out)',compute='_get_total_maravedies_changed_by_cashing_out')
    cashplaces = fields.One2many('fi.bankplace','centralbank_id')
    operations = fields.One2many('fi.bankoperation','centralbank_id')
    vouchers_payment = fields.One2many('account.voucher','centralbank_id',compute='_get_vouchers_payment')
    vouchers_entry = fields.One2many('account.voucher','centralbank_id',compute='_get_vouchers_entry')
    total_entries = fields.Float('Total entries',compute='_get_total_entries')
    total_payments = fields.Float('Total payments',compute='_get_total_payments')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: