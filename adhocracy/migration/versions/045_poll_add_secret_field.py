from datetime import datetime
from sqlalchemy import MetaData, Column, ForeignKey, Table
from sqlalchemy import Boolean, Integer, Unicode, DateTime

metadata = MetaData()

poll_table = Table('poll', metadata,
    Column('id', Integer, primary_key=True),
    Column('begin_time', DateTime, default=datetime.utcnow),
    Column('end_time', DateTime, nullable=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('action', Unicode(50), nullable=False),
    Column('subject', Unicode(254), nullable=False),
    Column('scope_id', Integer, ForeignKey('delegateable.id'), nullable=False)
    #Column('secret', Boolean, default=False)
    )

def upgrade(migrate_engine):

    metadata.bind = migrate_engine
    
    secret_column = Column('secret', Boolean, default=False)
    secret_column.create(poll_table)

def downgrade(migrate_engine):
    raise NotImplementedError()
