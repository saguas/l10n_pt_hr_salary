# -*- coding: utf-8 -*-

import frappe


"""
@frappe.whitelist()
def calculate_earnings_description_old(earn_docs):

	iliquid = 0
	tributavel = 0
	earn_docs = json.loads(earn_docs)
	earnings_description = frappe._dict({
		"tributavel": [],
		"totals": [],
	})

	for doc in earn_docs:
		doc = frappe._dict(doc)
		e_type = frappe.utils.encode(doc.e_type)
		doc_etype = frappe.get_doc("Earning Type", e_type)
		incidence_base = frappe.utils.encode(doc_etype.incidence_base)
		modified_value = doc.modified_value
		iliquid += modified_value
		if incidence_base == "Tributável":
			precision = 2
			tribut_value = get_tributavel_value(doc_etype, doc, precision)
			if not tribut_value:
				tribut_value = modified_value
			earnings_description.tributavel.append({"e_type": e_type, "value": tribut_value})
			tributavel += tribut_value

	earnings_description.totals.append({"iliquid": iliquid, "tributavel": tributavel})

	return earnings_description


def get_tributavel_value_old(doc_type, doc_struct, precision):

	tributavel_value = None
	tributavel_calcule = doc_type.tributavel_calcule
	trib_expr = tributavel_calcule and get_split(tributavel_calcule) or []
	is_diary = doc_type.diary_earning_

	values = get_values_from_expression(doc_type, doc_struct, trib_expr, is_diary=is_diary)

	if values:
		tributavel_value = calculate(values, precision)

	return tributavel_value



def get_values_from_expression(doc_type, doc_struct, expression_list, is_diary=False):

	values = []

	has_parents_f = 0

	for expr in expression_list:
		expr = expr.strip()
		print "exprs %s" % expr
		if expr.startswith("$(") or expr.startswith("($("):
			name = get_regexp_name(expr).strip()
			val = get_value_from_name(name, doc_type, doc_struct, is_diary=is_diary)
			if expr.startswith("($"):
				values.append("(")
				has_parents_f += 1
			values.append(val)
			if expr.endswith("))") and has_parents_f > 0:
				values.append(")")
				has_parents_f -= 1

		elif expr.startswith("$if(") or expr.startswith("($if("):
			result = get_regexp_if_expression(expr)
			if result:
				if result.group(1):
					exprss = result.group(1)
					i = 0
					start_symbol = get_symbol(i)
					expression = if_split(exprss, start_symbol)
					while not expression:
						i += 1
						start_symbol = get_symbol(i)
						expression = if_split(exprss, start_symbol)

					split_value = []
					for name in expression:
						name = name.strip()
						if re.match("^[a-zA-Z]+.*", name):
							val = get_value_from_name(name, doc_type, doc_struct, is_diary=is_diary)
							split_value.append(val)
						else:
							split_value.append(flt(name))

					l = len(split_value)
					if l == 2 and result.group(2):
						res = False
						s = "if %s %s %s: res=%s" % (split_value[0], start_symbol, split_value[1], True)
						exec(s)
						if res:
							v = process_expression(result.group(2).split(), doc_type, doc_struct, is_diary=is_diary)
							if expr.startswith("($if("):
								values.append("(")
								has_parents_f += 1
							values.extend(v)
							if expr.endswith("])") and has_parents_f > 0:
								values.append(")")
								has_parents_f -= 1

		elif expr in ("-", "+", "*", "/"):
			values.append(expr)
		elif expr.endswith(")") and has_parents_f > 0:
			values.append(")")
			has_parents_f -= 1
		else:
			values.append(expr)

	return values


def get_value_from_name(name, doc_etype, doc, is_diary=False):
	factor = 1

	if name:
		name = name.strip()
		if name == "valor":
			name = "modified_value"
		if name == "value_reference" and is_diary:
			factor = 31
		if doc.get(name):
			val = flt(getattr(doc, name, 0))*factor
		elif hasattr(doc_etype, name):
			val = flt(getattr(doc_etype, name, 0))*factor
		else:
			val = flt(0)
	else:
		val = flt(0)

	return val

def process_expression(expression, doc_type, doc_struct, is_diary=False):
	values = []

	for name in expression:
		print "name %s" % name
		has_parents_f = False
		has_parents_b = False
		if name.startswith("("):
			name = name[1:]
			has_parents_f = "("
		elif name.endswith(")"):
			name = name[:-1]
			has_parents_b = ")"
		if re.match("^[a-zA-Z]+.*", name):
			val = get_value_from_name(name, doc_type, doc_struct, is_diary=is_diary)
		elif name in ("-", "+", "*", "/"):
			val = name
		else:
			val = flt(name)
		if has_parents_f:
			val = "%s%s" %(has_parents_f, val)
		elif has_parents_b:
			val = "%s%s" %(val, has_parents_b)
		values.append(val)

	return values


def if_split(expr, symbol):
	result = expr.split(symbol)
	if len(result) == 1:
		result = []

	return result


def calculate(values, precision):

	value = "".join(str(x) for x in values)
	total = eval(value) or 0

	return rounded(total, precision)


def get_regexp_name(content):

	pattern = r"\(?\$\((.*?)\)"
	result = re.match(pattern, content, re.I | re.S)

	return result and result.group(1) or ""


def get_regexp_if_expression(content):

	pattern = r"\(?\$if\((.*?)\)(?:\[(.*)\])?"
	result = re.match(pattern, content, re.I | re.S)

	return result


def get_split(content):

	content = prepare_for_split(content)
	_if_split = []
	content_split = []

	in_if = False

	for s in content.strip().split():
		if s.startswith("$(") or s.startswith("($("):
			content_split.append(s)
			in_if = False
			continue
		elif s.startswith("$if(") or s.startswith("($if("):
			in_if = True
		elif not in_if:
			content_split.append(s)
			continue
		elif (s.endswith("]") or s.endswith("])")) and in_if:
			in_if = False
			_if_split.append(s)
			content_split.append(" ".join(_if_split))
			_if_split = []
			continue

		_if_split.append(s)

	return content_split


def prepare_for_split(content):

	pattern = r"([*+-/])"
	result = re.sub(pattern, " \\1 ", content, flags=re.I | re.S)
	return result

def get_symbol(pos):
	op = ["=", ">", "<", "!"]
	return op[pos]

"""