import cootoo.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from cootoo.types.coop.parameter.delete_member import DeleteMemberParameter
from cootoo.types.coop.storage import CoopStorage


async def on_delete_member(
    ctx: HandlerContext,
    delete_member: Transaction[DeleteMemberParameter, CoopStorage],
) -> None:
    
    coop = await models.Coop.get(address = delete_member.data.target_address)

    member_address = delete_member.parameter.__root__
    member, _ = await models.Holder.get_or_create(address = member_address)

    coop_member = await models.CoopMember.get(
            member = member,
            coop = coop
        )
    coop_member.status = models.MemberStatus.INACTIVE
    await coop_member.save()
