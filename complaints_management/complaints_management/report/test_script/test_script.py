# Copyright (c) 2022, Josef Engelskirchen and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    #frappe.msgprint("<pre>{}</pre>".format(filters))
    columns = [
        {'fieldname':'date','label':'Date','fieldtype':'Date'},
	{'fieldname':'name','label':'Complaint Nr','fieldtype':'Data'},
	{'fieldname':'complaint_status','label':'Status','fieldtype':'Select'},
	{'fieldname':'customer','label':'Customer','fieldtype':'Data'}
	]
	
    data = frappe.db.get_all('Complaint', ['date','name','complaint_status','customer'])

    return columns, data
