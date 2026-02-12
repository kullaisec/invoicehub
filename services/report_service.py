from services.invoice_service import get_invoice
from services.org_service import user_in_org
from cache import set_cache, get_cache

def generate_invoice_report(user, invoice_id, org_context=None):
    invoice = get_invoice(invoice_id)
    if not invoice:
        return None

    effective_org = org_context if org_context else invoice["org_id"]

    if not user_in_org(user, effective_org):
        return None

    if user["role"] not in ["accountant", "admin"]:
        return None

    report = {
        "invoice_id": invoice["id"],
        "org": effective_org,
        "amount": invoice["amount"],
        "description": invoice["description"]
    }

    set_cache(f"report:{invoice_id}:{effective_org}", report)

    return report
