frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // Add "Proforma Invoice" button if user has permission
        if (frappe.model.can_create("Proforma Invoice")) {
            frm.add_custom_button(
                __("Proforma Invoice"),
                () => {
                    frm.events.make_proforma_invoice(frm);
                },
                __("Create")
            );
        }
    },

    make_proforma_invoice: function(frm) {
        frappe.model.open_mapped_doc({
            method: "proforma_invoice_app.doctype.sales_order.sales_order.make_proforma_invoice",
            frm: frm
        });
    }
});
