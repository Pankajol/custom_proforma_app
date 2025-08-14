frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Proforma Invoice"), function() {
                frappe.model.open_mapped_doc({
                    method: "proforma_invoice_app.proforma_invoice_app.doctype.proforma_invoice.proforma_invoice.make_proforma_invoice",
                    frm: frm
                });
            }, __("Create"));
        }
    }
});
