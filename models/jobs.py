from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64
from datetime import date, datetime, timedelta


class jobs(models.Model):
    _name = 'housemaid.jobs'
    _description = 'Jobs Title'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "A name can only be assigned to one Job!"),
    ]

    name = fields.Char(
        string='Name',
        required=True,
        tracking=True,
    )
