from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64


class offices(models.Model):
    _name = 'housemaid.offices'
    _description = 'External Offices'
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

    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            if record.code:
                name = '[' + record.code + '] ' + record.name
            else:
                name = record.name
            result.append((record.id, name))
        return result

    code = fields.Char(
        string='Short Name',
        required=True,
        tracking=True
    )
    name = fields.Char(
        string='Name',
        default=lambda self: _('New'),
        required=True,
        tracking=True
    )
    phone = fields.Char(
        string='Phone',
        required=True,
        tracking=True
    )
    phone2 = fields.Char(
        string='Phone 2',
        required=False,
        tracking=True
    )
    phone3 = fields.Char(
        string='Phone 3',
        required=False,
        tracking=True
    )
    email = fields.Char(
        string='Email',
        required=True,
        default=lambda self: _('name@mail.com'),
        tracking=True
    )
    contact_person = fields.Char(
        string='Contact Person',
        required=True,
        tracking=True
    )
    address = fields.Text(
        string='Address',
        tracking=True,
    )
    image = fields.Image(
        default=_default_image,
        tracking=True,
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Office.",
        required=True,
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
        default=lambda self: self.env.user.id,
        required=True,
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
