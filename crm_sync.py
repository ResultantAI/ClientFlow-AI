import requests

def sync_with_hubspot(icp_score, client_email):
    """Sends ICP Score to HubSpot CRM"""
    payload = {
        "email": client_email,
        "custom_icp_score": icp_score
    }
    response = requests.post("https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/",
                             json=payload)
    return response.status_code

