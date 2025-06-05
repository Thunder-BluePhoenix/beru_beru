import frappe
from frappe import _
from datetime import datetime
from dateutil.relativedelta import relativedelta

def age_update(doc, method=None):
    print("learn python@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    for data in doc.custom_customer_details:
        if data.dob:
            print("dob", data.dob)
            
            # Calculate age
            age_data = calculate_age(data.dob)
            
            # Update the age fields (assuming you have these fields in your child table)
            # data.age_years = age_data['years']
            # data.age_months = age_data['months'] 
            # data.age_days = age_data['days']
            data.age = age_data['age_string']
            data.age_category = age_data['age_category']
            
            print(f"Age calculated: {age_data['age_string']}, Category: {age_data['age_category']}")

def calculate_age(birth_date):
    """
    Calculate age in years, months, and days from birth date
    """
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    today = datetime.now().date()
    
    # Calculate the difference using relativedelta
    age_diff = relativedelta(today, birth_date)
    
    years = age_diff.years
    months = age_diff.months
    days = age_diff.days
    
    # Create a formatted age string
    age_parts = []
    if years > 0:
        age_parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months > 0:
        age_parts.append(f"{months} month{'s' if months != 1 else ''}")
    if days > 0:
        age_parts.append(f"{days} day{'s' if days != 1 else ''}")
    
    age_string = ", ".join(age_parts) if age_parts else "0 days"
    
    # Determine age category based on years
    age_category = get_age_category(years)
    
    return {
        'years': years,
        'months': months,
        'days': days,
        'age_string': age_string,
        'age_category': age_category
    }

def get_age_category(years):
    """
    Determine age category based on age in years
    Age categories:
    - Infant: 0-2 years
    - Child: 3-17 years  
    - Adult: 18-59 years
    - Senior citizen: 60+ years
    """
    if years <= 2:
        return "Infant"
    elif 3 <= years <= 17:
        return "Child"
    elif 18 <= years <= 59:
        return "Adult"
    else:  # 60 and above
        return "Senior citizen"

# Alternative method if you want to use only standard library (without dateutil)
def calculate_age_manual(birth_date):
    """
    Calculate age manually without dateutil library
    """
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    today = datetime.now().date()
    
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day
    
    # Adjust for negative days
    if days < 0:
        months -= 1
        # Get the last day of the previous month
        if today.month == 1:
            prev_month = 12
            prev_year = today.year - 1
        else:
            prev_month = today.month - 1
            prev_year = today.year
        
        from calendar import monthrange
        days_in_prev_month = monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
    
    # Adjust for negative months
    if months < 0:
        years -= 1
        months += 12
    
    # Create a formatted age string
    age_parts = []
    if years > 0:
        age_parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months > 0:
        age_parts.append(f"{months} month{'s' if months != 1 else ''}")
    if days > 0:
        age_parts.append(f"{days} day{'s' if days != 1 else ''}")
    
    age_string = ", ".join(age_parts) if age_parts else "0 days"
    
    return {
        'years': years,
        'months': months,
        'days': days,
        'age_string': age_string
    }


#new button add in toolbar
# @frappe.whitelist()
# def create_opp(doc, method=None):
#     lead=frappe.get_doc("Lead",doc)
#     opp=frappe.new_doc("Opportunity")
#     opp.opportunity_from="Lead"
#     opp.party_name=lead.name
#     opp.save()
#     frappe.db.commit()



@frappe.whitelist()
def create_opp(doc, method=None):
    try:
        # Get the lead document
        lead = frappe.get_doc("Lead", doc)
        
        # Validate lead status (but allow multiple opportunities)
        if lead.status in ["Do Not Contact", "Lost"]:
            frappe.throw(f"Cannot create opportunity for lead with status: {lead.status}")
        
        # Create new opportunity
        opp = frappe.new_doc("Opportunity")
        
        # Copy relevant fields from lead to opportunity
        opp.opportunity_from = "Lead"
        opp.party_name = lead.name
        opp.customer_name = lead.lead_name
        opp.opportunity_type = "Sales"
        opp.source = lead.source
        opp.contact_email = lead.email_id
        opp.contact_mobile = lead.mobile_no
        opp.territory = lead.territory or frappe.defaults.get_defaults().territory
        opp.company = lead.company or frappe.defaults.get_defaults().company
        
        # Copy child table data from lead to opportunity
        if lead.custom_customer_details:
            for customer_detail in lead.custom_customer_details:
                # Create new row in opportunity's child table
                opp_customer_row = opp.append("custom_customer_data", {})
                opp_customer_row.customer_name = customer_detail.customer_name
                opp_customer_row.id_card = customer_detail.id_card
                opp_customer_row.dob = customer_detail.dob
                # Add any other fields that exist in both tables
        
        existing_count = frappe.db.count("Opportunity", {
            "opportunity_from": "Lead",
            "party_name": lead.name
        })
        
        opp.save()
        
        # Commit transaction
        frappe.db.commit()
        
        return {
            "status": "success",
            "opportunity_name": opp.name,
            "opportunity_count": existing_count + 1,
            "message": f"Opportunity {opp.name} created successfully (#{existing_count + 1} for this lead)"
        }
        
    except frappe.DoesNotExistError:
        frappe.throw(f"Lead {doc} does not exist")
    except frappe.ValidationError as e:
        frappe.throw(f"Validation Error: {str(e)}")
    except Exception as e:
        frappe.log_error(f"Error creating opportunity from lead {doc}: {str(e)}")
        frappe.throw(f"Failed to create opportunity: {str(e)}")