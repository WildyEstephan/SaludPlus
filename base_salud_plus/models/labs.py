from odoo import api, fields, models

class Labs(models.Model):
    _name = 'labs.labs'
    _description = 'Labs'

    name = fields.Char(
        string='Nombre',
        required=False)

