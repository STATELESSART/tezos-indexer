import cootoo.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from cootoo.types.coop.parameter.default import DefaultParameter
from cootoo.types.coop.storage import CoopStorage
from cootoo.metadata_utils import get_holder_profile

async def on_tez_received(
    ctx: HandlerContext,
    transaction: Transaction[DefaultParameter, CoopStorage],
) -> None:

    amount = transaction.data.amount
    members_address = transaction.storage.members
    number_members = len(members_address)

    for address in members_address:
        # member, _ = await models.Holder.get_or_create(address = address)
        member = await get_holder_profile(address)
        coop_member = await models.CoopMember.get(coop_id = transaction.data.target_address, member = member)
        coop_member.tez_received += amount / number_members
        await coop_member.save() 
        

