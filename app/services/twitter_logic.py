
import pandas as pd

CLASS_START = "2015-02-06"
CLASS_END = "2015-07-28"
DISCLOSURE_DATE = "2015-07-28"



def calculate_twitter_loss(row):
    try:
        purchase_price = float(row.get("purchase_price", 0) or 0)
        sale_price = float(row.get("sale_price", 0) or 0)
        quantity = float(row.get("quantity", 1) or 1)

        purchase_date = str(row.get("purchase_date", ""))
        sale_date = str(row.get("sale_date", ""))

        total_investment = purchase_price * quantity
        total_sale = sale_price * quantity

        if not ("2015-02-06" <= purchase_date <= "2015-07-28"):
            loss = 0
            eligible = False
            loss_type = "Not Eligible"
        else:
            eligible = True
            if sale_date and sale_date <= "2015-07-28":
                loss = max(0, purchase_price - sale_price) * quantity
                loss_type = "Pre-disclosure"
            else:
                loss = max(0, purchase_price - (sale_price * 0.9)) * quantity
                loss_type = "Post-disclosure"

        return pd.Series({
            "recognized_loss": loss,
            "eligible": eligible,
            "loss_type": loss_type,
            "holding_status": "Sold" if sale_date else "Holding",
            "total_investment": total_investment,
            "total_sale": total_sale
        })

    except Exception:
        return pd.Series({
            "recognized_loss": 0,
            "eligible": False,
            "loss_type": "Error",
            "holding_status": "N/A",
            "total_investment": 0,
            "total_sale": 0
        })
    

