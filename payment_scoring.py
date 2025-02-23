import stripe

def analyze_payment_risk(client_email):
    """Pulls Stripe data to check for late payment history"""
    charges = stripe.Charge.list(email=client_email)
    late_payments = sum(1 for charge in charges if charge['paid'] is False)
    return {"client_email": client_email, "late_payments": late_payments}

