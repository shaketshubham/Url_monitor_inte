from odoo import models, fields, api
import requests
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class URLMonitor(models.Model):
    _name = 'url.monitor'
    _description = 'Monitored URL'
    _order = 'name'

    name = fields.Char(string='Monitor Name', required=True)
    url = fields.Char(string='URL', required=True)
    check_interval = fields.Integer(string='Check Interval (seconds)')
    latency_threshold = fields.Integer(string='Latency Threshold (ms)')
    alert_email = fields.Char(string='Alert Email')
    alert_webhook = fields.Char(string='Alert Webhook')
    active = fields.Boolean(string='Is Active?', default=True)
    
    last_status = fields.Selection([
        ('up', 'Up'),
        ('down', 'Down'),
        ('unknown', 'Unknown')
    ], default='unknown', string='Last Known Status')
    
    last_latency = fields.Float(string='Last Latency (ms)')
    last_checked_at = fields.Datetime(string='Last Checked At')

    incident_count = fields.Integer(string='Incident Count', compute='_compute_incident_count', store=True)

    user_id = fields.Many2one('res.users', string='Assigned User')
    incident_ids = fields.One2many('url.incident', 'monitor_id', string='Incidents')

    # Compute how many incidents are linked
    @api.depends('incident_ids')
    def _compute_incident_count(self):
        for monitor in self:
            monitor.incident_count = len(monitor.incident_ids)

    # Sync Monitors from FastAPI backend
    @api.model
    def sync_monitors_from_fastapi(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('fastapi_base_url')

        if not base_url:
            _logger.warning("FastAPI Base URL not configured in system parameters.")
            return

        try:
            response = requests.get(f"{base_url}/monitors", timeout=5)
            response.raise_for_status()
            monitors = response.json()

            for mon in monitors:
                existing = self.search([('url', '=', mon['url'])], limit=1)

                values = {
                    'name': mon['url'],
                    'url': mon['url'],
                    'check_interval': mon.get('check_interval'),
                    'latency_threshold': mon.get('latency_threshold_ms'),
                    'alert_email': mon.get('alert_email'),
                    'alert_webhook': mon.get('alert_webhook'),
                    'active': mon.get('is_active', True),
                    'last_checked_at': mon.get('last_checked_at'),
                }

                if existing:
                    existing.write(values)
                else:
                    self.create(values)

        except Exception as e:
            _logger.warning(f"[Monitor Sync] Error: {str(e)}")
