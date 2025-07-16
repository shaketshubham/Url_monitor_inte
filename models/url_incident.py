from odoo import models, fields, api
import requests
import logging
class URLIncident(models.Model):
    _name = 'url.incident'
    _description = 'Incident Log'
    _order = 'started_at desc'  # newest first

    monitor_id = fields.Many2one('url.monitor', string='Monitor', required=True, ondelete='cascade')
    
    type = fields.Selection([
        ('timeout', 'Timeout'),
        ('latency', 'Latency Spike'),
        ('5xx', '5xx Error'),
        ('failure', 'Other Failure')
    ], string='Incident Type', required=True)

    started_at = fields.Datetime(string='Start Time', required=True)
    resolved_at = fields.Datetime(string='Resolved At')
    
    notified = fields.Boolean(string='Notified?', default=False)

    duration_minutes = fields.Float(string="Duration (minutes)", compute='_compute_duration', store=True)

    # Auto compute duration
    @api.depends('started_at', 'resolved_at')
    def _compute_duration(self):
        for record in self:
            if record.resolved_at and record.started_at:
                duration = (record.resolved_at - record.started_at).total_seconds() / 60
                record.duration_minutes = round(duration, 2)
            else:
                record.duration_minutes = 0.0
    

    @api.model
    def sync_incidents_from_fastapi(self):
        base_url=self.env['ir.config_parameter'].sudo().get_param('fastapi_base_url')
        try:
            response=requests.get(f"{base_url}/incidents",timeout=5)
            response.raise_for_status()
            incidents=response.json()

            for inc in incidents:
                monitor=self.env['url.monitor'].search([('url','=',inc['url'])],limit=1)
                if not monitor:
                    continue
                existing=self.search([
                    ('monitor_id','=',monitor.id)
                    ('started_at','=',inc['started_at'])
                ],limit=1)
                values={
                    'monitor_id':monitor.id,
                    'type':inc['type'],
                    'started_at':inc['started_at'],
                    'resolved_at':inc.get('resolved_at'),
                    'notified':inc.get('notified',False)

                }

                if existing:
                    existing.write(values)
                else:
                    self.create(values)
        except Exception as e:
            _logger=logging.getLogger(__name__)
            _logger.warning(f"[Incident Sync] Error : {str(e)}")
        