from decimal import Decimal
from typing import Optional, Dict, Any
import re
from bs4 import BeautifulSoup
from .base import BaseCollector

class WebScraperCollector(BaseCollector):
    async def fetch_price(self, product: Dict[str, Any]) -> Optional[Decimal]:
        url = product.get("url")
        selector = product.get("price_selector")
        if not url or not selector:
            return None

        response = await self.client.get(url)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        element = soup.select_one(selector)
        if element:
            price_text = element.get_text(strip=True)
            # Extrai o primeiro número (ex.: "R$ 1.234,56" -> 1234.56)
            match = re.search(r"[\d.,]+", price_text.replace(".", "").replace(",", "."))
            if match:
                return Decimal(match.group(0))
        return None