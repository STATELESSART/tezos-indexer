import cootoo.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from cootoo.types.coop.parameter.accept_manager import AcceptManagerParameter
from cootoo.types.coop.storage import CoopStorage
from cootoo.metadata_utils import get_holder_profile

async def on_new_coop_manager(
    ctx: HandlerContext,
    accept_manager: Transaction[AcceptManagerParameter, CoopStorage],
) -> None:
    
    coop = await models.Coop.filter(address = accept_manager.data.target_address).get()
    # manager, _ = await models.Holder.get_or_create(address = accept_manager.data.sender_address)
    manager = await get_holder_profile(accept_manager.data.sender_address)
    coop.manager = manager
    await coop.save()