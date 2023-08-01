from odoo import fields, models, _
from odoo.exceptions import UserError

class sponsers(models.AbstractModel):

    _name = 'housemaid.sponsers'
    _description = 'Records of Sponsers.'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one equipment !"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one equipment !"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    code = fields.Char(
        string = 'Short Name',
        required=True)
    name = fields.Char(
        string = 'Name',
        required = True)
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Office.")
    partner_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Partner')
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

