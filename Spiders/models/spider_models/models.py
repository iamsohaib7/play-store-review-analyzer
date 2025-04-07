# this includes the models for storing the scrapped data in database,
# it is considered as raw storage for scraped data.
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import (Date, DateTime, Float, ForeignKey, Integer, String,
                        Text, Uuid)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
    reviews: Mapped[List["AppReviewsModel"]] = relationship(
        "AppReviewsModel", back_populates="app_info", cascade="all, delete-orphan"
    )  # App Info has one-to-many relationship with App reviews it shows the relationship
    details: Mapped["AppDetailsModel"] = relationship(
        "AppDetailsModel",
        back_populates="app_info",
        uselist=False,
        cascade="all, delete-orphan",
    )  # Added relationship with AppDetailsModel
    rating_histogram: Mapped[List["AppRatingsHistogramModel"]] = relationship(
        "AppRatingsHistogramModel",
        back_populates="app_info",
        cascade="all, delete-orphan",
    )  # Added relationship with AppRatingsHistogramModel
    developer_details: Mapped[List["AppDeveloperDetailsModel"]] = relationship(
        "AppDeveloperDetailsModel",
        back_populates="app_info",
        cascade="all, delete-orphan",
    )  # Added relationship with AppDeveloperDetailsModel

    def __repr__(self):
        return f"{self.app_id=}, {self.app_name=}, {self.url=}, {self.added_at=}"


class AppReviewsModel(BaseModel):
    __tablename__ = "app_reviews"
    app_id: Mapped[str] = mapped_column(ForeignKey("app_info.app_id"))
    review_id: Mapped[Uuid] = mapped_column(
        Uuid, nullable=False, primary_key=True, default=uuid.uuid4
    )
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    app_info: Mapped["AppInfoModel"] = relationship(
        "AppInfoModel", back_populates="reviews"
    )
    review_meta: Mapped["ReviewMetaDetailsModel"] = relationship(
        "ReviewMetaDetailsModel",
        back_populates="review",
        uselist=False,
        cascade="all, delete-orphan",
    )


class ReviewMetaDetailsModel(BaseModel):
    __tablename__ = "review_meta_details"
    _id: Mapped[Integer] = mapped_column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    review_id: Mapped[Uuid] = mapped_column(Uuid, ForeignKey("app_reviews.review_id"))
    ratings: Mapped[str] = mapped_column(Integer, nullable=False)
    review_created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    thumbs_up_count: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)
    review_created_version: Mapped[str] = mapped_column(String(100), nullable=True)
    review_reply: Mapped[str] = mapped_column(Text, nullable=True)
    reply_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    current_app_version: Mapped[str] = mapped_column(String(100), nullable=True)
    review: Mapped["AppReviewsModel"] = relationship(
        "AppReviewsModel", back_populates="review_meta"
    )


class AppDetailsModel(BaseModel):
    __tablename__ = "app_details"
    _id: Mapped[Integer] = mapped_column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    app_id: Mapped[str] = mapped_column(ForeignKey("app_info.app_id"))
    summary: Mapped[str] = mapped_column(String(255), nullable=True)
    total_app_installs: Mapped[str] = mapped_column(
        String(100), nullable=False, default=0
    )
    avg_rating: Mapped[Float] = mapped_column(Float, nullable=False, default=0)
    ratings_count: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)
    reviews_count: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)
    last_updated: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    released_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    app_info: Mapped["AppInfoModel"] = relationship(
        "AppInfoModel", back_populates="details"
    )  # Added relationship with AppInfoModel


class AppRatingsHistogramModel(BaseModel):
    __tablename__ = "app_rating_histogram"
    app_id: Mapped[str] = mapped_column(ForeignKey("app_info.app_id"))
    _id: Mapped[Integer] = mapped_column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    rating_star: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)
    ratings_count: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)
    app_info: Mapped["AppInfoModel"] = relationship(
        "AppInfoModel", back_populates="rating_histogram"
    )  # Added relationship with AppInfoModel


class AppDeveloperDetailsModel(BaseModel):
    __tablename__ = "app_developer_details"
    _id: Mapped[Integer] = mapped_column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    app_id: Mapped[str] = mapped_column(ForeignKey("app_info.app_id"))
    developer_id: Mapped[str] = mapped_column(String, nullable=True)
    developer: Mapped[str] = mapped_column(String(255), nullable=True)
    developer_email: Mapped[str] = mapped_column(String(255), nullable=True)
    developer_website: Mapped[str] = mapped_column(String(255), nullable=True)
    developer_address: Mapped[str] = mapped_column(String(255), nullable=True)
    app_info: Mapped["AppInfoModel"] = relationship(
        "AppInfoModel", back_populates="developer_details"
    )  # Added relationship with AppInfoModel
