# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "l10n_pt_hr_salary"
app_title = "L10N Pt Hr Salary"
app_publisher = "Luis Fernandes"
app_description = "Make salary for portugal"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "luisfmfernandes@gmail.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/l10n_pt_hr_salary/css/l10n_pt_hr_salary.css"
app_include_js = ["/assets/l10n_pt_hr_salary/js/nunjucks.min.js", "/assets/l10n_pt_hr_salary/js/pt_salary_structure.js"]

# include js, css files in header of web template
# web_include_css = "/assets/l10n_pt_hr_salary/css/l10n_pt_hr_salary.css"
# web_include_js = "/assets/l10n_pt_hr_salary/js/l10n_pt_hr_salary.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "l10n_pt_hr_salary.install.before_install"
# after_install = "l10n_pt_hr_salary.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "l10n_pt_hr_salary.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"l10n_pt_hr_salary.tasks.all"
# 	],
# 	"daily": [
# 		"l10n_pt_hr_salary.tasks.daily"
# 	],
# 	"hourly": [
# 		"l10n_pt_hr_salary.tasks.hourly"
# 	],
# 	"weekly": [
# 		"l10n_pt_hr_salary.tasks.weekly"
# 	]
# 	"monthly": [
# 		"l10n_pt_hr_salary.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "l10n_pt_hr_salary.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "l10n_pt_hr_salary.event.get_events"
# }

