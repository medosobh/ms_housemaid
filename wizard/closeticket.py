from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class closeticket(models.TransientModel):
    _name = 'housemaid.closeticket'
    _description = 'Close Ticket Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    @api.model
    def default_get(self, fields):
        res = super(closeticket, self).default_get(fields)
        active_id = self._context.get('active_id')
        if active_id:
            ticket_rec = self.env['housemaid.tickets'].browse(int(active_id))
            res['tickets_id'] = ticket_rec.id
            res['type'] = ticket_rec.type
            res['sponsers_id'] = ticket_rec.sponsers_id
            res['maids_id'] = ticket_rec.maids_id
            res['user_id'] = ticket_rec.user_id
        return res

    closereason_id = fields.Many2one(
        comodel_name='housemaid.closereason',
        required=False,
        string='Reason',
    )
    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        required=True,
        string='Ticket no.',
    )
    type = fields.Selection(
        string='Type',
        selection=[
            ('sales', 'Sales'),
            ('transfer', 'Transfer'),
            ('temp', 'Temporary'),
        ],
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

    def action_closed_ticket(self):
        self.ensure_one()
        vals = {
            'issue_date': date.today(),
            'tickets_id': self.tickets_id.id,
            'type': self.type,
            'sponsers_id': self.sponsers_id.id,
            'maids_id': self.maids_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
        }
        self.env['housemaid.maidslogs'].self.create(vals)
        
        # change ticket state
        record = self.env['housemaid.tickets'].browse(tickets_id)
        record.state = 'closed'
        record.activity_schedule(
            'ms_housemaid.mail_act_close',
            user_id=self.user_id.id,
            note=f'Please check maid {record.maids_id.name} of the ticket {record.code}'
        )
        print('action_closed_ticket')
