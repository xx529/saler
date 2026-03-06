from src.store.base import BaseSqlModel, SnowFlakeID


class ConvModel(SnowFlakeID, BaseSqlModel, table=True):
    __tablename__ = 'conv'
    __table_args__ = {'comment': '对话记录'}


class MessageModel(SnowFlakeID, BaseSqlModel, table=True):
    __tablename__ = 'message'
    __table_args__ = {'comment': '消息记录'}
