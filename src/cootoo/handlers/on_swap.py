import cootoo.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from cootoo.metadata_utils import fix_other_metadata, fix_token_metadata
from cootoo.types.cootoo_market.parameter.swap import SwapParameter
from cootoo.types.cootoo_market.storage import CootooMarketStorage
from cootoo.metadata_utils import get_holder_profile

async def on_swap(
    ctx: HandlerContext,
    swap: Transaction[SwapParameter, CootooMarketStorage],
) -> None:
    # holder, _ = await models.Holder.get_or_create(address=swap.data.sender_address)
    holder = await get_holder_profile(swap.data.sender_address)
    # token, _ = await models.Token.get_or_create(id=int(swap.parameter.objkt_id), fa2_address=swap.parameter.fa2_address)
    
    token_exists = await models.Token.exists(token_id=swap.parameter.objkt_id, fa2_address=swap.parameter.fa2_address)
    if not token_exists:
    
        # creator, _ = await models.Holder.get_or_create(address=swap.parameter.creator)
        
        token = models.Token(
            token_id=swap.parameter.objkt_id,
            fa2_address=swap.parameter.fa2_address,
            royalties=swap.parameter.royalties,
            title='',
            description='',
            artifact_uri='',
            display_uri='',
            thumbnail_uri='',
            metadata='',
            mime='',
            creator='',
            supply=0, #TODO: supply should be in fa2 contract
            level=swap.data.level,
            timestamp=swap.data.timestamp,
        )
        await token.save()

    else:
        token = await models.Token.get(token_id=swap.parameter.objkt_id, fa2_address=swap.parameter.fa2_address)


    seller_holding, _ = await models.TokenHolder.get_or_create(token=token, holder=holder, quantity=int(swap.parameter.objkt_amount))
    await seller_holding.save()

    await fix_token_metadata(token)
    await fix_other_metadata()

    swap_id = int(swap.storage.counter) - 1

    is_valid = swap.parameter.creator == token.creator_id and int(swap.parameter.royalties) == int(token.royalties)  # type: ignore

    swap_model = models.Swap(
        id=swap_id,  # type: ignore
        creator=holder,
        token=token,
        price=swap.parameter.xtz_per_objkt,
        amount=swap.parameter.objkt_amount,
        amount_left=swap.parameter.objkt_amount,
        status=models.SwapStatus.ACTIVE,
        ophash=swap.data.hash,
        level=swap.data.level,
        timestamp=swap.data.timestamp,
        royalties=swap.parameter.royalties,
        contract_version=1,
        is_valid=is_valid,
    )
    await swap_model.save()

    await fix_other_metadata()
    if not token.artifact_uri and not token.title:
        await fix_token_metadata(token)
