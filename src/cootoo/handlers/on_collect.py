import cootoo.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from cootoo.types.cootoo_market.parameter.collect import CollectParameter
from cootoo.types.cootoo_market.storage import CootooMarketStorage
from cootoo.metadata_utils import get_holder_profile

async def on_collect(
    ctx: HandlerContext,
    collect: Transaction[CollectParameter, CootooMarketStorage],
) -> None:
    swap = await models.Swap.filter(id=int(collect.parameter.__root__)).get()
    seller = await swap.creator
    # buyer, _ = await models.Holder.get_or_create(address=collect.data.sender_address)
    buyer = await get_holder_profile(collect.data.sender_address)
    token = await swap.token.get()  # type: ignore
 
    trade = models.Trade(
        swap=swap,
        seller=seller,
        buyer=buyer,
        token=token,
        amount=1,
        ophash=collect.data.hash,
        level=collect.data.level,
        timestamp=collect.data.timestamp,
    )
    await trade.save()

    swap.amount_left -= 1  # type: ignore
    if swap.amount_left == 0:
        swap.status = models.SwapStatus.FINISHED
    await swap.save()

    seller_holding, _ = await models.TokenHolder.get_or_create(token=token, holder=seller)
    seller_holding.quantity -= 1
    await seller_holding.save()

    buyer_holding, _ = await models.TokenHolder.get_or_create(token=token, holder=buyer)
    buyer_holding.quantity += 1
    await buyer_holding.save()
