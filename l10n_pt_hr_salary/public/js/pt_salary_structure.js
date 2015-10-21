var iliquid = 0;
var iliquid_tribut = null;

frappe.ui.form.on("Salary Structure Earning", "earnings_remove", function(frm, doctype, name){

	console.log("remove salary structure earning ", frm.doc, doctype, frm.doc.earnings.length);
	//if (cur_frm.cur_grid.fields_dict.e_type.value && cur_frm.cur_grid.fields_dict.e_type.value !== "")
	calculate_iliquid_tributavel_value(frm.doc, doctype);

});


//earnings
frappe.ui.form.on("Salary Structure", "earnings_on_form_rendered", function(frm, doctype, name){

	//get_regexp_if_expression("$if(game=teste)");
	//get_regexp_name("$if(game=teste)");
	//console.log("earnings_on_form_rendered ", cur_frm.cur_grid.doc.doctype, cur_frm.cur_grid.doc.name);
	cur_frm.cur_grid.refresh();
	if (cur_frm.cur_grid.fields_dict.e_type.value && cur_frm.cur_grid.fields_dict.e_type.value !== ""){
		iliquid_tribut = null;
		grid_from_open(frm, cur_frm.cur_grid.doc.doctype, cur_frm.cur_grid.doc.name, "Earning Type", 'earnings');
	}
});

frappe.ui.form.on("Salary Structure Earning", "e_type", function(frm, doctype, name){
	//console.log("earnings_on_form_rendered ", doctype);
	var row = locals[doctype][name];
	row.modified_value = undefined;
	if (row.e_type && row.e_type !== ""){
		grid_from_open(frm, doctype, name, "Earning Type", 'earnings');
	}
});

frappe.ui.form.on("Salary Structure Earning", "modified_value", function(frm, doctype, name){
	console.log("modified value ");
	calculate_iliquid_tributavel_value(frm.doc, doctype);
})

frappe.ui.form.on("Salary Structure Earning", "modified_value_diary", function(frm, doctype, name){
	var row = locals[doctype][name];

	//console.log("in modified diary ", typeof row.modified_value_diary);
	if (!row.modified_value_diary || typeof row.modified_value_diary === "object"){
		grid_from_open(frm, doctype, name, "Earning Type", 'earnings');
		return;
	}

	row.modified_value = flt(row.modified_value_diary * 31);
	refresh_field('modified_value', row.name, 'earnings');
	calculate_iliquid_tributavel_value(frm.doc, doctype);
});

//deductions

frappe.ui.form.on("Salary Structure", "deductions_on_form_rendered", function(frm, doctype, name){
	cur_frm.cur_grid.refresh();
	console.log("deductions_on_form_rendered ", doctype);
	if (cur_frm.cur_grid.fields_dict.d_type.value && cur_frm.cur_grid.fields_dict.d_type.value !== ""){
		if (iliquid_tribut == null){
			console.log("iliquid");
			calculate_iliquid_tributavel_value(cur_frm.doc, doctype, function(result){
				grid_from_open(frm, cur_frm.cur_grid.doc.doctype, cur_frm.cur_grid.doc.name, "Deduction Type", 'deductions');
			});
		}else{
			console.log("not iliquid");
			calculate(frm.doc, doctype, iliquid_tribut);
			grid_from_open(frm, cur_frm.cur_grid.doc.doctype, cur_frm.cur_grid.doc.name, "Deduction Type", 'deductions');
		}
	}
});


//Utils

var grid_from_open = function(frm, doctype, name, table_doctype, table_name){
	var row = locals[doctype][name];
	//console.log("Salary Structure Earning etype ", name);
	var dn = cur_frm.cur_grid.fields_dict.e_type && cur_frm.cur_grid.fields_dict.e_type.value || cur_frm.cur_grid.fields_dict.d_type && cur_frm.cur_grid.fields_dict.d_type.value;
	//hide_show_fields(frm.doc, row, table_doctype, dn, 'earnings');
	get_child_doc(frm.doc, row, table_doctype, dn, table_name);

}


var hide_show_fields_deductions = function(doc, row, dt, dn, table_field){

	depend_on_lwp(doc, row, table_field);

	if (doc.deduction_type === "Percentage"){
		cur_frm.cur_grid.fields_dict.percent.toggle(1);
		cur_frm.cur_grid.fields_dict.modified_value_percent.toggle(1);
		row.percent = 1;
		cur_frm.cur_grid.fields_dict.percent["df"].read_only = 1;
		row.modified_value_percent = doc.percent_value;
		cur_frm.cur_grid.fields_dict.modified_value_percent["df"].read_only = 1;
		refresh_field('percent', row.name, table_field);
		refresh_field('modified_value_percent', row.name, table_field);
		//refresh_field('modified_value', row.name, table_field);
		//cur_frm.cur_grid.refresh();
	}else if(doc.deduction_type === "Table"){
		cur_frm.cur_grid.fields_dict.percent.toggle(0);
		cur_frm.cur_grid.fields_dict.modified_value_percent.toggle(0);
	}else if(doc.deduction_type === "Fix"){
		cur_frm.cur_grid.fields_dict.percent.toggle(0);
		cur_frm.cur_grid.fields_dict.modified_value_percent.toggle(0);
	}else{
		cur_frm.cur_grid.fields_dict.percent.toggle(0);
		cur_frm.cur_grid.fields_dict.modified_value_percent.toggle(0);
	}

}


var depend_on_lwp = function(doc, row, table_field){

	cur_frm.cur_grid.fields_dict.depend_on_lwp["df"].read_only = 1;
	if(cint(doc.depend_on_lwp) == 1){
		row.depend_on_lwp = 1;
	}else{
		row.depend_on_lwp = 0;
	}

	refresh_field('depend_on_lwp', row.name, table_field);

}


var hide_show_fields_earnings = function(doc, row, dt, dn, table_field){

	depend_on_lwp(doc, row, table_field);

	if (doc.diary_earning_){
		cur_frm.cur_grid.fields_dict.diary_earning_.toggle(1);
		cur_frm.cur_grid.fields_dict.modified_value_diary.toggle(1);
		row.diary_earning_ = 1;
		cur_frm.cur_grid.fields_dict.diary_earning_["df"].read_only = 1;
		cur_frm.cur_grid.fields_dict.modified_value["df"].read_only = 1;
		refresh_field('diary_earning_', row.name, table_field);
		refresh_field('modified_value_diary', row.name, table_field);
		//refresh_field('modified_value_diary', row.name, table_field);
		//refresh_field('modified_value', row.name, table_field);
		//cur_frm.cur_grid.refresh();
	}else{
		cur_frm.cur_grid.fields_dict.diary_earning_.toggle(0);
		cur_frm.cur_grid.fields_dict.modified_value_diary.toggle(0);
		cur_frm.cur_grid.fields_dict.modified_value["df"].read_only = 0;
	}

}


var get_child_doc = function(doc, row, dt, dn, table_field){
	frappe.model.with_doc(dt, dn, function(name){
		var child_doc = locals[dt][dn];
		//console.log("hide_show ", dt, dn, child_doc);
		if (table_field === "earnings"){
			hide_show_fields_earnings(child_doc, row, dt, dn, table_field);
			calculate_earnings(doc, child_doc, row, dt, dn, table_field);
		}else{
			hide_show_fields_deductions(child_doc, row, dt, dn, table_field);
			//calculate_deductions(child_doc, row, dt, dn, table_field);
		}
	});
}


var calculate_earnings = function(doc, child_doc, row, dt, dn, table_field){

	var modified_value = child_doc.value_reference;
	if(child_doc.diary_earning_){
		if (!row.modified_value_diary || typeof row.modified_value_diary === "object"){
			row.modified_value_diary = modified_value;
		}
		row.modified_value = flt(row.modified_value_diary * 31);
	}else{
		if(!row.modified_value || typeof row.modified_value === "object"){
			row.modified_value = modified_value;
		}
	}
	//if (iliquid_tribut == null)
	calculate_iliquid_tributavel_value(doc, dt);
	refresh_field('modified_value_diary', row.name, table_field);
	refresh_field('modified_value', row.name, table_field);
}


var calculate_iliquid_tributavel_value = function(doc, doctype, callback){

	var tbl = doc.deductions || [];
	call_server_func("utils.calculate_tributavel.calculate_earnings_description", {doc: doc}, function(result){
		console.log("result 1 ", result.message);
		result = result.message;
		iliquid_tribut = result;
		calculate(doc, doctype, result);
		if (callback)
			callback(result);
	});
}

var calculate = function(doc, doctype, result){
	var tbl = doc.deductions || [];

	for(var i = 0; i < tbl.length; i++){
		tbl[i].d_modified_amt = flt(result.deductions[i].d_modified_amt);
		cur_frm.doc.deductions[i].d_modified_amt = tbl[i].d_modified_amt;
		refresh_field('d_modified_amt', cur_frm.doc.deductions[i].name, "deductions");
	}
	cur_frm.cscript.d_modified_amt(doc, doctype);
}


var call_server_func = function(method, args, callback){
	var args = args || {};

	frappe.call({
	       method: "l10n_pt_hr_salary." + method,
	       args: args,
	       callback: callback
     });

}

