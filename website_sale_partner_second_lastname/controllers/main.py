# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.http import request

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values, errors, error_msg = super(WebsiteSale, self).values_postprocess(
            order=order, mode=mode, values=values, errors=errors, error_msg=error_msg
        )
        new_values.update({"lastname2": values.get("lastname2") or ""})
        return new_values, errors, error_msg

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
        )
        if data.get("partner_id"):
            partner_su = (
                request.env["res.partner"]
                .sudo()
                .browse(int(data["partner_id"]))
                .exists()
            )
            can_edit_vat = (
                partner_su.parent_id.can_edit_vat()
                if partner_su.parent_id
                else partner_su.can_edit_vat()
            )
            # Last AND expression explanation:
            # data['lastname2'] or partner_su.lastname2 not in ['', False]
            # When lastname2 field in form is empty, its values is False
            # When lastname2 field in backend is empty, its values is ''
            # In that case, if both are compared, they are considered to be
            # different so data['lastname2'] != partner_su.lastname2 would
            # return True although no real change would have been applied.
            # That is why this AND expression is added.
            lastname2_change = (
                partner_su
                and "lastname2" in data
                and data["lastname2"] != partner_su.lastname2
                and (data["lastname2"] or partner_su.lastname2 not in ["", False])
            )
            if lastname2_change and not can_edit_vat:
                error["lastname2"] = "error"
                error_message.append(
                    _(
                        "Changing your second last name is not allowed once "
                        "invoices have been issued for your account. Please "
                        "contact us directly for this operation."
                    )
                )
            # Prevent change the partner name, lastname or second last name if
            # it is an internal user.
            if (lastname2_change) and not all(partner_su.user_ids.mapped("share")):
                error.update(
                    {
                        "lastname2": "error" if lastname2_change else None,
                    }
                )
                error_message.append(
                    _(
                        "If you are ordering for an external person, please place "
                        "your order via the backend. If you wish to change your "
                        "name, last name or second last name, please do so in the "
                        "account settings or contact your administrator."
                    )
                )
        return error, error_message


class AuthSignupHome(AuthSignupHome):
    def get_auth_signup_qcontext(self):
        qcontext = super().get_auth_signup_qcontext()
        qcontext.update(
            {
                k: v
                for (k, v) in request.params.items()
                if k
                in {
                    "lastname2",
                }
            }
        )
        return qcontext

    def _prepare_signup_values(self, qcontext):
        values = super()._prepare_signup_values(qcontext)
        if "lastname2" in qcontext:
            values["lastname2"] = qcontext["lastname2"]
        return values
