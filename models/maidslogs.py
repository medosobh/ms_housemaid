from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64
from datetime import date, datetime, timedelta


class maidslogs(models.Model):
    _name = 'housemaid.maidslogs'
    _description = 'Maid Logs'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(
        string='Date',
        required=True,
        default=datetime.today(),
        tracking=True
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('open', 'Open to Work'),
            ('ready', 'Ready Inhouse'),
            ('valuated', '90 Days Valuation'),
            ('transfer', 'Sponser Trabsfer'),
            ('reserve', 'Reserved'),
            ('work', 'Working'),
            ('backout', 'Backout'),
        ],
        default='draft',
        tracking=True
    )
    visa_no = fields.Char(
        string='Visa No.',
        default=lambda self: _('new'),
        required=True,
        tracking=True
    )
    contract_no = fields.Char(
        string='Contract No.',
        default=lambda self: _('new'),
        required=True,
        tracking=True,
    )
    start_contract = fields.Date(
        string='Start Date',
        default=fields.Date.context_today,
        tracking=True,
    )
    end_contract = fields.Date(
        string='End Date',
        default=fields.Date.context_today,
        tracking=True,
    )
    maids_id = fields.Many2one(
        string='Maids',
        comodel_name='housemaid.maids',
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
