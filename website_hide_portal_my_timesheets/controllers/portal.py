# Copyright 2025 Ángel García de la Chica Herrera<angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class TimesheetCustomerPortal(CustomerPortal):
    @http.route(
        ["/my/timesheets", "/my/timesheets/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_timesheets(
        self,
        page=1,
        sortby=None,
        filterby=None,
        search=None,
        search_in="all",
        groupby="none",
        **kw
    ):
        return request.render("http_routing.404")
