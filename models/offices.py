from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64


class offices(models.Model):

    _name = 'housemaid.offices'
    _description = 'Records of External Offices.'
    _rec_name = 'name'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one office!"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one office!"),
        ('partner_id_uniq', 'unique(partner_id)',
         "A parnter can only be assigned to one office!"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_image(self):
        image_path = get_module_resource(
            'ms_housemaid', 'static/img', 'office.png')
        return base64.b64encode(open(image_path, 'rb').read())

    code = fields.Char(
        string='Short Name',
        required=True,
        tracking=True
    )
    phone = fields.Char(
        string='Phone',
        required=True,
        tracking=True
    )
    name = fields.Char(
        string='Name',
        default=lambda self: _('New'),
        required=True,
        tracking=True
    )
    email = fields.Char(
        string='Email',
        required=True,
        default=lambda self: _('name@mail.com'),
        tracking=True
    )
    image_1920 = fields.Image(
        default=_default_image
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Office.",
        tracking=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        tracking=True
    )
    description = fields.Text(
        string='Description',
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True,
        tracking=True
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Operation Man",
        required=True,
        tracking=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
        ondelete='set null',
        help="Used to select the currency when billing.",
        tracking=True
    )
