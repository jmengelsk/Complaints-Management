// Copyright (c) 2022, Josef Engelskirchen and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Complaint Details"] = {
	"filters": [
	   {
	      "fieldname":"date_from_filter",
	      "label":"From Date",
	      "fieldtype":"Date",
//	      "default":frappe.datetime.add_months(frappe.datetime.get_today(), -24)
              "default":"2019.01.01"
	   },
	   {
	      "fieldname":"date_to_filter",
	      "label":"To Date",
	      "fieldtype": "Date",
	      "default":frappe.datetime.get_today()
	   },
           {
              "fieldname":"status_filter",
              "label":("Complaint Status"),
              "fieldtype":"Select",
//              "options":["","Open","Closed"],
   	      "options": "Open\nClosed\nOnHold",
              "default": "Open"
          },
           {
              "fieldname":"customer_filter",
              "label":("Customer"),
              "fieldtype":"Link",
              "options": "Customers",
              "width": 350
          },
           {
              "fieldname":"product_filter",
              "label":("Product"),
              "fieldtype":"Link",
              "options": "GC Product",
          },
           {
              "fieldname":"rootcause_filter",
              "label":("Root Cause"),
              "fieldtype":"Link",
              "options": "Root Cause",
          },
           {
              "fieldname":"approval_filter",
              "label":("Approved by"),
//              "fieldtype":"Select",
//              "options": "\n\Ahmed Fouad\nKlaus",
//              "options":["","Ahmed Fouad","Klaus"],
//              "default": ""
              "fieldtype":"Link",
              "options": "Approvers",
          },
           {
              "fieldname":"language_filter",
              "label":("Report Language"),
              "fieldtype":"Select",
              "options": "\English\nGerman",
              "default": "\English"
          }
	],
//};
"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
            if (column.name == "C/N Amount"){
                                   if(data.cn_amount>1){
					var $value = $(value).css("background-color", "red");
					value = $value.wrap("<p></p>").parent().html();
                                    }
            }
            if (column.name == "GS Betrag"){
                                   if(data.cn_amount>1){
                                        var $value = $(value).css("background-color", "red");
                                        value = $value.wrap("<p></p>").parent().html();
                                    }
            }

            if (data.cn_amount) {
            }

            if (column.name == "Approved by") {
                                   if(data.approval_by == "Klaus"){
                                    value = "<span style='color:#ff00ff;font-weight:bold'>" + value + "</span>";
                                    }
            }
            if (column.name == "Genehmigt von") {
                                   if(data.approval_by == "Klaus"){
                                    value = "<span style='color:#ff00ff;font-weight:bold'>" + value + "</span>";
                                    }
            }

            if (data.approval_by) {
            }

        return value;
    },

};
