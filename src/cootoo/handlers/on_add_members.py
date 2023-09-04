import cootoo.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from cootoo.types.coop.parameter.add_members import AddMembersParameter
from cootoo.types.coop.storage import CoopStorage


async def on_add_members(
    ctx: HandlerContext,
    add_member: Transaction[AddMembersParameter, CoopStorage],
) -> None:
    
    coop = await models.Coop.get(address = add_member.data.target_address)

    param = add_member.parameter.__root__
    ctx.logger.info(param)
    ctx.logger.info(type(param))

    # if type(param) == 'list':
    for address in param:

        member, _ = await models.Holder.get_or_create(address = address)
        await models.CoopMember.get_or_create(
            member = member,
            coop = coop,
            tez_received = 0,
            status = models.MemberStatus.ACTIVE,
            ophash=add_member.data.hash,
            level=add_member.data.level,
            timestamp=add_member.data.timestamp,
        )
    # else:
    #     member, _ = await models.Holder.get_or_create(address = param)
    #     await models.CoopMember.get_or_create(
    #         member = member,
    #         coop = coop,
    #         tez_received = 0,
    #         status = models.MemberStatus.ACTIVE,
    #         ophash=add_member.data.hash,
    #         level=add_member.data.level,
    #         timestamp=add_member.data.timestamp,
    #     )
    