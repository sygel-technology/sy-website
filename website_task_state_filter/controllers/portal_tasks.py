# Copyright 2019 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import OrderedDict
from operator import itemgetter

from markupsafe import Markup

from odoo import _, http
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem

from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.project.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    @http.route(
        ["/my/tasks", "/my/tasks/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_tasks(  # noqa: C901
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        groupby="project",
        filterbystate=None,
        **kw
    ):

        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Title"), "order": "name"},
            "stage": {"label": _("Stage"), "order": "stage_id"},
            "project": {"label": _("Project"), "order": "project_id, stage_id"},
            "update": {
                "label": _("Last Stage Update"),
                "order": "date_last_stage_update desc",
            },
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_filters_state = {
            "all": {"order": -3, "label": _("All"), "domain": []},
        }
        searchbar_inputs = {
            "content": {
                "input": "content",
                "label": Markup(_('Search <span class="nolabel"> (in Content)</span>')),
            },
            "message": {"input": "message", "label": _("Search in Messages")},
            "customer": {"input": "customer", "label": _("Search in Customer")},
            "stage": {"input": "stage", "label": _("Search in Stages")},
            "project": {"input": "project", "label": _("Search in Project")},
            "all": {"input": "all", "label": _("Search in All")},
        }
        searchbar_groupby = {
            "none": {"input": "none", "label": _("None")},
            "project": {"input": "project", "label": _("Project")},
            "stage": {"input": "stage", "label": _("Stage")},
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
        # extends filterby criteria with project the customer has access to
        projects = request.env["project.project"].search([])
        for project in projects:
            searchbar_filters.update(
                {
                    str(project.id): {
                        "label": project.name,
                        "domain": [("project_id", "=", project.id)],
                    }
                }
            )

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env["project.task"].read_group(
            [("project_id", "not in", projects.ids)], ["project_id"], ["project_id"]
        )
        for group in project_groups:
            proj_id = group["project_id"][0] if group["project_id"] else False
            proj_name = group["project_id"][1] if group["project_id"] else _("Others")
            searchbar_filters.update(
                {
                    str(proj_id): {
                        "label": proj_name,
                        "domain": [("project_id", "=", proj_id)],
                    }
                }
            )

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]
        # default group by value
        if not groupby:
            groupby = "project"
        if not filterbystate:
            filterbystate = "active"
        domain += searchbar_filters_state[filterbystate]["domain"]
        # archive groups - Default Group By 'create_date'
        # archive_groups = self._get_archive_groups('project.task', domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ("content", "all"):
                search_domain = OR(
                    [
                        search_domain,
                        [
                            "|",
                            ("name", "ilike", search),
                            ("description", "ilike", search),
                        ],
                    ]
                )
            if search_in in ("customer", "all"):
                search_domain = OR([search_domain, [("partner_id", "ilike", search)]])
            if search_in in ("message", "all"):
                search_domain = OR(
                    [search_domain, [("message_ids.body", "ilike", search)]]
                )
            if search_in in ("stage", "all"):
                search_domain = OR([search_domain, [("stage_id", "ilike", search)]])
            if search_in in ("project", "all"):
                search_domain = OR([search_domain, [("project_id", "ilike", search)]])
            domain += search_domain

        # task count
        task_count = request.env["project.task"].search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/tasks",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
                "groupby": groupby,
                "filterbystate": filterbystate,
            },
            total=task_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        if groupby == "project":
            order = (
                "project_id, %s" % order
            )  # force sort on project first to group by project in view
        elif groupby == "stage":
            order = (
                "stage_id, %s" % order
            )  # force sort on stage first to group by stage in view

        tasks = request.env["project.task"].search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=(page - 1) * self._items_per_page,
        )
        request.session["my_tasks_history"] = tasks.ids[:100]
        groupby_mapping = self._task_get_groupby_mapping()
        group = groupby_mapping.get(groupby)
        if group:
            grouped_tasks = [
                request.env["project.task"].concat(*g)
                for k, g in groupbyelem(tasks, itemgetter(group))
            ]
        else:
            grouped_tasks = [tasks] if tasks else []

        # Es necesario hacer esto para que no falle la vista base
        if not grouped_tasks or not grouped_tasks[0].ids:
            grouped_tasks = False

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "grouped_tasks": grouped_tasks,
                "page_name": "task",
                "default_url": "/my/tasks",
                "task_url": "task",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "search": search,
                "sortby": sortby,
                "groupby": groupby,
                "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
                "searchbar_filters_state": OrderedDict(
                    sorted(searchbar_filters_state.items(), key=lambda t: t[1]["order"])
                ),
                "filterbystate": filterbystate,
                "filterby": filterby,
            }
        )
        return request.render("project.portal_my_tasks", values)
