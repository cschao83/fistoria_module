# -*- coding: utf-8 -*-
####################################
#
#    Created on 28 de octubre de 2017
#
#    @author:castor
#
##############################################################################
#
# 2016 ALIA Technologies
#       http://www.alialabs.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError
import logging
_logger = logging.getLogger(__name__)



class fi_campaign(models.Model):

    _name = 'fi.campaign'
    _description = 'Campaign'


    name = fields.Char("Name",required=True)
    event_date = fields.Date("Date",required=True)
    centralbank_id = fields.Many2one('fi.bank',string='Bank')
    shopplaces = fields.One2many('fi.shopplace','campaign_id',copy=True)
    total_shops = fields.Integer("Total shops")
    total_artisans = fields.Integer("Total artisans")
    amount_maravedies_changed = fields.Float("Total changed (Maravedies)",related='centralbank_id.total_maravedies_changed')
    amount_founding = fields.Float("Total profits (€)")
    amount_payments = fields.Float("Total paid (€)")
    amount_profits = fields.Float("Total profits (€)")
    change_ratio = fields.Float("Change ratio (%)",required=True)
    total_new_money_amount = fields.Float(related='centralbank_id.amount_maravedies_provided',string='Total new money supplied')
    notes = fields.Text("Internal notes")
    state = fields.Selection([('borrador','Borrador'),('activa','Activa'),('cerrada','Cerrada')],default='borrador')


    @api.multi
    @api.depends('state')
    def action_active_campaign(self):
        if self.search_count([('state','=','activa')]) > 0:
            raise ValidationError("An active campaign already exists!")
        else:
            self.write({'state':'activa'})
            return True


    @api.multi
    @api.depends('sales_forecasts')
    def action_close_campaign(self):
        self.write({'state':'cerrada'})
        return True

       
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
