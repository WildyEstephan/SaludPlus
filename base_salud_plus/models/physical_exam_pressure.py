from odoo import api, fields, models


class PhysicalPressureExam(models.Model):
    _name = 'physical.pressure.exam'
    _description = 'Physical & Pressure Exam'

    name = fields.Char(
        string='Exam',
        required=False)
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Unidad de Medida',
        required=False)


