# -*- coding: utf-8 -*-
__author__ = 'luissaguas'


import frappe, json
from frappe import _
from frappe.utils import cint, flt, rounded
from jinja2 import Environment, Template, contextfunction



def set_functions_context(env):
	env.globals.update({"get_irs_tax":get_irs_tax})
	env.globals.update({"get_field_value":get_document_field})
	#env.globals.update({"get_from_sql":get_doctype_document_sql})
	env.globals.update({"get_from_date":get_from_date})
	#env.globals.update({"check_ciclo": check_ciclo})

@contextfunction
def get_from_date(ctx, date, dformat="%Y-%m-%d", what="year"):
	from datetime import datetime
	d = getattr(datetime.strptime(date, dformat), what)
	print "getting date %s year %s" % (date, d)
	return d

"""
@contextfunction
def get_doctype_document_sql(ctx, sql, **keydict):
	#field_value = frappe.get_value(doctype, frappe.utils.encode(docname), frappe.utils.encode(field))
	lsql = sql % (**keydict, )
"""

@contextfunction
def get_document_field(ctx, doctype, docname, field):
	field_value = frappe.get_value(doctype, docname, field)
	print "get field %s value %s" % (doctype, field_value)
	return field_value

@contextfunction
def get_irs_tax(ctx, ordenado, doctype, docname, field):
	sql = """
		select remuneracao, `%(field)s` from `tab%(parent_doctype)s` where parent = '%(docname)s' and remuneracao >= %(ordenado)s order by remuneracao ASC LIMIT 1;
	""" % ({"field":field, "parent_doctype": doctype, "docname": docname, "ordenado": ordenado})
	res = frappe.db.sql(sql)
	return res[0][1]


@contextfunction
def check_ciclo(ctx, ordenado):
	#field_value = frappe.get_value(doctype, frappe.utils.encode(docname), frappe.utils.encode(field))
	print "get field ordenado %s" %(ordenado)


@frappe.whitelist()
def calculate_earnings_description(doc):

	iliquid = 0
	tributavel = 0

	doc_salary = frappe._dict(json.loads(doc))
	earn_docs = doc_salary.earnings

	result_description = frappe._dict({
		"tributavel": [],
		"totals": [],
	})

	precision = 2

	for doc in earn_docs:
		doc = frappe._dict(doc)
		e_type = frappe.utils.encode(doc.e_type)
		doc_etype = frappe.get_doc("Earning Type", e_type)
		incidence_base = frappe.utils.encode(doc_etype.incidence_base)
		modified_value = doc.modified_value

		print "modified value %s" %modified_value
		iliquid += modified_value
		if incidence_base == "Tributável":
			tribut_value = get_tributavel_value(doc_salary, doc_etype, doc, precision)
			result_description.tributavel.append({"e_type": e_type, "value": tribut_value})
			tributavel += tribut_value

	totals = frappe._dict({"iliquid": iliquid, "tributavel": tributavel})
	result_description.totals.append(totals)
	calculate_deductions(doc_salary, totals, result_description, precision)

	return result_description


def get_tributavel_value(doc_salary, doc_type, doc_struct, precision):

	tributavel_calcule = doc_type.tributavel_calcule

	if not tributavel_calcule:
		tributavel_value = rounded(doc_struct.modified_value, precision)
		return tributavel_value

	is_diary = doc_type.diary_earning_

	if is_diary:
		value = doc_struct.modified_value_diary
	else:
		value = doc_struct.modified_value

	context = {"value": value}

	doc_employee = frappe.get_doc("Employee", doc_salary.employee).as_dict()
	doc_type_dict = doc_type.as_dict()

	for attr in ("tributavel_calcule", "parent", "parenttype", "parentfield", "owner", "modified_by", "short_name", "idx"):
		doc_type_dict.pop(attr, None)
		doc_struct.pop(attr, None)
		doc_employee.pop(attr, None)

	context.update({doc_type_dict.short_name: doc_type_dict})
	context.update({doc_struct.short_name: doc_struct})

	context.update(doc_employee)
	context.update(doc_struct)
	context.update(doc_type_dict)

	try:
		t = Template(tributavel_calcule, extensions=["jinja2.ext.do"], trim_blocks=True)
		set_functions_context(t)
		m = t.make_module(context)

		try:
			value = m.tribut
		except AttributeError:
			value = 0

		if value:
			tributavel_value = rounded(value, precision)
			if is_diary:
				tributavel_value = tributavel_value*31
		else:
			tributavel_value = rounded(0, precision)

		return tributavel_value
	except:
		e_type = frappe.utils.encode(doc_struct.e_type)
		frappe.throw(_("Error in rule for Earning Type {}. Please check jinja2 syntax.".format(e_type)))


def calculate_deductions(doc_salary, totals, result_description, precision):


	deduct_docs = doc_salary.deductions

	tributavel = totals.tributavel
	iliquid = totals.iliquid
	doc_employee = frappe.get_doc("Employee", doc_salary.employee).as_dict()
	context = {"tributavel": tributavel, "iliquid": iliquid}
	context.update(doc_employee)
	context.update(doc_salary)

	for doc in deduct_docs:
		doc = frappe._dict(doc)
		d_type = frappe.utils.encode(doc.d_type)
		doc_dtype = frappe.get_doc("Deduction Type", d_type)
		make_deduction(doc_salary, doc_dtype, doc, context, result_description, precision)


def make_deduction(doc_salary, doc_type, doc_struct, context, result_description, precision):

	tributavel_calcule = doc_type.tributavel_expression

	if not result_description.get("deductions"):
		result_description["deductions"] = []

	if not tributavel_calcule:
		tributavel_value = rounded(doc_struct.d_modified_amt, precision)
		res = {"idx": doc_struct.idx, "d_modified_amt": tributavel_value}
		result_description.get("deductions").append(res)
		return tributavel_value

	doc_type_dict = doc_type.as_dict()

	for attr in ("tributavel_calcule", "parent", "parenttype", "parentfield", "owner", "modified_by"):
		doc_type_dict.pop(attr, None)
		doc_struct.pop(attr, None)
		doc_salary.pop(attr, None)

	#context.update({doc_type_dict.short_name: doc_type_dict})
	#context.update({doc_struct.short_name: doc_struct})

	context.update(doc_struct)
	context.update(doc_type_dict)

	try:
		t = Template(tributavel_calcule, extensions=["jinja2.ext.do"], trim_blocks=True)
		set_functions_context(t)
		m = t.make_module(context)

		#try:
		#if (doc_type.deduction_type == "Table"):
		#	print "table name %s date %s" % (doc_salary.earnings, doc_salary.from_date)
		#except:
		#	print "there is no table_name %s" % frappe.utils.encode(doc_employee.estado_civil)

		try:
			value = m.tribut
		except AttributeError:
			value = 0

		if value:
			tributavel_value = rounded(value, precision)
		else:
			tributavel_value = rounded(0, precision)

		res = {"idx": doc_struct.idx, "d_modified_amt": tributavel_value}
		context[doc_type_dict.short_name] = res
		result_description.get("deductions").append(res)
		print "short_name %s res %s idx %s tributavel_value %s" % (doc_type_dict.short_name, context.get(doc_type_dict.short_name), doc_struct.idx, tributavel_value)
		return tributavel_value
	except:
		d_type = frappe.utils.encode(doc_struct.d_type)
		frappe.throw(_("Error in rule for Earning Type {}. Please check jinja2 syntax.".format(d_type)))

