from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64
from datetime import date, datetime, timedelta


class maidscontracts(models.Model):
    _name = 'housemaid.maidscontracts'
    _description = 'Contracts'
    _rec_name = 'contract_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.depends('name', 'contract_no', 'maids_id')
    def name_get(self):
        result = []
        for record in self:
            if record.tickets_id:
                name = '[' + record.contract_no + '] ' + record.maids_id
            else:
                name = record.name
            result.append((record.id, name))
        return result

    name = fields.Char(
        string='Name',
        default=lambda self: _('New'),
        readonly=True,
        tracking=True,
    )
    issue_date = fields.Date(
        string='Issue Date',
        required=True,
        default=datetime.today(),
        tracking=True
    )
    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        string='Ticket no.',
        required=True,
        tracking=True,
    )
    type = fields.Selection(
        string='Type',
        selection=[
            ('sales', 'Sales'),
            ('transfer', 'Transfer'),
            ('temp', 'Temporary'),
        ],
        required=False,
        tracking=True,
    )
    new_sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='New Sponser',
        required=False,
        tracking=True,
    )
    old_sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='old Sponser',
        required=True,
        tracking=True,
    )
    maids_id = fields.Many2one(
        string='Maids',
        comodel_name='housemaid.maids',
        required=True,
        tracking=True,
    )
    offices_id = fields.Many2one(
        'housemaid.offices',
        string='Offices',
        required=True,
        tracking=True,
    )
    contract_no = fields.Char(
        string='Contract No.',
        required=True,
        tracking=True,
    )
    start_contract = fields.Date(
        string='Start Date',
        required=True,
        tracking=True,
    )
    end_contract = fields.Date(
        string='End Date',
        required=True,
        tracking=True,
    )
    visa_no = fields.Char(
        string='Visa No.',
        required=True,
        tracking=True
    )
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        tracking=True,
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Maid.",
        required=False,
        tracking=True,
    )
    user_id = fields.Many2one(
        string="Responsable",
        comodel_name='res.users',
        required=True,
        tracking=True,
    )
    description = fields.Text(
        string='Description',
        required=False,
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
