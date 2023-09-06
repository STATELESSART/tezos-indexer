import cootoo.models as models
from typing import cast
from dipdup.context import HandlerContext
from cootoo.types.cootoo_market.storage import CootooMarketStorage
from cootoo.types.cootoo_market.parameter.create_coop import CreateCoopParameter
from dipdup.models import Transaction
from cootoo.metadata_utils import get_holder_profile

async def on_create_coop(
    ctx: HandlerContext,
    create_coop: Transaction[CreateCoopParameter, CootooMarketStorage],
) -> None:
    
    address = next(iter(create_coop.storage.coops))
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


    contract_address = originated_contract
    coop_share = create_coop.parameter.coop_share
    # manager, _ = await models.Holder.get_or_create(address=coop_origination.data.storage['manager'])
    manager = await get_holder_profile(create_coop.data.sender_address)
    members = create_coop.parameter.members + [create_coop.data.sender_address]
    
    coop = models.Coop(
        address = contract_address, 
        manager = manager,
        coop_share = int(coop_share),
        ophash=create_coop.data.hash,
        level=create_coop.data.level,
        timestamp=create_coop.data.timestamp
    )
    await coop.save()

    for member_address in members:
        # member, _ = await models.Holder.get_or_create(address=member_address)
        member = await get_holder_profile(member_address)
        coop_member, _ = await models.CoopMember.get_or_create(
            member = member,
            coop = coop,
            tez_received = 0,
            status = models.MemberStatus.ACTIVE,
            ophash=create_coop.data.hash,
            level=create_coop.data.level,
            timestamp=create_coop.data.timestamp,
        )
        await coop_member.save()

    