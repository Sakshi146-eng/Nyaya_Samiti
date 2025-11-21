import databases
import sqlalchemy
from config import config

metadata=sqlalchemy.MetaData()

users_table=sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("email",sqlalchemy.String,unique=True),
    sqlalchemy.Column("mobno",sqlalchemy.String),
    sqlalchemy.Column("password",sqlalchemy.String),
    sqlalchemy.Column("confirmation",sqlalchemy.Boolean,default=False)
)

client_table=sqlalchemy.Table(
    "client",
    metadata,
    sqlalchemy.Column("user_id",sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("no_fm",sqlalchemy.Integer),
    sqlalchemy.Column("doc_type",sqlalchemy.String),
    sqlalchemy.Column("aadhar_no",sqlalchemy.String),
)

document_table=sqlalchemy.Table(
    "document",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("document",sqlalchemy.String),
    sqlalchemy.Column("user_id",sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("validity",sqlalchemy.Boolean,default=False),
)


profile_table=sqlalchemy.Table(
    "profile",
    metadata,
    sqlalchemy.Column("user_id",sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("proceed",sqlalchemy.Boolean,default=False),
)
engine=sqlalchemy.create_engine(config.DATABASE_URL,connect_args={"check_same_thread":False})

metadata.create_all(engine)
database=databases.Database(config.DATABASE_URL,force_rollback=config.DB_FORCE_ROLLBACK)