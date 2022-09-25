from odoo import api, fields, models

class TrackingPatient(models.Model):
    _name = 'tracking.patient'
    _description = 'Tracking Patient'

    name = fields.Char(
        string='Asunto',
        required=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Paciente',
        required=True, domain=[('is_patient', '=', True)])
    email_patient = fields.Char(
        string='Paciente Email',
        required=False, related='patient_id.email')
    phone_patient = fields.Char(
        string='Telefono Paciente',
        required=False, related='patient_id.phone')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable',
        required=False)
    user_email = fields.Char('User Email', related='user_id.email', readonly=True)
    user_login = fields.Char('User Login', related='user_id.login', readonly=True)
    priority = fields.Selection(
        string='Prioridad',
        selection=[('0', 'Baja'),
                   ('1', 'Media'),
                   ('2', 'Alta'),
                   ('3', 'Muy Alta'),
                   ],
        required=False, )
    date_start = fields.Date(
        string='Fecha de Cita',
        required=False)
    nu_order = fields.Integer(
        string='No. Orden',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('new', 'Nuevo'),
                   ('contact', 'Contactando'),
                   ('confirm', 'Confirmado'),
                   ('attending', 'Attending'),
                   ('done', 'Hecho'),
                   ],
        required=False, default='new')
    calendar_event_ids = fields.One2many('calendar.event', 'tracking_patient_id', string='Calendario')
    doctor_id = fields.Many2one(
        comodel_name='res.users',
        string='Medico',
        required=False, )
    specialty_id = fields.Many2one(
        comodel_name='specialty.specialty',
        string='Especialidad',
        required=False, related='doctor_id.specialty_id')
    mode = fields.Selection(
        string='Modo de Consulta',
        selection=[('online', 'Online'),
                   ('offline', 'Presencial'), ],
        required=False, default='offline')
    description = fields.Text(
        string="Descripcion",
        required=False)

    @api.onchange('state')
    def _onchange_state(self):

        if self.state == 'confirm':
            self.create_event()

    def action_schedule_meeting(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("calendar.action_calendar_event")

        action['domain'] = [('tracking_patient_id', '=', self.id)]

        action['context'] = {
            'default_tracking_patient_id': self.id,
            'default_partner_id': self.patient_id.id,
            'default_name': self.name,
            'default_start': self.date_start,
            'default_end': self.date_start,
            'default_privacy': 'private'
        }

        return action

    def create_event(self):
        record = {
            'tracking_patient_id': self.id,
            'partner_id': self.patient_id.id,
            'name': self.name,
            'start': self.date_start,
            'stop': self.date_start,
            'privacy': 'private'
        }

        self.env['calendar.event'].create(record)

    def contacting(self):
        self.state = 'contact'

    def confirm(self):
        self.state = 'confirm'
        self.create_event()

    def done(self):
        self.state = 'done'

    def attending(self):
        last_patient = self.env['tracking.patient'].search([('date_start', '=', self.date_start),
                                                            ('doctor_id', '=', self.doctor_id.id),
                                                            ('user_id', '=', self.user_id.id)],
                                                           order='nu_order desc', limit=1)

        self.nu_order = last_patient.nu_order + 1

        self.env['medical.consultation'].create({
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'subject': self.name,
            'tracking_patient_id': self.id,
            'description': self.description,
            'mode': self.mode
        })

        self.state = 'attending'
        

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    tracking_patient_id = fields.Many2one(
        comodel_name='tracking.patient',
        string='Seguimiento de Paciente',
        required=False)