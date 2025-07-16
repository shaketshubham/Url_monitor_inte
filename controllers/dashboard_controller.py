# File: controllers/dashboard_controller.py
from odoo import http
from odoo.http import request
from datetime import datetime, timedelta

class MonitorDashboard(http.Controller):

    @http.route('/monitor/dashboard/data', auth='user', type='json')
    def get_dashboard_data(self):
        Monitor = request.env['url.monitor'].sudo()
        Incident = request.env['url.incident'].sudo()

        total_monitors = Monitor.search_count([])
        down_monitors = Monitor.search_count([('last_status', '=', 'down')])

        # Calculate uptime percentage over last 24h
        now = datetime.utcnow()
        last_24h = now - timedelta(hours=24)
        check_results = Incident.search([('started_at', '>=', last_24h)])
        total_checks = len(check_results)
        failed_checks = len([i for i in check_results if i.type in ('timeout', '5xx', 'failure')])
        uptime_24h = round(100 - (failed_checks / total_checks * 100), 2) if total_checks > 0 else 100.0

        # Latency chart (simulate last 12 hours)
        latency_chart = []
        monitors = Monitor.search([])
        for monitor in monitors:
            if monitor.last_latency:
                latency_chart.append({
                    'time': monitor.last_checked_at.strftime('%H:%M') if monitor.last_checked_at else 'N/A',
                    'latency': monitor.last_latency
                })
                if len(latency_chart) >= 12:
                    break

        return {
            'total_monitors': total_monitors,
            'down_monitors': down_monitors,
            'uptime_24h': uptime_24h,
            'latency_chart': latency_chart,
        }
