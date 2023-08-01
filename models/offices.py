from odoo import fields, models, _
from odoo.exceptions import UserError


class office(models.Model):

    _name = 'housemaid.office'
    _description = 'a table of offices linked to office parnter'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one equipment !"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one equipment !"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields(
        string='Short Name',
        default=lambda self: _('New'),
        required=True,
        tracking=True
    )
    name = fields.Char(
        string='Name',
        default=lambda self: _('New'),
        required=True,
        tracking=True
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
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
