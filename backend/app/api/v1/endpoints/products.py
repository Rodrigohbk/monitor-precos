from typing import List
from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.product import ProductOut  # (criaremos)

router = APIRouter(prefix="/products", tags=["produtos"])

# Dados mockados
fake_products = [
    {"id": 1, "name": "Notebook Gamer", "price": 4500.00},
    {"id": 2, "name": "Mouse sem fio", "price": 89.90},
    {"id": 3, "name": "Teclado mecânico", "price": 350.50},
]

@router.get("/", response_model=List[ProductOut])
async def list_products(current_user: User = Depends(get_current_active_user)):
    """Retorna uma lista de produtos mockados (apenas para usuários autenticados)."""
    return fake_products