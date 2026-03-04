import os
import resend

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

def send_best_price_email(recipient_email: str, results: list):
    """
    Sends an email to the recipient with the best prices found using Resend API.
    """
    if not RESEND_API_KEY:
        print("RESEND_API_KEY is missing. Cannot send email.")
        return False
        
    html_body = f"""
    <html>
    <body style="font-family: sans-serif; color: #333; line-height: 1.6;">
        <h2 style="color: #2c3e50;">Your Grocery Price Aggregation Results 🛒</h2>
        <p>Here are the best prices we found for the items on your list:</p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
    """
    
    for item in results:
        query = item.get("query", "")
        # Enforce proper casing (Title Case)
        query_display = query.title() if query else "Unknown Item"
        best_data = item.get("best_option")
        
        html_body += f'<h3 style="color: #2980b9; margin-bottom: 5px;">🛒 <u>{query_display}</u></h3>'

        # Check for explicitly blocked non-grocery queries (e.g. "Samsung", "TV")
        if isinstance(best_data, dict) and best_data.get("error") == "blocked_category":
            html_body += f"<p style='color: #e74c3c; font-weight: bold;'>We return results for grocery products only.</p><br>"
            continue

        if not best_data or not best_data.get("prices_by_store"):
            html_body += f"<p><i>No results found for {query_display}.</i></p><br>"
            continue
            
        prices_by_store = best_data.get("prices_by_store", {})
        
        # Store Map for Emojis
        store_emojis = {
            "Walmart": "🔵 Walmart",
            "Target": "🔴 Target",
            "Instacart": "🥕 Instacart"
        }
        
        html_body += "<ul>"
        for store in ["Walmart", "Target", "Instacart"]:
            top_items = prices_by_store.get(store, [])
            store_name = store_emojis.get(store, store)
            
            if top_items:
                html_body += f"<li style='margin-bottom: 5px;'><strong>{store_name}</strong>: <ul>"
                for idx, store_item in enumerate(top_items):
                    name = store_item.get('name', '').title()
                    price = store_item.get('price', '$0.00')
                    link = store_item.get('link', '#')
                    
                    # Create hyperlinked "Link" text
                    html_body += f"<li>{price} - <i>{name}</i> (<a href='{link}' style='color: #3498db; text-decoration: none;'>Link</a>)</li>"
                html_body += "</ul></li>"
            else:
                html_body += f"<li><strong>{store_name}</strong>: -</li>"
        html_body += "</ul>"
                
        best_overall = best_data.get("best_overall")
        if best_overall and best_overall.get("savings_amount") > 0:
            html_body += f"<p style='background-color: #f8f9fa; padding: 10px; border-left: 4px solid #f1c40f;'>"
            html_body += f"🏆 <strong>Best place to buy: {best_overall['store']}!</strong><br>"
            html_body += f"💡 You will save <strong>${best_overall['savings_amount']} ({best_overall['savings_percentage']}%)</strong> compared to the most expensive option."
            html_body += f"</p>"
        elif best_overall:
            html_body += f"<p style='background-color: #f8f9fa; padding: 10px; border-left: 4px solid #f1c40f;'>"
            html_body += f"🏆 <strong>Best place to buy: {best_overall['store']}!</strong>"
            html_body += f"</p>"
            
        html_body += "<br>"

    html_body += "</body></html>"
        
    try:
        email_params = {
            "from": "Grocery Aggregator <onboarding@resend.dev>",
            "to": [recipient_email],
            "subject": "🛒 Your Grocery Best Prices - Results",
            "html": html_body
        }
        
        resend.Emails.send(email_params)
        return True
    except Exception as e:
        print(f"Failed to send email via Resend: {e}")
        return False
