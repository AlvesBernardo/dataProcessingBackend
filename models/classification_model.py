from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, ForeignKey , Date , Interval
from config.connection_configuration import engine
from datetime import timedelta
meta = MetaData(bind=engine)
view_table = Table(
    "classification",
    meta,
    Column("idClassification", Integer, primary_key=True),
    Column("dtDescription", String)
)