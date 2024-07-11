# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    signup_use_additional_fields = fields.Boolean(string="Use Signup Additional Fields")
    signup_additional_fields = fields.Many2many(
        string="Signup Additional Fields",
        comodel_name="ir.model.fields",
        domain=[("model", "=", "res.partner")],
    )
