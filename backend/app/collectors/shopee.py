from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional, Dict, Any
import httpx

class BaseCollector(ABC):
    """Classe base para todos os coletores de preços."""

    def __init__(self, credentials: Optional[Dict[str, Any]] = None):
        self.credentials = credentials or {}
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        await self.client.aclose()

    @abstractmethod
    async def fetch_price(self, product: Dict[str, Any]) -> Optional[Decimal]:
        """Retorna o preço atual como Decimal, ou None se falhar."""
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()