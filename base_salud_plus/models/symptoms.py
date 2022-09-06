from odoo import api, fields, models

class Symptoms(models.Model):
    _name = 'symptoms.symptoms'
    _description = 'Symptoms'

    name = fields.Char(
        string='Sintoma',
        required=True)

