from odoo import api, fields, models

class Diseases(models.Model):
    _name = 'diseases.diseases'
    _description = 'Diseases'

    name = fields.Char(
        string='Nombre',
        required=True)
    symptom_ids = fields.Many2many(
        comodel_name='symptoms.symptoms', 
        string='Sintomas')
    description = fields.Text(
        string="Descripcion",
        required=False)
