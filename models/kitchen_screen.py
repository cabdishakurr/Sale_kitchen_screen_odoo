# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Gokul P I (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models


class WebsiteKitchenScreen(models.Model):
    """Kitchen Screen model for website orders"""
    _name = 'website.kitchen.screen'
    _description = 'Website Kitchen Screen'
    _rec_name = 'sequence'

    sequence = fields.Char(
        readonly=True, 
        default='New',
        copy=False, 
        tracking=True, 
        help="Sequence of items")
    website_id = fields.Many2one(
        'website',
        string='Website',
        help="Website this kitchen screen is associated with")
    product_categ_ids = fields.Many2many(
        'product.category',
        string='Product Categories',
        help="Product categories to show in this kitchen screen")
    
    @api.model
    def create(self, vals):
        """Generate sequence on creation"""
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'website.kitchen.screen') or 'New'
        return super(WebsiteKitchenScreen, self).create(vals)

    def get_website_orders(self):
        """Get relevant orders for this kitchen screen"""
        domain = [
            ('state', '=', 'sale'),  # Confirmed orders
            ('requires_cooking', '=', True),
            ('website_id', '=', self.website_id.id)
        ]
        return self.env['sale.order'].search(domain)
