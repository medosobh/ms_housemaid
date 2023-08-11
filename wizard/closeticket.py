from odoo import api, fields, models, _
from odoo.exceptions import UserError


class closeticket(models.TransientModel):
    _name = 'housemaid.closeticket'
    _description = 'Close Ticket Wizard'

    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        required=False,
        string='Ticket no.',
    )
