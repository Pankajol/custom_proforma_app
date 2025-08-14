	
@frappe.whitelist()
def make_proforma_invoice(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc
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
                    "parent": "sales_order"
                }
            }
        },
        target_doc,
        set_missing_values
    )
@frappe.whitelist()
def make_proforma_invoice(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc
    # 1️⃣ Fetch the Sales Order and validate quantities
    sales_order = frappe.get_doc("Sales Order", source_name)
    for item in sales_order.items:
        # Remaining quantity = Ordered - already billed/delivered in proforma
        remaining_qty = item.qty - (item.get("proforma_invoice_qty") or 0)
        if remaining_qty <= 0:
            frappe.throw(
                _("Cannot create Proforma Invoice because item {0} has no remaining quantity.")
                .format(item.item_code)
            )
    # 2️⃣ Mapping function
    def set_missing_values(source, target):
        target.flags.ignore_permissions = True
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")
    # 3️⃣ Create the mapped document
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
                    "qty": "qty"  # change here if you want to map only remaining qty
                }
            }
        },
        target_doc,
        set_missing_values
    )
