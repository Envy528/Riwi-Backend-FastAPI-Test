from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ------------Models---------------------

# Model for creating a product
class CreateProduct(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    category: str
    
# Model for updating a product
class UpdateProduct(BaseModel):
    name: str = None
    price: float = None
    quantity: int = None
    category: str = None

# ----------------------------------------


products = [
    CreateProduct(id=1, name="24-inch LED Monitor", price=189.99, quantity=15, category="electronics"),
    CreateProduct(id=2, name="White Monitor Stand", price=24.50, quantity=40, category="accessories"),
    CreateProduct(id=3, name="Mechanical Keyboard", price=79.90, quantity=25, category="electronics"),
    CreateProduct(id=4, name="Wireless Mouse", price=29.99, quantity=60, category="electronics"),
    CreateProduct(id=5, name="Laptop Sleeve", price=19.75, quantity=35, category="accessories"),
    CreateProduct(id=6, name="Ergonomic Office Chair", price=149.00, quantity=8, category="furniture"),
    CreateProduct(id=7, name="Desk Lamp", price=34.20, quantity=22, category="furniture"),
]


# --------------endpoints-----------------

# 
@app.get("/products")
def get_products(skip: int = 0, limit: int = 5, category: str | None = None, search: str | None = None):    
    result = products
    
    if category is not None:
        result = [p for p in result if p.category.lower() == category.lower()]
    
    if search is not None:
        result = [p for p in result if search.lower() in p.name.lower()]

    return {"products": result[skip:skip + limit]}

# Search a product by id
@app.get("/products/{id}")
def get_product(id: int):
    for product in products:
        if product.id == id:
            return {"message": "Product found",
                "found_product": product}
    raise HTTPException(status_code=404, detail=f"Product with id {id} not found")

# Create a new product
@app.post("/products")
def create_product(product: CreateProduct):
    products.append(product)
    return {"message": "Product created successfully",
            "created_product": product}

# Update a product by id
@app.patch("/products/{id}")
def update_product(id: int, editedProduct: UpdateProduct):
    for product in products:
        if product.id == id:
            if editedProduct.name is not None:
                product.name = editedProduct.name
            if editedProduct.price is not None:
                product.price = editedProduct.price
            if editedProduct.quantity is not None:
                product.quantity = editedProduct.quantity
            if editedProduct.category is not None:
                product.category = editedProduct.category
            return {"message": "Product updated successfully",
                    "updated_product": product}
    raise HTTPException(status_code=404, detail=f"Product with id {id} not found")

# Delete a product by id
@app.delete("/products/{id}")
def delete_product(id: int):
    for product in products:
        if product.id == id:
            products.remove(product)
            return {"message": "Product deleted successfully",
                    "deleted_product": product}
    raise HTTPException(status_code=404, detail=f"Product with id {id} not found")

# --------------------------------------------