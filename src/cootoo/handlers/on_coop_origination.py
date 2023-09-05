import cootoo.models as models
from cootoo.types.coop.storage import CoopStorage
from dipdup.context import HandlerContext
from dipdup.models import Origination
from cootoo.metadata_utils import get_holder_profile

# import requests, json

async def on_coop_origination(
    ctx: HandlerContext,
    coop_origination: Origination[CoopStorage],
) -> None:

    contract_address = coop_origination.data.originated_contract_address
    coop_share = coop_origination.data.storage['coop_share']
    # manager, _ = await models.Holder.get_or_create(address=coop_origination.data.storage['manager'])
    manager = await get_holder_profile(coop_origination.data.storage['manager'])
    members = coop_origination.data.storage['members']    

    coop = models.Coop(
        address = contract_address, 
        manager = manager,
        coop_share = int(coop_share),
        ophash=coop_origination.data.hash,
        level=coop_origination.data.level,
        timestamp=coop_origination.data.timestamp
    )
    await coop.save()

    ctx.logger.info(members)
    for member_address in members:
        # member, _ = await models.Holder.get_or_create(address=member_address)
        member = await get_holder_profile(member_address)
        coop_member, _ = await models.CoopMember.get_or_create(
            member = member,
            coop = coop,
            tez_received = 0,
            status = models.MemberStatus.ACTIVE,
            ophash=coop_origination.data.hash,
            level=coop_origination.data.level,
            timestamp=coop_origination.data.timestamp,
        )
        await coop_member.save()
