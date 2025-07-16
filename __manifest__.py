{
    'name': 'URL Monitor Integration',
    'version': '1.0',
    'summary': 'Integrate FASTAPI-based URL monitor with Odoo',
    'author': 'Shaket Shubham',
    'category': 'Tools',
    'depends': ['base','web'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/menu_root.xml',
        'views/url_monitor_views.xml',
        'views/url_incident_views.xml',
        'views/dashboard_menu.xml',
        'data/cron_jobs.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'url_monitor_integration/static/src/js/monitor_dashboard.js',
            'url_monitor_integration/static/src/xml/monitor_dashboard.xml',
        ],
    },
}

