from peewee import *

database = SqliteDatabase('./saiot.db')


class BaseModel(Model):
    class Meta:
        database = database


class Connection(BaseModel):
    id = AutoField()
    device_id = IntegerField(column_name='deviceId')
    topic = TextField(null=True)

    class Meta:
        table_name = 'connection'


class Device(BaseModel):
    id = AutoField()
    dcode = TextField(null=True)
    description = TextField(null=True)
    ip = TextField(null=True)
    name = TextField(null=True)
    port = IntegerField(null=True)
    secret = TextField(null=True)
    type = TextField(null=True)

    class Meta:
        table_name = 'device'


class Rule(BaseModel):
    id = AutoField()
    columns = TextField(null=True)
    condition = TextField(null=True)
    description = TextField(null=True)
    device_id = IntegerField(column_name='deviceId')
    name = TextField(null=True)
    path = TextField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    topic = TextField(null=True)

    class Meta:
        table_name = 'rule'
