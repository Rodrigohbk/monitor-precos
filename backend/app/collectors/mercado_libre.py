from decimal import Decimal
from typing import Optional, Dict, Any
import re
from .base import BaseCollector

class MercadoLivreCollector(BaseCollector):
    async def fetch_price(self, product: Dict[str, Any]) -> Optional[Decimal]:
        source_id = product.get("source_id")
        if not source_id:
            # Tenta extrair da URL
            url = product.get("url", "")
            source_id = self._extract_id_from_url(url)

        if not source_id:
            return None

        # Chamada à API pública do Mercado Livre
        url = f"https://api.mercadolibre.com/items/{source_id}"
        # Se necessário, inclui token de acesso (se o usuário tiver)
        headers = {}
        if self.credentials.get("access_token"):
            headers["Authorization"] = f"Bearer {self.credentials['access_token']}"

        response = await self.client.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            price = data.get("price")
            if price:
                return Decimal(str(price))
        return None

    def _extract_id_from_url(self, url: str) -> Optional[str]:
        # Exemplo: https://www.mercadolivre.com.br/.../MLB123456
        match = re.search(r"MLB\d+", url)
        return match.group(0) if match else None