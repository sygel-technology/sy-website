# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def signup(self, values, token=None):
        if token:
            partner = self.env["res.partner"]._signup_retrieve_partner(
                token, check_validity=True, raise_exception=True
            )
            partner_user = partner.user_ids and partner.user_ids[0] or False
            # Don't update firstname, lastname, and lastname2 if partner
            # related to user exists (i.e. when resetting password)
            if partner_user:
                values.pop("lastname2", None)
        return super().signup(values, token)

    def _create_user_from_template(self, values):
        user = super()._create_user_from_template(values)
        user.write(
            {
                "lastname2": values.get("lastname2"),
            }
        )
        return user
