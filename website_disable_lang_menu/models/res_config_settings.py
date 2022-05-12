# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    excluded_language_ids = fields.Many2many(
        related='website_id.excluded_language_ids',
        relation='res.lang',
        readonly=False
    )

    @api.constrains("excluded_language_ids", "website_default_lang_id")
    def _check_excluded_language_ids(self):
        for sel in self.sudo():
            if (
                sel.website_default_lang_id 
                and sel.website_default_lang_id.id in sel.excluded_language_ids.ids
            ):
                raise ValidationError(
                    _(
                        "Default language cannot be excluded"
                    )
                )
