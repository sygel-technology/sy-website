# Copyright 2019 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import _, http
from odoo.http import request

from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.project.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    def _get_my_tasks_searchbar_filters_state(self):
        searchbar_filters_state = {
            "all": {"order": -3, "label": _("All"), "domain": []},
        }
        # searchbar_filters_state all states
        for state in request.env["project.task.type"].search(
            [("case_default", "=", True)]
        ):
            searchbar_filters_state.update(
                {
                    str(state.id): {
                        "order": state.sequence,
                        "label": state.name,
                        "domain": [("stage_id", "=", state.id)],
                    }
                }
            )
        # searchbar_filters_state open
        ptt_active = (
            request.env["project.task.type"]
            .search([("case_default", "=", True), ("fold", "=", True)])
            .ids
        )
        searchbar_filters_state.update(
            {
                "active": {
                    "order": -2,
                    "label": _("Active"),
                    "domain": [("stage_id", "not in", ptt_active)],
                }
            }
        )
        # searchbar_filters_state closed
        searchbar_filters_state.update(
            {
                "inactive": {
                    "order": -1,
                    "label": _("Inactive"),
                    "domain": [("stage_id", "in", ptt_active)],
                }
            }
        )

        return searchbar_filters_state

    @http.route(
        ["/my/tasks", "/my/tasks/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_tasks(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        groupby=None,
        filterbystate=None,
        **kw
    ):

        searchbar_filters = self._get_my_tasks_searchbar_filters()
        searchbar_filters_state = self._get_my_tasks_searchbar_filters_state()
        if not filterby:
            filterby = "all"
        domain = searchbar_filters.get(filterby, searchbar_filters.get("all"))["domain"]

        # Filterbystate
        if not filterbystate:
            filterbystate = "active"
        domain += searchbar_filters_state.get(
            filterbystate, searchbar_filters_state.get("all")
        )["domain"]

        values = self._prepare_tasks_values(
            page,
            date_begin,
            date_end,
            sortby,
            search,
            search_in,
            groupby,
            domain=domain,
        )

        # pager
        pager_vals = values["pager"]
        pager_vals["url_args"].update(filterby=filterby, filterbystate=filterbystate)
        pager = portal_pager(**pager_vals)

        values.update(
            {
                "grouped_tasks": values["grouped_tasks"](pager["offset"]),
                "pager": pager,
                "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
                "searchbar_filters_state": OrderedDict(
                    sorted(searchbar_filters_state.items())
                ),
                "filterby": filterby,
                "filterbystate": filterbystate,
            }
        )
        return request.render("project.portal_my_tasks", values)
