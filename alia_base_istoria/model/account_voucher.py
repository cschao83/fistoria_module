# -*- coding: utf-8 -*-

from openerp import models, fields, api

class account_voucher(models.Model):

    #herencia
    _inherit = 'account.voucher'


    def _default_central_bank(self):
        if 'centralbank_id' in self._context.keys():
            return self.env['fi.bank'].browse(self._context['centralbank_id'])
        return False

    #
    centralbank_id = fields.Many2one('fi.bank',default=_default_central_bank)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
