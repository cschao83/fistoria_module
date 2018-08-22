# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fi_bankoperation(models.Model):

    _name = 'fi.bankoperation'
    _description = 'Bank Operation'


    def _default_type(self):
        if 'type' in self._context.keys():
            return self._context['type']
        return False

    def _default_central_bank(self):
        if 'centralbank_id' in self._context.keys():
            return self.env['fi.bank'].browse(self._context['centralbank_id'])
        return False


    type = fields.Selection([('change','Change to client'),('return','Return to client'),('send','Send from CBank'),
                             ('receive','Received in CBank'),('reserve','Reserve for Shops'),('payment','Payment'),('entry','Entry')],default=_default_type)
    centralbank_id = fields.Many2one('fi.bank',string='Central Bank',default=_default_central_bank)
    turn_id = fields.Many2one('fi.bankturn',string='Bank operator')
    origin_bank_id = fields.Many2one('fi.bankplace',string='Origin Bank')
    maravedies_amount = fields.Float('Maravedies amount')
    euros_amount = fields.Float('Euros amount')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
