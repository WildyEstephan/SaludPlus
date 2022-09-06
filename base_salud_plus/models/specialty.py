from odoo import api, fields, models


class Specialty(models.Model):
    _name = 'specialty.specialty'
    _description = 'Specialty'

    name = fields.Char(
        string='Especialidad',
        required=True)
    user_ids = fields.One2many(
        comodel_name='res.users',
        inverse_name='specialty_id',
        string='Doctores',
        required=False)

class Users(models.Model):
    _inherit = 'res.users'

    specialty_id = fields.Many2one(
        comodel_name='specialty.specialty',
        string='Especialidad',
        required=False)
