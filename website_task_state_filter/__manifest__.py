# Copyright 2019 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Task State Filter",
    "summary": "This module allow to filter tasks by states in website.",
    "version": "16.0.1.0.0",
    "category": "Custom",
    "website": "https://github.com/sygel-technology/sy-website",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "portal",
        "project",
        "project_task_default_stage",
    ],
    "data": [
        "views/portal_search_bar.xml",
    ],
}
