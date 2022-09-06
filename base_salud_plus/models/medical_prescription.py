from odoo import api, fields, models 

class Medicine(models.Model):
    _name = 'medicine.medicine'
    _description = 'Medicine'

    name = fields.Char(
        string='Name',
        required=True)

