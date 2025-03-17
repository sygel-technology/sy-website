# Copyright 2025 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Hide My Timesheets View in Portal",
    "summary": "Hide My Timesheets View in Portal",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/sygel-technology/sy-website",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "hr_timesheet",
        "http_routing",
    ],
    "data": [
        "views/hr_timesheet_portal_template.xml",
    ],
}
