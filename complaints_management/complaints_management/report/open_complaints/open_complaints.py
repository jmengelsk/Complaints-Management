
# Copyright (c) 2022, Josef Engelskirchen and contributors For license information, please see license.txt

import frappe
from frappe import _, msgprint


def execute(filters=None):
	if not filters:
		filters = {}

	if filters.language_filter == "English":
		complaints_list = get_complaints_en(filters)
		columns = get_columns_en()
	if filters.language_filter == "German":
		complaints_list = get_complaints_de(filters)
		columns = get_columns_de()


	if not complaints_list:
		msgprint(_("No record found"))
		return columns, complaints_list

	data = []

	for complaint in complaints_list:
		row1 = [
 #                       complaint.cplnr,
			complaint.cpldate,
			complaint.customer,
                        complaint.complaint,
			complaint.product,
                        complaint.rootcause,
			complaint.actions,
			complaint.status,
		]
		data.append(row1)

	sumcn = get_sumcn(filters)

	message = None
#	message = ["<br>Choosen Filters are "]
#	message.append("<br>Status Filter : " + filters.get("status_filter"))

	chart = None

	if filters.language_filter == "English":
		report_summary = [
			{
				"label": "# of Items with Complaints",
				"value": len(data),
				"datatype": "Data",
				"indicator": "Blue"
			},
			{
				"label": _("Total C/N Amount"),
				"indicator": "Green" if sum(sumcn[0]) < 1 else "Red",
				"value": sumcn,
				"datatype": "Currency",
				"currency": "EUR"
			}
		]

	if filters.language_filter == "German":
		report_summary = [
			{
				"label": "# Artikel mit Reklamationen",
				"value": len(data),
				"datatype": "Data",
				"indicator": "Blue"
			},
			{
				"label": _("Summe Gutschriften"),
				"indicator": "Green" if sum(sumcn[0]) < 1 else "Red",
				"value": sumcn,
				"datatype": "Currency",
				"currency": "EUR"
			}
		]


	return columns, data, message, chart, report_summary


def get_columns_en():
    return [
#       {
#         "label": _("Complaint Nr"),
#         "fieldname": "name",
#         "fieldtype": "Data",
#         "dropdown": False,
#         "sortable": False,
#       },
       {
          "label": _("Date"),
          "fieldname": "cpldate",
          "fieldtype": "Date",
          "width": 100,
          "dropdown": False,
          "sortable":False,
       },
       {
          "label": _("Customer"),
          "fieldname": "customer",
          "fieldtype": "Data",
          "width": 300,
          "dropdown": True,
          "sortable": True,
       },
       {
          "label": _("Issue"),
          "fieldname": "complaint",
          "fieldtype": "Data",
          "width": 265,
          "dropdown": True,
          "sortable": True,
       },
       {
          "label": _("Product"),
          "fieldname": "product",
          "fieldtype": "Data",
          "width": 300,
          "dropdown": True,
          "sortable": True,
       },
       {
          "label": _("Root Cause"),
          "fieldname": "rootcause",
          "fieldtype": "Data",
          "width": 120,
          "dropdown": True,
          "sortable": True,
       },
       {
          "label": _("Actions"),
          "fieldname": "actions",
          "width": 300,
          "fieldtype": "Data",
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Status"),
          "fieldname": "complaint_status",
          "fieldtype": "Data",
          "dropdown": False,
          "sortable": False,
       },
    ]


def get_columns_de():
    return [
#       {
#         "label": _("Reklamations Nr"),
#         "fieldname": "name",
#         "fieldtype": "Data",
#         "dropdown": False,
#         "sortable": False,
#       },
       {
          "label": _("Datum"),
          "fieldname": "cpldate",
          "fieldtype": "Date",
          "width": 100,
          "dropdown": False,
          "sortable":False,
       },
       {
          "label": _("Kunde"),
          "fieldname": "customer",
          "fieldtype": "Data",
          "width": 300,
          "dropdown": True,
          "sortable": True,
       },
       {
          "label": _("Artikel"),
          "fieldname": "product",
          "fieldtype": "Data",
          "width": 300,
          "dropdown": True,
          "sortable": True,
       },
       {
          "label": _("Reklamation"),
          "fieldname": "complaint",
          "fieldtype": "Data",
          "width": 265,
          "dropdown": True,
          "sortable": True,
       },
       {
          "label": _("Actions"),
          "fieldname": "actions",
          "fieldtype": "Data",
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("GS Betrag"),
          "fieldname": "cn_amount",
          "fieldtype": "Currency",
          "dropdown": False,
          "sortable": False,
       },
    ]


def get_conditions(filters):
	conditions = ""
	if filters.date_from_filter and filters.date_to_filter:
		if filters.date_from_filter > filters.date_to_filter:
			frappe.throw("The 'From Date' ({}) must be before the 'To Date' ({})".format(filters.date_from_filter, filters.date_to_filter))
	if filters.date_from_filter == None:
		filters.date_from_filter = "2019-01-01"
	if filters.date_to_filter == None:
		filters.date_to_filter = frappe.datetime.get_today()
	conditions = "cpldate between '" + filters.date_from_filter + "' and '" + filters.date_to_filter + "'"
	if filters.get("status_filter"): conditions += "and complaint_status = %(status_filter)s"
	if filters.get("customer_filter"): conditions += "and customer = %(customer_filter)s"
#	if filters.get("product_filter"): conditions += "and item1_code = %(product_filter)s"
#	if filters.get("approval_filter"): conditions += "and approval_by = %(approval_filter)s"
	return conditions

def get_pfil(filters):
	pfil = ""
	if filters.get("product_filter"): pfil = "where product_code = %(product_filter)s"
	return pfil

def get_pfilsum(filters):
        pfilsum = ""
        if filters.get("product_filter"): pfilsum = "and product_code = %(product_filter)s"
        return pfilsum

def get_complaints_en(filters):
    conditions=get_conditions(filters)
    pfil=get_pfil(filters)

    return frappe.db.sql(
    """select cpldate, cplnr, customer_name as customer, complaint, product, rootcause, actions, status from
           (select cpldate,
                   name as cplnr,
                   customer_name,
                   item1_complaint_en as complaint,
                   item1_name_en as product,
                   item1_rootcause_en as rootcause,
                   actions_en as actions,
                   complaint_status as status,
                   item1_code as product_code
           from `tabComplaint`
           where not item1_name_en = ''
           and %s
           union all
           select cpldate,
                   name as cplnr,
                   customer_name,
                   item2_complaint_en as complaint,
                   item2_name_en as product,
                   item2_rootcause_en as rootcause,
                   blank as actions,
                   blank as status,
                   item2_code as product_code
           from `tabComplaint`
           where  not item2_name_en = ''
           and %s
           union all
           select cpldate,
                   name as cplnr,
                   customer_name,
                   item3_complaint_en as complaint,
                   item3_name_en as product,
                   item3_rootcause_en as rootcause,
                   blank as actions,
                   blank as status,
                   item3_code as product_code
           from `tabComplaint`
           where not item3_name_en = ''
           and %s
           union all
           select cpldate,
                   name as cplnr,
                   customer_name,
                   item4_complaint_en as complaint,
                   item4_name_en as product,
                   item4_rootcause_en as rootcause,
                   blank as actions,
                   blank as status,
                   item4_code as product_code
           from `tabComplaint`
           where not item4_name_en = ''
           and %s
           union all
           select cpldate,
                   name as cplnr,
                   customer_name,
                   item5_complaint_en as complaint,
                   item5_name_en as product,
                   item5_rootcause_en as rootcause,
                   blank as actions,
                   blank as status,
                   item5_code as product_code
           from `tabComplaint`
           where not item5_name_en = ''
           and %s
           union all
           select cpldate,
                   name as cplnr,
                   customer_name,
                   item6_complaint_en as complaint,
                   item6_name_en as product,
                   item6_rootcause_en as rootcause,
                   blank as actions,
                   blank as status,
                   item6_code as product_code
           from `tabComplaint`
           where not item6_name_en = ''
           and %s ) t
           %s
           order by cplnr asc, status desc"""
           % (conditions,conditions,conditions,conditions,conditions,conditions,pfil),
           filters,
           as_dict=1,
     )

def get_complaints_de(filters):
    conditions=get_conditions(filters)
    pfil=get_pfil(filters)

    return frappe.db.sql(
    """select cpldate, name, customer_name as customer, approval_by, cn_amount, product, complaint from
           (select cpldate,
                   name,
                   customer_name,
                   approval_by,
                   cn_amount,
                   item1_code as product_code,
                   item1_name_de as product,
                   item1_complaint_de as complaint
           from `tabComplaint`
           where not item1_name_de = ''
           and %s
           union all
           select cpldate,
                  name,
                  customer_name,
                  blank as approval_by,
                  blank as cn_amount,
                  item2_code as product_code,
                  item2_name_de as product,
                  item2_complaint_de as complaint
           from `tabComplaint`
           where not item2_name_de = ''
           and %s
           union all
           select cpldate,
                  name,
                  customer_name,
                  blank as approval_by,
                  blank as cn_amount,
                  item3_code as product_code,
                  item3_name_de as product,
                  item3_complaint_de as complaint
           from `tabComplaint`
           where not item3_name_de = ''
           and %s
           union all
           select cpldate,
                  name,
                  customer_name,
                  blank as approval_by,
                  blank as cn_amount,
                  item4_code as product_code,
                  item4_name_de as product,
                  item4_complaint_de as complaint
           from `tabComplaint`
           where not item4_name_de = ''
           and %s
           union all
           select cpldate,
                  name,
                  customer_name,
                  blank as approval_by,
                  blank as cn_amount,
                  item5_code as product_code,
                  item5_name_de as product,
                  item5_complaint_de as complaint
           from `tabComplaint`
           where not item5_name_de = ''
           and %s
           union all
           select cpldate,
                  name,
                  customer_name,
                  blank as approval_by,
                  blank as cn_amount,
                  item6_code as product_code,
                  item6_name_de as product,
                  item6_complaint_de as complaint
           from `tabComplaint`
           where not item6_name_de = ''
           and %s ) t
           %s
           order by name asc, cn_amount desc"""
           % (conditions,conditions,conditions,conditions,conditions,conditions,pfil),
           filters,
           as_dict=1,
     )
def get_sumcn(filters):
    conditions=get_conditions(filters)
    pfil=get_pfil(filters)

    return frappe.db.sql(
    """select sum(cn_amount) from
           (select name,
                   cn_amount,
                   item1_code as product_code
           from `tabComplaint`
           where not item1_name_de = ''
           and %s
           union all
           select name,
                  blank_cur as cn_amount,
                  item2_code as product_code
           from `tabComplaint`
           where not item2_name_de = ''
           and %s
           union all
           select name,
                  blank_cur as cn_amount,
                  item3_code as product_code
           from `tabComplaint`
           where not item3_name_de = ''
           and %s
           union all
           select name,
                  blank_cur as cn_amount,
                  item4_code as product_code
           from `tabComplaint`
           where not item4_name_de = ''
           and %s
           union all
           select name,
                  blank_cur as cn_amount,
                  item5_code as product_code
           from `tabComplaint`
           where not item5_name_de = ''
           and %s
           union all
           select name,
                  blank_cur as cn_amount,
                  item6_code as product_code
           from `tabComplaint`
           where not item6_name_de = ''
           and %s ) t
           %s"""
           % (conditions,conditions,conditions,conditions,conditions,conditions,pfil),
           filters,
           as_dict=0,
     )
