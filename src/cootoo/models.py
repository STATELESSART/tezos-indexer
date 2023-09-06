from datetime import datetime
from enum import Enum, IntEnum

from tortoise import fields
from tortoise.fields.relational import ForeignKeyFieldInstance

from dipdup.models import Model


class SwapStatus(IntEnum):
    ACTIVE = 0
    FINISHED = 1
    CANCELED = 2

class MemberStatus(IntEnum):
    ACTIVE = 0
    INACTIVE = 1
    

class Holder(Model):
    address = fields.CharField(36, pk=True)
    name = fields.TextField(default='')
    # description = fields.TextField(default='')
    # metadata_file = fields.TextField(default='')
    # metadata = fields.JSONField(default={})


####################
# COOP Models #
####################

class Coop(Model):
    address = fields.CharField(36, pk=True)
    coop_share = fields.SmallIntField()
    manager: ForeignKeyFieldInstance[Holder] = fields.ForeignKeyField('models.Holder', 'manager', null=False, index=True)

    ophash = fields.CharField(51)
    level = fields.BigIntField()
    timestamp = fields.DatetimeField()


class CoopMember(Model):
    id = fields.BigIntField(pk=True)
    member: ForeignKeyFieldInstance[Holder] = fields.ForeignKeyField('models.Holder', 'member', null=False, index=True)
    coop: ForeignKeyFieldInstance[Coop] = fields.ForeignKeyField('models.Coop', 'members', null=False, index=True)
    tez_received = fields.BigIntField()
    status = fields.IntEnumField(MemberStatus)

    ophash = fields.CharField(51)
    level = fields.BigIntField()
    timestamp = fields.DatetimeField()


####################
# MARKET Models #
####################


class Token(Model):
    id = fields.BigIntField(pk=True)
    token_id = fields.BigIntField()
    fa2_address = fields.CharField(36)
    creator: ForeignKeyFieldInstance[Holder] = fields.ForeignKeyField('models.Holder', 'tokens', index=True, null=True)
    title = fields.TextField(default='')
    description = fields.TextField(default='')
    artifact_uri = fields.TextField(default='')
    display_uri = fields.TextField(default='')
    thumbnail_uri = fields.TextField(default='')
    metadata = fields.TextField(default='')
    extra = fields.JSONField(default={})
    mime = fields.TextField(default='')
    royalties = fields.SmallIntField(default=0)
    supply = fields.SmallIntField(default=0)

    level = fields.BigIntField(default=0)
    timestamp = fields.DatetimeField(default=datetime.utcnow())


class TagTable(Model):
    id = fields.BigIntField(pk=True)
    tag = fields.CharField(255)


class TokenTag(Model):
    token: ForeignKeyFieldInstance[Token] = fields.ForeignKeyField('models.Token', 'token_tags', null=False, index=True)
    tag: ForeignKeyFieldInstance[TagTable] = fields.ForeignKeyField('models.TagTable', 'tag_tokens', null=False, index=True)

    class Meta:
        table = 'token_tag'


class TokenHolder(Model):
    holder: ForeignKeyFieldInstance[Holder] = fields.ForeignKeyField('models.Holder', 'holders_token', null=False, index=True)
    token: ForeignKeyFieldInstance[Token] = fields.ForeignKeyField('models.Token', 'token_holders', null=False, index=True)
    quantity = fields.BigIntField(default=0)

    class Meta:
        table = 'token_holder'


class Swap(Model):
    id = fields.BigIntField(pk=True)
    creator: ForeignKeyFieldInstance[Holder] = fields.ForeignKeyField('models.Holder', 'swaps', index=True)
    token: ForeignKeyFieldInstance[Token] = fields.ForeignKeyField('models.Token', 'swaps', index=True)
    coop: ForeignKeyFieldInstance[Coop] = fields.ForeignKeyField('models.Coop', 'swaps', index=True)
    price = fields.BigIntField()
    amount = fields.SmallIntField()
    amount_left = fields.SmallIntField()
    status = fields.IntEnumField(SwapStatus)
    royalties = fields.SmallIntField()
    contract_version = fields.SmallIntField()
    is_valid = fields.BooleanField(default=True)

    ophash = fields.CharField(51)
    level = fields.BigIntField()
    timestamp = fields.DatetimeField()


class Trade(Model):
    id = fields.BigIntField(pk=True)
    token: ForeignKeyFieldInstance[Token] = fields.ForeignKeyField('models.Token', 'trades', index=True)
    swap: ForeignKeyFieldInstance[Swap] = fields.ForeignKeyField('models.Swap', 'trades', index=True)
    seller: ForeignKeyFieldInstance[Holder] = fields.ForeignKeyField('models.Holder', 'sales', index=True)
    buyer: ForeignKeyFieldInstance[Holder] = fields.ForeignKeyField('models.Holder', 'purchases', index=True)
    amount = fields.BigIntField()

    ophash = fields.CharField(51)
    level = fields.BigIntField()
    timestamp = fields.DatetimeField()



