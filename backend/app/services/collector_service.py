from typing import Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Product, PriceHistory, SourceCredentials
from app.collectors.base import BaseCollector
from app.collectors.mercado_libre import MercadoLivreCollector
from app.collectors.web_scraper import WebScraperCollector
# from app.collectors.amazon_spapi import AmazonSPAPICollector
# from app.collectors.shopee import ShopeeCollector

class CollectorService:
    # Mapeamento source_type -> classe do coletor
    COLLECTOR_MAP: Dict[str, Type[BaseCollector]] = {
        "mercadolibre": MercadoLivreCollector,
        "web_scraping": WebScraperCollector,
        # "amazon": AmazonSPAPICollector,
        # "shopee": ShopeeCollector,
    }

    async def run_collection_for_all_active_products(self, db: AsyncSession):
        # 1. Buscar produtos ativos
        stmt = select(Product).where(Product.is_active == True)
        result = await db.execute(stmt)
        products = result.scalars().all()

        for product in products:
            # 2. Obter credenciais do usuário (se houver)
            cred_stmt = select(SourceCredentials).where(
                SourceCredentials.user_id == product.user_id,
                SourceCredentials.source_type == product.source_type
            )
            cred_result = await db.execute(cred_stmt)
            creds = cred_result.scalar_one_or_none()
            credentials = creds.credentials if creds else {}

            # 3. Selecionar o coletor
            collector_class = self.COLLECTOR_MAP.get(product.source_type)
            if not collector_class:
                # Se não temos coletor implementado, apenas pular
                continue

            # 4. Coletar preço
            async with collector_class(credentials) as collector:
                price = await collector.fetch_price(product.__dict__)

            # 5. Se obteve preço, salvar no histórico
            if price is not None:
                price_history = PriceHistory(
                    product_id=product.id,
                    price=price
                )
                db.add(price_history)
                product.last_collected_at = datetime.now(timezone.utc)
                await db.commit()
            else:
                # Opcional: registrar log de falha
                pass