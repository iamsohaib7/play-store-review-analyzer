# this includes the models for storing the scrapped data in database,
# it is considered as raw storage for scraped data.

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class AppInfoModel(BaseModel):
    __tablename__ = "app_info"
    app_id: Mapped[str] = mapped_column(String(150), primary_key=True)
    app_name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    app_description: Mapped[str] = mapped_column(Text, nullable=True)
    added_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    def __repr__(self):
        return f"{self.app_id=}, {self.app_name=}, {self.url=}, {self.added_at=}"
