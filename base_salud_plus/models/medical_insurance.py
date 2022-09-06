from odoo import api, fields, models

class MedicalInsurance(models.Model):
    _name = 'medical.insurance'
    _description = 'Medical Insurance'

    name = fields.Char(
        string='Nombre',
        required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto',
        required=True)
    category_ids = fields.One2many(
        comodel_name='medical.insurance.category',
        inverse_name='medical_insurance_id',
        string='Categororias',
        required=False)

class MedicalInsuranceCategory(models.Model):
    _name = 'medical.insurance.category'
    _description = 'Medical Insurance Category'

    name = fields.Char(
        string='Categoria',
        required=True)
    level = fields.Integer(
        string='Nivel',
        required=True)
    medical_insurance_id = fields.Many2one(
        comodel_name='medical.insurance',
        string='Medical Insurance',
        required=False)

class MedicalInsurancesApprovations(models.Model):
    _name = 'medical.insurances.approvations'
    _description = 'Medical Insurances Approvations'

    name = fields.Char(
        string='Numero',
        required=False)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Paciente',
        required=False)
    medical_insurance_id = fields.Many2one(
        comodel_name='medical.insurance',
        string='Seguro',
        required=False)


