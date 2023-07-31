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

    code = fields(
        string = 'Short Name',
        required=True)
    name = fields.Char(
        string = 'Name',
        required = True)
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Office.")
    description = fields.Text(
        string = 'Description')