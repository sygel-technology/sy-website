# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Signup Additional Fields",
    "version": "15.0.1.0.0",
    "category": "Website",
    "summary": "Add default fields when creating user from website.",
    "website": "https://github.com/sygel-technology/sy-website",
    "author": "Sygel Technology",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website", "auth_signup"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
}
