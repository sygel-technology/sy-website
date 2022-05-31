# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.http import request


class View(models.Model):
    _inherit = "ir.ui.view"

    @api.model
    def _prepare_qcontext(self):
        vals = super(View, self)._prepare_qcontext()
        if request and getattr(request, 'website', False) and \
                not self.env.user.has_group('base.group_user') and \
                request.website.excluded_language_ids and \
                vals.get('languages'):
            vals['languages'] = list(filter(
                lambda a: a[0] not in request.website.excluded_language_ids.mapped(
                    'code'
                ) or a[0] == self._context.get('lang'), vals.get('languages')
            ))
        return vals
