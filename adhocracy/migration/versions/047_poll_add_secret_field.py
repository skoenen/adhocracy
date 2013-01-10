from datetime import datetime
from sqlalchemy import MetaData, Column, ForeignKey, Table, String
from sqlalchemy import Boolean, Integer, Unicode, DateTime, UnicodeText

metadata = MetaData()

poll_table = Table('poll', metadata,
    Column('id', Integer, primary_key=True),
    Column('begin_time', DateTime, default=datetime.utcnow),
    Column('end_time', DateTime, nullable=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('action', Unicode(50), nullable=False),
    Column('subject', Unicode(254), nullable=False),
    Column('scope_id', Integer, ForeignKey('delegateable.id'), nullable=False)
    #Column('secret', Boolean, default=False),
    #Column('secret_requestor', Integer, ForeignKey('user.id')),
    #Column('secret_request_date', DateTime)
    )

user_table = Table('user', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_name', Unicode(255), nullable=False, unique=True, index=True),
    Column('display_name', Unicode(255), nullable=True, index=True),
    Column('bio', UnicodeText(), nullable=True),
    Column('email', Unicode(255), nullable=True, unique=False),
    Column('email_priority', Integer, default=3),
    Column('activation_code', Unicode(255), nullable=True, unique=False),
    Column('reset_code', Unicode(255), nullable=True, unique=False),
    Column('password', Unicode(80), nullable=False),
    Column('locale', Unicode(7), nullable=True),
    Column('create_time', DateTime, default=datetime.utcnow),
    Column('access_time', DateTime, default=datetime.utcnow,
           onupdate=datetime.utcnow),
    Column('delete_time', DateTime),
    Column('banned', Boolean, default=False),
    Column('no_help', Boolean, default=False, nullable=True),
    Column('page_size', Integer, default=10, nullable=True),
    Column('proposal_sort_order', Unicode(50), default=None, nullable=True)
    )

delegateable_table = Table('delegateable', metadata,
    Column('id', Integer, primary_key=True),
    Column('label', Unicode(255), nullable=False),
    Column('type', String(50)),
    Column('create_time', DateTime, default=datetime.utcnow),
    Column('access_time', DateTime, default=datetime.utcnow,
           onupdate=datetime.utcnow),
    Column('delete_time', DateTime, nullable=True),
    Column('milestone_id', Integer, ForeignKey('milestone.id'), nullable=True),
    Column('creator_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('instance_id', Integer, ForeignKey('instance.id'), nullable=False)
    )

def upgrade(migrate_engine):

    metadata.bind = migrate_engine

    secret_column = Column('secret', Boolean, default=False)
    secret_requestor_column = Column('secret_requestor', Integer, ForeignKey('user.id'))
    secret_request_date_column = Column('secret_request_date', DateTime)

    secret_column.create(poll_table)
    secret_requestor_column.create(poll_table)
    secret_request_date_column.create(poll_table)

def downgrade(migrate_engine):
    raise NotImplementedError()
