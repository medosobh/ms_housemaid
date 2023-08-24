from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class closedtickets(models.Model):
    _name = 'housemaid.closedtickets'
    _description = 'Closed Ticket'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    @api.depends('name', 'closereason_id', 'tickets_id')
    def name_get(self):
        result = []
        for record in self:
            if record.tickets_id:
                name = '[' + record.tickets_id + '] ' + record.closereason_id
            else:
                name = record.name
            result.append((record.id, name))
        return result
    
    name= fields.Char(
        string='Name',
        default=lambda self: _('New'),
        readonly=True,
        tracking=True,
    )
    issue_date = fields.Date(
        string='Issue Date',
        required=True,
        default=datetime.today(),
        tracking=True,
    )
    closereason_id = fields.Many2one(
        comodel_name='housemaid.closereason',
        string='Reason',
        required=True,
        tracking=True,
    )
    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        string='Ticket no.',
        required=True,
        tracking=True,
    )
    sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Current Sponser',
        required=True,
        tracking=True,
    )
    maids_id = fields.Many2one(
        comodel_name='housemaid.maids',
        string='Maid',
        required=True,
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
        required=True,
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
