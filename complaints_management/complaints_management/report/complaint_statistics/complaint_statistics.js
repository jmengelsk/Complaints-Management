// Copyright (c) 2022, Josef Engelskirchen and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Complaint Statistics"] = {
	"filters": [
           {
              "fieldname":"posting_date",
              "label":("From Date"),
              "fieldtype":"Date",
              "default":get_today(),
             "reqd":1
          },
           {
              "fieldname":"posting_date",
              "label":("To Date"),
              "fieldtype":"Date",
              "default":get_today(),
             "reqd":1
          },
           {
              "fieldname":"supplier",
              "label":("Supplier"),
              "fieldtype":"Link",
              "options":"Supplier"
          },
           {
              "fieldname":"form_types",
              "label":("Form Type"),
              "fieldtype":"Select",
              "options":["","C-Form",H-Form"]
          }
	]
};
