# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Sale Partner Second Lastname",
    "version": "15.0.1.0.0",
    "category": "Website",
    "summary": "Introduce second lastname in website.",
    "author": "Sygel Technology",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "development_status": "Beta",
    "depends": [
        "website_sale_partner_firstname",
        "partner_second_lastname",
    ],
    "data": [
        "views/templates.xml",
        "views/auth_signup_login_templates.xml",
        "views/portal_templates.xml",
    ],
}
