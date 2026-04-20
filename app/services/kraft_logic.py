
import pandas as pd

CLASS_START = "2015-08-27"
CLASS_END = "2019-02-21"

def calculate_kraft_loss(row):
    purchase_price = float(row.get("purchase_price", 0) or 0)
    sale_price = float(row.get("sale_price", 0) or 0)
    quantity = float(row.get("quantity", 1) or 1)

    purchase_date = str(row.get("purchase_date", ""))

    total_investment = purchase_price * quantity
    total_sale = sale_price * quantity

    # Eligibility
    if not (CLASS_START <= purchase_date <= CLASS_END):
        return pd.Series({
            "recognized_loss": 0,
            "eligible": False,
            "loss_type": "Not Eligible",
            "holding_status": "N/A",
            "total_investment": total_investment,
            "total_sale": total_sale
        })

    # More realistic logic
    price_diff = purchase_price - sale_price

    if price_diff <= 0:
        loss = 0
        loss_type = "No Loss"
    else:
        # cap logic (important for interview)
        capped_loss = min(price_diff, purchase_price * 0.3)
        loss = capped_loss * quantity
        loss_type = "Capped Loss Applied"

    return pd.Series({
        "recognized_loss": loss,
        "eligible": True,
        "loss_type": loss_type,
        "holding_status": "Sold" if sale_price else "Holding",
        "total_investment": total_investment,
        "total_sale": total_sale
    })