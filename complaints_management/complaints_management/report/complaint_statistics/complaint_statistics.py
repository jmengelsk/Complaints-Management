# Copyright (c) 2022, Josef Engelskirchen and contributors
# For license information, please see license.txt

import frappe
import datetime

def execute(filters=None):
    columns = [
        {'fieldname':'date','label':'Complaint Date','fieldtype':'Date'},
        {'fieldname':'name','label':'Complaint Nr','fieldtype':'Data'},
	{'fieldname':'customer','label':'Customer','fieldtype':'Data'}
    ]
    data = frappe.db.get_all('Complaint', ['date','name','customer'])
#    message = ["The equivalent of the letters 'cats' in numbers is '2287'"]
    return columns, data
