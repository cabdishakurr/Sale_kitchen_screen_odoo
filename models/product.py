from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    requires_cooking = fields.Boolean(
        string='Requires Cooking',
        help='Check this if the product needs to be prepared in the kitchen') 