from odoo import models, fields, api

class WebsiteOrderLine(models.Model):
    """Order line model for website kitchen orders"""
    _inherit = "sale.order.line"
    _description = "Website Kitchen Order Line"

    kitchen_status = fields.Selection(
        selection=[('draft', 'Draft'), ('waiting', 'Cooking'),
                  ('ready', 'Ready'), ('cancel', 'Cancel')], 
        default='draft',
        help='The status of kitchen order')
    kitchen_ref = fields.Char(
        related='order_id.name',
        string='Order Reference',
        help='Order reference of website order')
    requires_cooking = fields.Boolean(
        string="Requires Cooking", 
        default=False,
        help='To identify if the order needs kitchen preparation')
    customer_id = fields.Many2one(
        'res.partner', 
        string="Customer",
        related='order_id.partner_id',
        help='Customer who placed the order')

    def get_kitchen_order_details(self, ids):
        """To get the product details for kitchen"""
        lines = self.env['sale.order'].browse(ids)
        res = []
        for rec in lines:
            res.append({
                'product_id': rec.product_id.id,
                'name': rec.product_id.name,
                'qty': rec.product_uom_qty
            })
        return res

    def kitchen_progress_change(self):
        """Change the kitchen order status"""
        if self.kitchen_status == 'ready':
            self.kitchen_status = 'waiting'
        else:
            self.kitchen_status = 'ready' 

class WebsiteOrder(models.Model):
    _inherit = 'sale.order'
    _description = "Website Kitchen Order"

    requires_cooking = fields.Boolean(
        string="Requires Kitchen Preparation",
        default=False,
        help='Indicates if this order needs kitchen preparation')
    kitchen_status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('waiting', 'Cooking'),
            ('ready', 'Ready'),
            ('cancel', 'Cancel')
        ],
        default='draft',
        help='Kitchen preparation status') 