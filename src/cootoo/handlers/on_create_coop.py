from typing import cast
from dipdup.context import HandlerContext
from dipdup.models import Origination
from cootoo.types.cootoo_market.storage import CootooMarketStorage
# import indexer.models as models

async def on_create_coop(
    ctx: HandlerContext,
    origination: Origination[CootooMarketStorage],
) -> None:
    
    ctx.logger.info(origination)
    address = origination.originated_contract_address
    originated_contract = cast(str, address)
    name = f'coop_template_{originated_contract}'
    await ctx.add_contract(
        name=originated_contract,
        address=originated_contract,
        typename='coop',
    )

    await ctx.add_index(
        name=name,
        template='coop_template',
        values={'contract': originated_contract},
    )

    