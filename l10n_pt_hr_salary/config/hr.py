from __future__ import unicode_literals
__author__ = 'luissaguas'

from frappe import _

def get_data():
	return [
		{
			"label": _("Setup"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Incidence Base",
					"description": _("Incidence Base."),
				},
				{
					"type": "doctype",
					"name": "IRS Table",
					"description": _("IRS Table."),
				}
			]
		}
	]