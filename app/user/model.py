from datetime import datetime

from app.models import Base
from app.user.schemas import TimeData, UserShow
from sqlalchemy import TEXT, VARCHAR, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    password_hash: Mapped[str] = mapped_column(TEXT)
    time: Mapped[int] = mapped_column(Integer, default=0)
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    )

    def to_read_model(self, time_data: list[TimeData] | None = None) -> UserShow:
        return UserShow(
            id=self.id, username=self.username, time=self.time, time_data=time_data
        )


class UserInfoModel(Base):
    __tablename__ = "user_info"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    session_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    )
    session_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    )

    def to_read_model(self) -> TimeData:
        delta = int((self.session_end - self.session_start).total_seconds() // 60)
        return TimeData(
            session_start=self.session_start, session_end=self.session_end, delta=delta
        )
