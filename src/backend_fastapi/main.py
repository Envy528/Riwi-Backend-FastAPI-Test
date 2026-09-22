from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

# ------------Models---------------------

# Model for creating a product
class CreateProduct(BaseModel):
    id: int
    name: str
    price: float = Field(gt=0, description="Price must be greater than zero")
    quantity: int = Field(ge=0, description="Quantity must be greater than or equal to zero")
    category: str
    
# Model for updating a product
class UpdateProduct(BaseModel):
    name: str = None
    price: float = Field(None, gt=0, description="Price must be greater than zero")
    quantity: int = Field(None, ge=0, description="Quantity must be greater than or equal to zero")
    category: str = None

# ----------------------------------------

# Array to store products in memory (already with sample data)
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

# See all products with optional query params
@app.get("/products", status_code=200)
def get_products(skip: int = Query(0, ge=0), limit: int = Query(5, ge=1), category: str | None = None, search: str | None = None):    
    result = products
    
    if category is not None:
        result = [p for p in result if p.category.lower() == category.lower()]
    
    if search is not None:
        result = [p for p in result if search.lower() in p.name.lower()]

    return {"products": result[skip:skip + limit]}

# Search a product by id
@app.get("/products/{id}", status_code=200)
def get_product(id: int):
    for product in products:
        if product.id == id:
            return {"message": "Product found",
                "found_product": product}
    raise HTTPException(status_code=404, detail=f"Product with id {id} not found")

# Create a new product
@app.post("/products", status_code=201)
def createproduct(product: CreateProduct):
    for existing_product in products:
        if existing_product.id == product.id:
            raise HTTPException(status_code=409, detail=f"Product with id {product.id} already exists")
        
    products.append(product)
    return {"message": "Product created successfully",
            "created_product": product}

# Update a product by id
@app.patch("/products/{id}", status_code=200)
def updateproduct(id: int, edited_product: UpdateProduct):
    for product in products:
        if product.id == id:
            if edited_product.name is not None:
                product.name = edited_product.name
            if edited_product.price is not None:
                product.price = edited_product.price
            if edited_product.quantity is not None:
                product.quantity = edited_product.quantity
            if edited_product.category is not None:
                product.category = edited_product.category
            return {"message": "Product updated successfully",
                    "updated_product": product}
    raise HTTPException(status_code=404, detail=f"Product with id {id} not found")

# Delete a product by id
@app.delete("/products/{id}", status_code=200)
def delete_product(id: int):
    for product in products:
        if product.id == id:
            products.remove(product)
            return {"message": "Product deleted successfully",
                    "deleted_product": product}
    raise HTTPException(status_code=404, detail=f"Product with id {id} not found")

# --------------------------------------------