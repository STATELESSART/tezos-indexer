# import indexer.models as models
from typing import cast
from dipdup.context import HandlerContext
from cootoo.types.cootoo_market.storage import CootooMarketStorage
from cootoo.types.cootoo_market.parameter.create_coop import CreateCoopParameter
from dipdup.models import Transaction

async def on_create_coop(
    ctx: HandlerContext,
    create_coop: Transaction[CreateCoopParameter, CootooMarketStorage],
) -> None:
    
    ctx.logger.info(create_coop)
    address = next(iter(create_coop.storage.coops))
    ctx.logger.info(address)
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

    