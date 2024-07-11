# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_signup_use_additional_fields = fields.Boolean(
        string="Use Signup Additional Fields",
        related="website_id.signup_use_additional_fields",
        readonly=False,
    )
    website_signup_additional_fields = fields.Many2many(
        string="Signup Additional Fields",
        comodel_name="ir.model.fields",
        related="website_id.signup_additional_fields",
        readonly=False,
        domain=[("model", "=", "res.partner")],
    )
