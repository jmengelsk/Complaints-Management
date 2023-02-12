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
                        complaint.cpldate,
                        complaint.customer,
                        complaint.complaint,
                        complaint.product,
                        complaint.rootcause,
                        complaint.actions,
                ]
                data.append(row1)

        sumcn = get_sumcn(filters)

        message = None

        if filters.language_filter == "English":
                message = ["<br>Choosen Filters are: "]
                message.append ("<br>")
                if filters.date_from_filter and filters.date_to_filter:
                        message += "Date Range: " + filters.date_from_filter + " to " + filters.date_to_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.status_filter:
                        message += "Status: " + filters.status_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.customer_filter:
                        message += "Customer: " + filters.customer_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.product_filter:
                        message += "Product: " + filters.product_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.rootcause_filter:
                        message += "Root Cause: " + filters.rootcause_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.approval_filter:
                        message += "Approved by: " + filters.approval_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")

        if filters.language_filter == "German":
                message = ["<br>Aktive Filter: "]
                message.append ("<br>")
                if filters.date_from_filter and filters.date_to_filter:
                        message += "Zeitraum: " + filters.date_from_filter + " bis " + filters.date_to_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.status_filter:
                        message += "Status: " + filters.status_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.customer_filter:
                        message += "Kunde: " + filters.customer_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.product_filter:
                        message += "Produkt: " + filters.product_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.rootcause_filter:
                        message += "Ursache: " + filters.rootcause_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")
                if filters.approval_filter:
                        message += "Genehmigt von: " + filters.approval_filter
                        message.append ("&nbsp;&nbsp;&nbsp;&nbsp;")

        chart = None

        if filters.language_filter == "English":
                report_summary = [
                        {
                                "label": "# of Items matching selection",
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
                                "label": "# Artikel entspr. Filter",
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
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Complaint"),
          "fieldname": "complaint",
          "fieldtype": "Data",
          "width": 265,
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Product"),
          "fieldname": "product",
          "fieldtype": "Data",
          "width": 300,
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Root Cause"),
          "fieldname": "rootcause",
          "fieldtype": "Data",
          "width": 120,
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Actions"),
          "fieldname": "actions",
          "width": 300,
          "fieldtype": "Data",
          "dropdown": False,
          "sortable": False,
       },
   ]


def get_columns_de():
    return [
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
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Reklamation"),
          "fieldname": "complaint",
          "fieldtype": "Data",
          "width": 265,
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Produkt"),
          "fieldname": "product",
          "fieldtype": "Data",
          "width": 300,
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Ursache"),
          "fieldname": "rootcause",
          "fieldtype": "Data",
          "width": 120,
          "dropdown": False,
          "sortable": False,
       },
       {
          "label": _("Massnahmen"),
          "fieldname": "actions",
          "width": 300,
          "fieldtype": "Data",
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
	if filters.get("status_filter"): conditions += " and complaint_status = %(status_filter)s"
	if filters.get("customer_filter"): conditions += " and customer = %(customer_filter)s"
	return conditions

def get_pfil(filters):
        pfil = ""
        pftemp1 = ""
        if filters.get("product_filter"):
                pftemp1 = "where pfilter = '" + filters.get("product_filter") + "'"
                pfil = pftemp1
        return pfil

def get_rcfil(filters):
        rcfil = ""
        if filters.get("rootcause_filter"): rcfil = "where rcfilter = %(rootcause_filter)s"
        return rcfil

def get_apfil(filters):
        apfil = ""
        if filters.get("approval_filter"): apfil = "where apfilter = %(approval_filter)s"
        return apfil

def get_complaints_en(filters):
    conditions=get_conditions(filters)
    pfil=get_pfil(filters)
    rcfil=get_rcfil(filters)
    apfil=get_apfil(filters)
    return frappe.db.sql(
    """select cpldate, cplnr, customer, complaint, product, rootcause, actions, status, pfilter from
       (select cpldate, cplnr, customer, complaint, product, rootcause, actions, status, apfilter, pfilter, rcfilter from
        (select cpldate, cplnr, customer, complaint, product, rootcause, actions, status, apfilter, pfilter, rcfilter from
            (select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item1_complaint_en as complaint,
                    item1_name_en as product,
                    item1_rootcause_en as rootcause,
                    item1_actions_en as actions,
                    complaint_status as status,
                    item1_name_en as pfilter,
                    item1_rootcause_en as rcfilter,
                    item1_approval_by as apfilter
            from `tabComplaint`
            where not item1_name_en = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item2_complaint_en as complaint,
                    item2_name_en as product,
                    item2_rootcause_en as rootcause,
                    item2_actions_en as actions,
                    complaint_status as status,
                    item2_name_en as pfilter,
                    item2_rootcause_en as rcfilter,
                    item2_approval_by as apfilter
            from `tabComplaint`
            where not item2_name_en = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item3_complaint_en as complaint,
                    item3_name_en as product,
                    item3_rootcause_en as rootcause,
                    item3_actions_en as actions,
                    complaint_status as status,
                    item3_name_en as pfilter,
                    item3_rootcause_en as rcfilter,
                    item3_approval_by as apfilter
            from `tabComplaint`
            where not item3_name_en = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item4_complaint_en as complaint,
                    item4_name_en as product,
                    item4_rootcause_en as rootcause,
                    item4_actions_en as actions,
                    complaint_status as status,
                    item4_name_en as pfilter,
                    item4_rootcause_en as rcfilter,
                    item4_approval_by as apfilter
            from `tabComplaint`
            where not item4_name_en = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item5_complaint_en as complaint,
                    item5_name_en as product,
                    item5_rootcause_en as rootcause,
                    item5_actions_en as actions,
                    complaint_status as status,
                    item5_name_en as pfilter,
                    item5_rootcause_en as rcfilter,
                    item5_approval_by as apfilter
            from `tabComplaint`
            where not item5_name_en = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item6_complaint_en as complaint,
                    item6_name_en as product,
                    item6_rootcause_en as rootcause,
                    item6_actions_en as actions,
                    complaint_status as status,
                    item6_name_en as pfilter,
                    item6_rootcause_en as rcfilter,
                    item6_approval_by as apfilter
            from `tabComplaint`
            where not item6_name_en = ''
            and %s ) t
            %s ) t
            %s ) t
            %s
            order by cplnr asc, status desc"""
           % (conditions,conditions,conditions,conditions,conditions,conditions,pfil,rcfil,apfil),
           filters,
           as_dict=1,
     )

def get_complaints_de(filters):
    conditions=get_conditions(filters)
    pfil=get_pfil(filters)
    rcfil=get_rcfil(filters)
    apfil=get_apfil(filters)
    return frappe.db.sql(
    """select cpldate, cplnr, customer, complaint, product, rootcause, actions, status, pfilter from
       (select cpldate, cplnr, customer, complaint, product, rootcause, actions, status, apfilter, pfilter, rcfilter from
        (select cpldate, cplnr, customer, complaint, product, rootcause, actions, status, apfilter, pfilter, rcfilter from
            (select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item1_complaint_de as complaint,
                    item1_name_de as product,
                    item1_rootcause_de as rootcause,
                    item1_actions_de as actions,
                    complaint_status as status,
                    item1_name_en as pfilter,
                    item1_rootcause_en as rcfilter,
                    item1_approval_by as apfilter
            from `tabComplaint`
            where not item1_name_de = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item2_complaint_de as complaint,
                    item2_name_de as product,
                    item2_rootcause_de as rootcause,
                    item2_actions_de as actions,
                    complaint_status as status,
                    item2_name_en as pfilter,
                    item2_rootcause_en as rcfilter,
                    item2_approval_by as apfilter
            from `tabComplaint`
            where not item2_name_de = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item3_complaint_de as complaint,
                    item3_name_de as product,
                    item3_rootcause_de as rootcause,
                    item3_actions_de as actions,
                    complaint_status as status,
                    item3_name_en as pfilter,
                    item3_rootcause_en as rcfilter,
                    item3_approval_by as apfilter
            from `tabComplaint`
            where not item3_name_de = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item4_complaint_de as complaint,
                    item4_name_de as product,
                    item4_rootcause_de as rootcause,
                    item4_actions_de as actions,
                    complaint_status as status,
                    item4_name_en as pfilter,
                    item4_rootcause_en as rcfilter,
                    item4_approval_by as apfilter
            from `tabComplaint`
            where not item4_name_de = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item5_complaint_de as complaint,
                    item5_name_de as product,
                    item5_rootcause_de as rootcause,
                    item5_actions_de as actions,
                    complaint_status as status,
                    item5_name_en as pfilter,
                    item5_rootcause_en as rcfilter,
                    item5_approval_by as apfilter
            from `tabComplaint`
            where not item5_name_de = ''
            and %s
            union all
            select cpldate,
                    name as cplnr,
                    customer_name as customer,
                    item6_complaint_de as complaint,
                    item6_name_de as product,
                    item6_rootcause_de as rootcause,
                    item6_actions_de as actions,
                    complaint_status as status,
                    item6_name_en as pfilter,
                    item6_rootcause_en as rcfilter,
                    item6_approval_by as apfilter
            from `tabComplaint`
            where not item6_name_de = ''
            and %s ) t
            %s ) t
            %s ) t
            %s
            order by cplnr asc, status desc"""
           % (conditions,conditions,conditions,conditions,conditions,conditions,pfil,rcfil,apfil),
           filters,
           as_dict=1,
     )

def get_sumcn(filters):
    conditions=get_conditions(filters)
    pfil=get_pfil(filters)
    apfil=get_apfil(filters)
    return frappe.db.sql(
    """select sum(cn_amount) from
          (select name, cn_amount, pfilter, apfilter from
           (select name,
                   item1_cn_amount as cn_amount,
                   item1_name_en as pfilter,
                   item1_approval_by as apfilter
           from `tabComplaint`
           where not item1_name_de = ''
           and %s
           union all
           select name,
                  item2_cn_amount as cn_amount,
                  item2_name_en as pfilter,
                  item2_approval_by as apfilter
           from `tabComplaint`
           where not item2_name_de = ''
           and %s
           union all
           select name,
                  item3_cn_amount as cn_amount,
                  item3_name_en as pfilter,
                  item3_approval_by as apfilter
           from `tabComplaint`
           where not item3_name_de = ''
           and %s
           union all
           select name,
                  item4_cn_amount as cn_amount,
                  item4_name_en as pfilter,
                  item4_approval_by as apfilter
           from `tabComplaint`
           where not item4_name_de = ''
           and %s
           union all
           select name,
                  item5_cn_amount as cn_amount,
                  item5_name_en as pfilter,
                  item5_approval_by as apfilter
           from `tabComplaint`
           where not item5_name_de = ''
           and %s
           union all
           select name,
                  item6_cn_amount as cn_amount,
                  item6_name_en as pfilter,
                  item6_approval_by as apfilter
           from `tabComplaint`
           where not item6_name_de = ''
           and %s ) t
          %s ) t
           %s"""
           % (conditions,conditions,conditions,conditions,conditions,conditions,pfil,apfil),
           filters,
           as_dict=0,
     )
