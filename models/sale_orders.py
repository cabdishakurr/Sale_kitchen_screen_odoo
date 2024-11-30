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
        related='product_id.requires_cooking',
        string="Requires Cooking", 
        store=True,
        help='To identify if the order needs kitchen preparation')

    @api.depends('requires_cooking', 'kitchen_status')
    def _compute_display_name(self):
        for line in self:
            line.display_name = f"{line.product_id.name} ({line.kitchen_status})" if line.requires_cooking else line.product_id.name

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
        compute='_compute_requires_cooking',
        store=True,
        help='Indicates if this order needs kitchen preparation')
    kitchen_status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('waiting', 'Cooking'),
            ('ready', 'Ready'),
            ('cancel', 'Cancel')
        ],
        compute='_compute_kitchen_status',
        store=True,
        help='Kitchen preparation status')

    @api.depends('order_line.requires_cooking')
    def _compute_requires_cooking(self):
        for order in self:
            order.requires_cooking = any(line.requires_cooking for line in order.order_line)

    @api.depends('order_line.kitchen_status')
    def _compute_kitchen_status(self):
        for order in self:
            if not order.requires_cooking:
                order.kitchen_status = False
                continue
            
            statuses = order.order_line.filtered('requires_cooking').mapped('kitchen_status')
            if not statuses:
                order.kitchen_status = 'draft'
            elif all(status == 'ready' for status in statuses):
                order.kitchen_status = 'ready'
            elif all(status == 'cancel' for status in statuses):
                order.kitchen_status = 'cancel'
            else:
                order.kitchen_status = 'waiting' 