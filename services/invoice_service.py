from db import get_db
from cache import get_cache, set_cache

def create_invoice(user, amount, description):
    db = get_db()
    db.execute(
        "INSERT INTO invoices (owner_id, org_id, amount, description) VALUES (?, ?, ?, ?)",
        (user["id"], user["org_id"], amount, description)
    )
    db.commit()

def get_invoice(invoice_id):
    cached = get_cache(f"invoice:{invoice_id}")
    if cached:
        return cached

    db = get_db()
    invoice = db.execute(
        "SELECT * FROM invoices WHERE id = ?",
        (invoice_id,)
    ).fetchone()

    if invoice:
        set_cache(f"invoice:{invoice_id}", invoice)

    return invoice
