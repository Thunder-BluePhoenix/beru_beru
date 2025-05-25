// Copyright (c) 2025, rahul sarkar and contributors
// For license information, please see license.txt

frappe.ui.form.on("Lead", {
	refresh(frm) {
        setTimeout(function() {
            frm.remove_custom_button('Customer', 'Create');
            frm.remove_custom_button('Quotation', 'Create');
            frm.remove_custom_button('Prospect', 'Create');
            frm.remove_custom_button('Add to Prospect', 'Action');
        }, 500)

	},
});
