# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Disable Language Menu",
    "summary": "Hide languages from website languages menu",
    "version": "13.0.1.0.0",
    "category": "Website",
    "website": "https://www.sygel.es",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ]
}
