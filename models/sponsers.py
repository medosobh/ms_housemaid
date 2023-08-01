from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64


class sponsers(models.Model):

    _name = 'housemaid.sponsers'
    _description = 'Records of Sponsers.'
    _rec_name = 'phone'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one Sponser!"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one Sponser!"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_image(self):
        image_path = get_module_resource(
            'ms_housemaid', 'static/img', 'sponser.png')
        return base64.b64encode(open(image_path, 'rb').read())

    code = fields.Char(
        string='Code',
        required=True,
        tracking=True
    )
    phone = fields.Char(
        string='Phone',
        required=True,
        index=True,
        tracking=True
    )
    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        tracking=True
    )
    email = fields.Char(
        string='email',
        required=True,
        default=lambda self: _('name@mail.com'),
        tracking=True
    )
    image_1920 = fields.Image(
        default=_default_image
    )
    address = fields.Text(
        string='Address',
        required=False,
        tracking=True
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Sponser.",
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
        help="Used to display the currency when tracking monetary values",
        tracking=True
    )
