from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class CloseTicketWizard(models.TransientModel):
    _name = 'housemaid.close.ticket.wizard'
    _description = 'Close Ticket Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    @api.model
    def default_get(self, fields):
        res = super(CloseTicketWizard, self).default_get(fields)
        active_id = self._context.get('active_id')
        if active_id:
            ticket_rec = self.env['housemaid.tickets'].browse(int(active_id))
            res['tickets_id'] = ticket_rec.id
            res['type'] = ticket_rec.type
            res['new_sponsers_id'] = ticket_rec.new_sponsers_id
            res['old_sponsers_id'] = ticket_rec.old_sponsers_id
            res['maids_id'] = ticket_rec.maids_id
            res['user_id'] = ticket_rec.user_id
        return res

    issue_date = fields.Date(
        string='Date',
        required=True,
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
        readonly=True,
        tracking=True,
    )
    type = fields.Selection(
        string='Type',
        selection=[
            ('sales', 'Sales'),
            ('transfer', 'Transfer'),
            ('temp', 'Temporary'),
        ],
        readonly=True,
        tracking=True,
    )
    new_sponsers_id = fields.Many2one(
        comodel_name='housemaid.sponsers',
        string='New Sponsor',
        readonly=True,
        tracking=True,
    )
    old_sponsers_id = fields.Many2one(
        comodel_name='housemaid.sponsers',
        string='Old Sponsor',
        readonly=True,
        tracking=True,
    )
    maids_id = fields.Many2one(
        comodel_name='housemaid.maids',
        string='Maid',
        readonly=True,
        tracking=True,
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name='res.users',
        readonly=True,
        tracking=True,
    )
    description = fields.Text(
        string='Description',
        required=True,
        tracking=True,
    )

    def action_closed_ticket(self):
        self.ensure_one()
        vals = {
            'issue_date': date.today(),
            'closereason_id': self.closereason_id.id,
            'tickets_id': self.tickets_id.id,
            'type': self.type,
            'new_sponsers_id': self.new_sponsers_id.id,
            'old_sponsers_id': self.old_sponsers_id.id,
            'maids_id': self.maids_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
        }
        self.env['housemaid.closedtickets'].create(vals)
        
        # change ticket state
        active_id = self._context.get('tickets_id')
        record = self.env['housemaid.tickets'].browse(active_id)
        record.state = 'closed'
        record.activity_schedule(
            'ms_housemaid.mail_act_close',
            user_id=self.user_id.id,
            note=f'Please check ticket {record.code}; it was closed due to {self.closereason_id}'
        )
