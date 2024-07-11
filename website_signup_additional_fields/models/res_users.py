# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from ast import literal_eval

from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _signup_create_user(self, values):
        if self.env.context.get("website_id"):
            website_id = self.env["website"].browse(self.env.context.get("website_id"))
            if (
                website_id
                and website_id.signup_use_additional_fields
                and website_id.signup_additional_fields
            ):
                template_user_id = literal_eval(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("base.template_portal_user_id", "False")
                )
                template_user = self.browse(template_user_id)
                if template_user:
                    partner = template_user.partner_id
                    for field in website_id.signup_additional_fields:
                        values[field.name] = getattr(partner, field.name)
        return super()._signup_create_user(values)
