from odoo import api, fields, models, _
from datetime import datetime

class MedicalConsultation(models.Model):
    _name = 'medical.consultation'
    _description = 'Medical Consultation'
    _order = 'date_consultation desc '

    name = fields.Char(
        string='Numero',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('new', 'Nuevo'),
                   ('approve', 'Aprobado'),
                   ('attending', 'Atendiendo'),
                   ('done', 'Hecho'),
                   ],
        required=False, default='new')

    # Patient
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Paciente',
        required=True, domain=[('is_patient', '=', True)])
    vat = fields.Char(
        string='Identificacion No.',
        required=False, related='patient_id.vat')
    medical_insurance_id = fields.Many2one(
        comodel_name='medical.insurance',
        string='Seguro',
        required=False, related='patient_id.medical_insurance_id')
    medical_category_id = fields.Many2one(
        comodel_name='medical.insurance.category',
        string='Categoria de seguro',
        required=False, domain="[('medical_insurance_id', '=', medical_insurance_id)]",
        related='patient_id.medical_category_id')
    medical_insurance_no = fields.Char(
        string='No. Seguro',
        required=False, related='patient_id.medical_insurance_no')
    date_expire_medical_insurance = fields.Date(
        string='Fecha de vencimiento de seguro',
        required=False, related='patient_id.date_expire_medical_insurance')
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
        required=False, related='patient_id.type_blood' )
    gender = fields.Selection(
        string='Sexo',
        selection=[('male', 'Masculino'),
                   ('female', 'Femenino'), ],
        required=False, related='patient_id.gender' )
    tipo_contribuyente = fields.Selection(
        string='Tipo Contribuyente',
        selection=[('consumo', 'Consumidor Final'),
                   ('contribuyente', 'Contribuyente'), ],
        required=False, related='patient_id.tipo_contribuyente' )
    email = fields.Char(
        string='Correo Electronico',
        required=False, related='patient_id.email')
    phone = fields.Char(
        string='Phone',
        required=False, related='patient_id.phone')
    mobile = fields.Char(
        string='Mobile',
        required=False, related='patient_id.mobile')
    # End Patient

    doctor_id = fields.Many2one(
        comodel_name='res.users',
        string='Medico',
        required=True, default=lambda self: self.env.user,)
    specialty_id = fields.Many2one(
        comodel_name='specialty.specialty',
        string='Especialidad',
        required=False, related='doctor_id.specialty_id')
    mode = fields.Selection(
        string='Modo de Consulta',
        selection=[('online', 'Online'),
                   ('offline', 'Presencial'), ],
        required=True, default='offline')
    type_consultation = fields.Selection(
        string='Tipo de Consulta',
        selection=[('emergency', 'Emergencia'),
                   ('normal', 'Normal'), ],
        required=True, default='normal')
    subject = fields.Char(
        string='Asunto',
        required=False)
    date_consultation = fields.Date(
        string='Fecha de Consulta',
        required=False, default=datetime.today(), readonly=True)
    description = fields.Text(
        string="Descripcion de consulta medica",
        required=False)
    prescription_ids = fields.One2many(
        comodel_name='medical.prescription',
        inverse_name='medical_consultation_id',
        string='Prescription_ids',
        required=False)
    labs_ids = fields.One2many(
        comodel_name='labs.indications',
        inverse_name='medical_consultation_id',
        string='Labs',
        required=False)
    result_ids = fields.One2many(
        comodel_name='result.labs',
        inverse_name='medical_consultation_id',
        string='Result_ids',
        required=False)

    # Seguimiento
    asunto_seguimiento = fields.Char(
        string='Asunto Seguimiento',
        required=False)
    date_next = fields.Date(
        string='Fecha Proxima Consulta',
        required=False)
    responsable_id_seguimiento = fields.Many2one(
        comodel_name='res.users',
        string='Responsable',
        required=False)
    description_seguimiento = fields.Text(
        string="Descripcion",
        required=False)
    tracking_patient_id = fields.Many2one(
        comodel_name='tracking.patient',
        string='Seguimiento',
        required=False)

    # Seguro
    aprobacion_no = fields.Char(
        string='Aprobacion no',
        required=False)

    # Factura
    date_income = fields.Date(
        string='Fecha Ingreso',
        required=False, default=datetime.today())
    amount = fields.Monetary(
        string='Monto',
        required=False)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        required=False, default=lambda self: self.env.user.company_id.currency_id,)

    exam_ids = fields.One2many(
        comodel_name='patient.physical.pressure.exam',
        inverse_name='medical_consultation_id',
        string='Examenes',
        required=False)
    pathological_background_ids = fields.One2many(
        comodel_name='allergy.disability.pathological.background',
        inverse_name='medical_consultation_id',
        string='Patologia',
        required=False, )
    disability_ids = fields.One2many(
        comodel_name='disability.background',
        inverse_name='medical_consultation_id',
        string='Discapacidad',
        required=False, )
    allergy_ids = fields.One2many(
        comodel_name='allergy.background',
        inverse_name='medical_consultation_id',
        string='Alergia',
        required=False, )

    def approve(self):

        if self.aprobacion_no:
            self.env['medical.insurances.approvations'].create({
                'name': self.aprobacion_no,
                'patient_id': self.patient_id.id,
                'medical_insurance_id': self.medical_insurance_id.id
            })

        self.state = 'approve'

    def attending(self):
        self.state = 'attending'

    def done(self):

        if self.date_next:
            self.env['tracking.patient'].create({
                'name': self.asunto_seguimiento,
                'patient_id': self.patient_id.id,
                'user_id': self.responsable_id_seguimiento.id,
                'description': self.description_seguimiento,
                'date_start': self.date_next,
                'doctor_id': self.doctor_id.id,
            })

        if self.tracking_patient_id:
            self.tracking_patient_id.done()

        self.state = 'done'

    def add_exam(self):
        wizard = self.env['add.exam.wizard'].create({

            'patient_id': self.patient_id.id,
            'medical_consultation_id': self.id
        })

        return {
            'name': _('Agregar'),
            'type': 'ir.actions.act_window',
            'res_model': 'add.exam.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new'
        }

    @api.model
    def create(self, values):
        # Add code here
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence']. \
                                 next_by_code('medical.consultation') or _('New')
        return super().create(values)

class MedicalPrescription(models.Model):
    _name = 'medical.prescription'
    _description = 'Medical Prescription'

    medicine_id = fields.Many2one(
        comodel_name='medicine.medicine',
        string='Farmaco',
        required=True)
    duration = fields.Char(
        string='Duracion del Tratamiento',
        required=True)
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Unidades',
        required=True)
    pauta = fields.Char(
        string='Pauta',
        required=True)
    indications = fields.Char(
        string='Indicaciones',
        required=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient',
        required=False)
    medical_consultation_id = fields.Many2one(
        comodel_name='medical.consultation',
        string='Consulta',
        required=False)
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='Recetado por',
        required=False, default=lambda self: self.env.user, )

class LabsIndications(models.Model):
    _name = 'labs.indications'
    _description = 'Labs Indications'

    labs = fields.Many2one(
        comodel_name='labs.labs',
        string='Indicacion',
        required=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient_id',
        required=False)
    medical_consultation_id = fields.Many2one(
        comodel_name='medical.consultation',
        string='Consulta',
        required=False)
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='Indicado por',
        required=False, default=lambda self: self.env.user, )

class ResultLabs(models.Model):
    _name = 'result.labs'
    _description = 'Result Labs'

    name = fields.Char(
        string='Resultados',
        required=False)
    date = fields.Date(
        string='Fecha de Registro',
        required=False, deafult=datetime.today())
    filename = fields.Char(
        string='Filename',
        required=False)
    file_labs = fields.Binary(string="Documento",  )
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient_id',
        required=False)
    medical_consultation_id = fields.Many2one(
        comodel_name='medical.consultation',
        string='Consulta',
        required=False)
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='Registado por',
        required=False, default=lambda self: self.env.user, )

class ResUsers(models.Model):
    _inherit = 'res.users'

    specialty_id = fields.Many2one(
        comodel_name='specialty.specialty',
        string='Especialidad',
        required=False)
