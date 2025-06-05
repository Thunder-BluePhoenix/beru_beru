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


        //add button
        frm.add_custom_button(__('Create Opportunity'), function() {
            frappe.call({
                method: "beru_beru.beru_beru.overrides.lead.create_opp",
                args: {
                    doc: frm.doc.name
                },
                freeze: true,
                freeze_message: __('Creating Opportunity...'),
                callback: function(response) {
                    if (response.message) {
                        // Success
                        frappe.show_alert({
                            message: `Opportunity ${response.message} created successfully!`,
                            indicator: 'green'
                        }, 10);
                
                // Auto-navigate to opportunity
                setTimeout(() => {
                    frappe.set_route('Form', 'Opportunity', response.message);
                }, 2000);
                
            } else {
                frappe.msgprint(__('Opportunity creation failed or already exists.'));
            }
        }
    });
});
	},
});















frappe.ui.form.on('Opportunity', {
    travel_type: function(frm) {
        // Show/hide fields based on travel type
        if (frm.doc.travel_type === 'International') {
            frm.set_df_property('passport_required', 'hidden', 0);
            frm.set_df_property('visa_required', 'hidden', 0);
        } else {
            frm.set_df_property('passport_required', 'hidden', 1);
            frm.set_df_property('visa_required', 'hidden', 1);
        }
        
        if (frm.doc.travel_type === 'Corporate') {
            frm.set_df_property('company_name', 'hidden', 0);
            frm.set_df_property('employee_id', 'hidden', 0);
        } else {
            frm.set_df_property('company_name', 'hidden', 1);
            frm.set_df_property('employee_id', 'hidden', 1);
        }
    }
});