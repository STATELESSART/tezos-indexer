import cootoo.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from cootoo.types.cootoo_market.parameter.cancel_swap import CancelSwapParameter
from cootoo.types.cootoo_market.storage import CootooMarketStorage


async def on_cancel_swap(
    ctx: HandlerContext,
    cancel_swap: Transaction[CancelSwapParameter, CootooMarketStorage],
) -> None:
    swap = await models.Swap.filter(id=int(cancel_swap.parameter.__root__)).get()
    swap.status = models.SwapStatus.CANCELED
    swap.level = cancel_swap.data.level  # type: ignore
    await swap.save()
