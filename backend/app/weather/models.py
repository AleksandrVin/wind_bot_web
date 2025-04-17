import uuid
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class WeatherReading(SQLModel, table=True):
    __tablename__ = "weather_reading"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    location_id: uuid.UUID = Field(foreign_key="weather_location.id", index=True)
    data_source: str = Field(max_length=50, index=True)  # e.g., "openweathermap"
    fetched_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    valid_at: datetime = Field(index=True)
    is_forecast: bool = Field(index=True)
    wind_speed: float  # Assuming m/s
    wind_gust: float | None = Field(default=None)  # Assuming m/s
    wind_direction: int  # Degrees (0-360)
    temperature: float | None = Field(default=None)  # Assuming Celsius
    cloud_cover: int | None = Field(default=None)  # Percentage (0-100)
    precipitation_probability: float | None = Field(default=None)  # 0.0 - 1.0
    precipitation_amount: float | None = Field(default=None)  # e.g., mm/hr
    condition_code: str | None = Field(default=None, max_length=50)
    condition_description: str | None = Field(default=None, max_length=255)

    # Use a string for the forward reference because WeatherLocation is defined later
    location: "WeatherLocation" = Relationship(back_populates="readings")


class WeatherLocation(SQLModel, table=True):
    __tablename__ = "weather_location"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    latitude: float = Field(index=True)
    longitude: float = Field(index=True)
    name: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, max_length=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},  # Add onupdate behavior
    )

    readings: list[WeatherReading] = Relationship(
        back_populates="location", cascade_delete=True
    )
