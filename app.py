from flask import Flask, request, jsonify
from auth import get_current_user
from services.invoice_service import create_invoice
from services.report_service import generate_invoice_report
from cache import get_cache

app = Flask(__name__)

@app.route("/create", methods=["POST"])
def create():
    user = get_current_user()
    if not user:
        return "Unauthorized", 401

    create_invoice(
        user,
        request.json.get("amount"),
        request.json.get("description")
    )

    return "Created"

@app.route("/report")
def report():
    user = get_current_user()
    if not user:
        return "Unauthorized", 401

    invoice_id = request.args.get("invoice_id")
    org_context = request.args.get("org")

    cached = get_cache(f"report:{invoice_id}:{org_context}")
    if cached:
        return jsonify(cached)

    result = generate_invoice_report(user, invoice_id, org_context)

    if not result:
        return "Forbidden", 403

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
