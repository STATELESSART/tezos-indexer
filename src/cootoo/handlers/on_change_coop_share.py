import cootoo.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from cootoo.types.coop.parameter.change_coop_share import ChangeCoopShareParameter
from cootoo.types.coop.storage import CoopStorage


async def on_change_coop_share(
    ctx: HandlerContext,
    change_coop_share: Transaction[ChangeCoopShareParameter, CoopStorage],
) -> None:
    
    coop = await models.Coop.filter(address = change_coop_share.data.target_address).get()
    new_share = int(change_coop_share.parameter.__root__)

    coop.coop_share = new_share
    await coop.save()