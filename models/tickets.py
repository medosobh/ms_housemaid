from odoo import fields, models, _
from odoo.exceptions import UserError

class ticket(models.Model):
    _name = 'housemaid.ticket'
    _description = 'Ticket request for sales team and the operation tickets also for both search or hiring'
    _rec_name = 'code'
    _order = 'name ASC'
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one equipment !"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    code = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )
    company_id = fields.Many2one(
        comodel_name = 'res.company',
        string = 'Company',
        change_default = True,
        default = lambda self: self.env.company,
        required = False,
        readonly = True
    )
    currency_id = fields.Many2one(
        comodel_name = 'res.currency',
        string = 'Currency',
        related = 'company_id.currency_id',
        readonly = True,
        ondelete = 'set null',
        help = "Used to display the currency when tracking monetary values"
    )

    

