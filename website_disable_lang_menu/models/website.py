# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    excluded_language_ids = fields.Many2many(
        'res.lang',
        'website_excluded_lang_rel',
        'website_id',
        'excluded_lang_id',
        'Excluded Languages'
    )
