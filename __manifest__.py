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
{
    'name': 'Website Kitchen Screen',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Kitchen Screen for Website Orders',
    'description': """
        Website Kitchen Screen allows restaurant staff to view and manage 
        orders from the website in real-time from the kitchen. This screen 
        provides a clear and organized display of all active orders, enabling 
        kitchen staff to prioritize and manage their tasks efficiently.
    """,
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': [
        'website_sale',
        'sale_management',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/kitchen_screen_sequence_data.xml',
        'views/sale_order_views.xml',
        'views/kitchen_screen_views.xml',
        'views/website_kitchen_screen_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'website_kitchen_screen/static/src/css/kitchen_screen.css',
            'website_kitchen_screen/static/src/js/kitchen_screen.js',
            'website_kitchen_screen/static/src/xml/kitchen_screen_templates.xml',
        ],
    },
    'images': [
        'static/description/banner.jpg',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
