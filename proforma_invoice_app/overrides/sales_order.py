import frappe
from frappe import _

@frappe.whitelist()
def make_proforma_invoice(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc
    
    # ✅ First functionality
    sales_order = frappe.get_doc("Sales Order", source_name)
    for item in sales_order.items:
        remaining_qty = item.qty - (item.get("proforma_invoice_qty") or 0)
        if remaining_qty <= 0:
            frappe.throw(
                _("Cannot create Proforma Invoice because item {0} has no remaining quantity.")
                .format(item.item_code)
            )
    
    # ✅ Second functionality
    def set_missing_values(source, target):
        target.flags.ignore_permissions = True
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")
    
    return get_mapped_doc(
        "Sales Order",
        source_name,
        {
            "Sales Order": {
                "doctype": "Proforma Invoice",
                "field_map": {
                    "customer": "customer",
                    "name": "sales_order"
                },
                "validation": {
                    "docstatus": ["=", 1]
                }
            },
            "Sales Order Item": {
                "doctype": "Proforma Invoice Item",
                "field_map": {
                    "name": "so_detail",
                    "parent": "sales_order",
                    "qty": "qty"
                }
            }
        },
        target_doc,
        set_missing_values
    )
