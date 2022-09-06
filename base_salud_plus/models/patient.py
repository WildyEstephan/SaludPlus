from odoo import api, fields, models
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(
        string='Es Paciente',
        required=False)
    medical_insurance_id = fields.Many2one(
        comodel_name='medical.insurance',
        string='Seguro',
        required=False)
    medical_category_id = fields.Many2one(
        comodel_name='medical.insurance.category',
        string='Categoria de seguro',
        required=False, domain="[('medical_insurance_id', '=', medical_insurance_id)]")
    medical_insurance_no = fields.Char(
        string='No. Seguro',
        required=False)
    date_expire_medical_insurance = fields.Date(
        string='Fecha de vencimiento de seguro',
        required=False)
    birth_date = fields.Date(
        string='Nacimiento',
        required=False)
    type_blood = fields.Selection(
        string='Tipo de sangre',
        selection=[
                   ('a+', 'A+'),
                   ('a-', 'A-'),
                   ('b+', 'B+'),
                   ('b-', 'B-'),
                   ('ab+', 'AB+'),
                   ('ab-', 'AB-'),
                   ('o+', 'O+'),
                   ('o-', 'O-'),
                   ],
        required=False, )
    gender = fields.Selection(
        string='Sexo',
        selection=[('male', 'Masculino'),
                   ('female', 'Femenino'), ],
        required=False, )
    tipo_contribuyente = fields.Selection(
        string='Tipo Contribuyente',
        selection=[('consumo', 'Consumidor Final'),
                   ('contribuyente', 'Contribuyente'), ],
        required=False, )
    exam_ids = fields.One2many(
        comodel_name='patient.physical.pressure.exam',
        inverse_name='patient_id',
        string='Examenes',
        required=False)
    pathological_background_ids = fields.One2many(
        comodel_name='allergy.disability.pathological.background',
        inverse_name='patient_id',
        string='Patologia',
        required=False, domain="[('type_diseases', '=', 'diseases')]")
    disability_ids = fields.One2many(
        comodel_name='allergy.disability.pathological.background',
        inverse_name='patient_id',
        string='Discapacidad',
        required=False, domain="[('type_diseases', '=', 'disability')]")
    allergy_ids = fields.One2many(
        comodel_name='allergy.disability.pathological.background',
        inverse_name='patient_id',
        string='Alergia',
        required=False, domain="[('type_diseases', '=', 'allergy')]")
    consultation_ids = fields.One2many(
        comodel_name='medical.consultation',
        inverse_name='patient_id',
        string='Consultas',
        required=False)
    consultation_count = fields.Integer(
        string='Consultation_count',
        required=False, compute='_compute_consultation_count')
    prescription_ids = fields.One2many(
        comodel_name='medical.prescription',
        inverse_name='patient_id',
        string='Recetas',
        required=False)
    prescription_count = fields.Integer(
        string='Prescription_count',
        required=False, compute='_compute_prescription_count')
    indication_ids = fields.One2many(
        comodel_name='labs.indications',
        inverse_name='patient_id',
        string='Laboratorio',
        required=False)
    indication_count = fields.Integer(
        string='Indication_count',
        required=False, compute='_compute_indication_count')
    result_lab_ids = fields.One2many(
        comodel_name='labs.indications',
        inverse_name='patient_id',
        string='Laboratorio',
        required=False)
    result_lab_count = fields.Integer(
        string='Indication_count',
        required=False, compute='_compute_result_lab_count')

    def action_view_consultation(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base_salud_plus.medical_consultation_action')
        action['domain'] = [('patient_id.id', '=', self.id)]
        return action

    def action_view_prescription(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base_salud_plus.prescription_view_action')
        action['domain'] = [('patient_id.id', '=', self.id)]
        return action

    def action_view_indication(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base_salud_plus.labs_indications_view_action')
        action['domain'] = [('patient_id.id', '=', self.id)]
        return action

    def action_view_result_lab(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base_salud_plus.result_labs_view_action')
        action['domain'] = [('patient_id.id', '=', self.id)]
        return action

    @api.depends('consultation_ids')
    def _compute_consultation_count(self):
        for rec in self:
            rec.consultation_count = len(rec.consultation_ids)

    @api.depends('result_lab_ids')
    def _compute_result_lab_count(self):
        for rec in self:
            rec.result_lab_count = len(rec.result_lab_ids)

    @api.depends('prescription_ids')
    def _compute_prescription_count(self):
        for rec in self:
            rec.prescription_count = len(rec.prescription_ids)

    @api.depends('indication_ids')
    def _compute_indication_count(self):
        for rec in self:
            rec.indication_count = len(rec.indication_ids)


class PatientPhysicalPressureExam(models.Model):
    _name = 'patient.physical.pressure.exam'
    _description = 'Patient Physical & Pressure Exam'
    _order = 'date asc'

    date = fields.Date(
        string='Fecha',
        required=True, default=datetime.today())
    exam_id = fields.Many2one(
        comodel_name='',
        string='Examen',
        required=True)
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Unidad de Medida',
        required=False)
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='Registrado por',
        required=False, default=lambda self: self.env.user, readonly=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Paciente',
        required=False)
    medical_consultation_id = fields.Many2one(
        comodel_name='medical.consultation',
        string='Consulta',
        required=False)

class PathologicalBackground(models.Model):
    _name = 'allergy.disability.pathological.background'
    _description = 'Pathological Background'

    diseases_id = fields.Many2one(
        comodel_name='diseases.diseases',
        string='Enfermedad',
        required=True)
    type_diseases = fields.Selection(
        string='Type Diseases',
        selection=[('diseases', 'Enfermedad'),
                   ('disability', 'Discapacidad'),
                   ('allergy', 'Alergia'),
                   ],
        required=False, )

    origin = fields.Selection(
        string='Origen',
        selection=[('patient', 'Paciente'),
                   ('family', 'Familia'), ],
        required=False, )
    date = fields.Date(
        string='Fecha',
        required=True, default=datetime.today())
    action = fields.Selection(
        string='Accion',
        selection=[('healed', 'Sano'),
                   ('in_treatment', 'En tratamiento'),
                   ('sick', 'No atendido'),
                   ],
        required=True, )
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='Registrado por',
        required=False, default=lambda self: self.env.user, readonly=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Paciente',
        required=False)
    medical_consultation_id = fields.Many2one(
        comodel_name='medical.consultation',
        string='Consulta',
        required=False)




