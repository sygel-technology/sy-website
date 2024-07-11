# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    CustomerPortal.OPTIONAL_BILLING_FIELDS += [
        "lastname2",
    ]

    def details_form_validate(self, data):
        context = dict(request.env.context)
        # 'name' field cannont be updated as it would recompute fields
        # firstname, lastname and lastname2. That is why it is set
        # in context that changes in field name need to be ignored.
        context.update({"name_ignore": True})
        request.env.context = context
        error, error_message = super().details_form_validate(data)
        partner = request.env.user.partner_id
        if (
            not partner.can_edit_vat()
            and "lastname2" in data
            and data.get("lastname2") != partner.lastname2
        ):
            error["lastname2"] = "error"
            error_message.append(
                _(
                    "Changing Second Lastname is not allowed once document(s) "
                    "have been issued for your account. Please contact us "
                    "directly for this operation."
                )
            )
        return error, error_message
