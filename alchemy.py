from sqlalchemy import Table,MetaData,create_engine,Column,String,Integer,Boolean
from sqlalchemy.orm import scoped_session,sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey
import pymysql


Base = declarative_base()
DB_CONNECT_STR = "mysql+pymysql://root:@localhost:3306/torrant?charset=utf8"
engine = create_engine(DB_CONNECT_STR,echo=True,encoding="utf8",convert_unicode=True)  #已更改为在pipelines中创建
db_session = scoped_session(sessionmaker(autocommit=False,  # 已更改为在pipelines中创建
                                         autoflush=False,
                                         bind=engine))
                                         
class Torrant(Base):
    __tablename__ = 'wanacg'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(255),nullable=True)
    link = Column(String(255),nullable=False)
    download = Column(String(255),nullable=False)
    image = Column(String(255),nullable=True)
    bit = Column(String(255),nullable=True)
    num = Column(String(255),nullable=True)
    gallary = Column(String(255),nullable=True)

def main():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()
