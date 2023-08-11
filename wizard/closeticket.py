from odoo import api, fields, models, _
from odoo.exceptions import UserError


class closeticket(models.TransientModel):
    _name = 'housemaid.closeticket'
    _description = 'Close Ticket Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    closereason_id = fields.Many2one(
        comodel_name='housemaid.closereason',
        required=False,
        string='Reason',
    )
    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        required=False,
        string='Ticket no.',
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
        context = dict(self.env.context or {})
        user_id = context.get('user_id', False)
        tickets_id = context.get('tickets_id', False)
        # change ticket state
        record = self.env['housemaid.tickets'].browse(tickets_id)
        record.state = 'closed'
        record.activity_schedule(
            'ms_housemaid.mail_act_close',
            user_id=user_id,
            note=f'Please proceed hiring for {self.name} of the ticket {self.tickets_id.code}'
        )
        print('action_closed_ticket')
