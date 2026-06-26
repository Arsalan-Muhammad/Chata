from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Madina Super Store - POS Backend Panel",
    description="Interactive control panel for inventory and checkouts.",
    version="1.0"
)

# Your store's database simulation
INVENTORY = {
    "11111": {"name": "Lipton Tea 950g", "price": 1450.00, "stock": 25},
    "22222": {"name": "Dalda Cooking Oil 1L", "price": 520.00, "stock": 40}
}

# 1. Look up a single product
@app.get("/product/{barcode}", tags=["Inventory Management"])
def get_product_by_barcode(barcode: str):
    """
    Enter a product's barcode to instantly view its price and stock level.
    """
    if barcode not in INVENTORY:
        raise HTTPException(status_code=404, detail="Product not found in system!")
    return INVENTORY[barcode]

# 2. Process a quick sale
@app.post("/checkout", tags=["Sales & Billing"])
def process_customer_checkout(barcode: str, quantity: int):
    """
    Simulate scanning an item and entering a quantity to calculate the total bill.
    """
    if barcode not in INVENTORY:
        raise HTTPException(status_code=404, detail="Product not found!")
    
    product = INVENTORY[barcode]
    if product["stock"] < quantity:
        raise HTTPException(status_code=400, detail=f"Not enough stock! Only {product['stock']} left.")
    
    # Process sale logic
    product["stock"] -= quantity
    total_bill = product["price"] * quantity
    
    return {
        "status": "Success",
        "product_sold": product["name"],
        "quantity": quantity,
        "total_bill_pkr": total_bill,
        "remaining_stock": product["stock"]
    }
