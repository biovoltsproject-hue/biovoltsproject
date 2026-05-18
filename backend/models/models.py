"""Modelos de dados da API."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SensorReading(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    channel: str = "ch0"
    voltage_v: Optional[float] = Field(None, description="Tensão em Volts")
    current_a: Optional[float] = Field(None, description="Corrente em Amperes")
    power_w: Optional[float] = Field(None, description="Potência em Watts")
    shunt_mv: Optional[float] = Field(None, description="Tensão no shunt em mV (INA219)")
    raw_adc: Optional[int] = Field(None, description="Valor bruto do ADC")
    sensor_type: str = "unknown"

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class SensorHistory(BaseModel):
    count: int
    readings: List[SensorReading]
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class SensorInfo(BaseModel):
    name: str
    type: str
    connected: bool
    address: Optional[str] = None
    description: str = ""


class SensorStatus(BaseModel):
    online: bool
    sensors: List[SensorInfo]
    uptime_seconds: float
    read_interval_seconds: float
    last_reading: Optional[SensorReading] = None


class AlertConfig(BaseModel):
    voltage_min: Optional[float] = Field(None, description="Tensão mínima (V)")
    voltage_max: Optional[float] = Field(None, description="Tensão máxima (V)")
    current_max: Optional[float] = Field(None, description="Corrente máxima (A)")
    power_max: Optional[float] = Field(None, description="Potência máxima (W)")


class AlertStatus(BaseModel):
    active: bool
    alerts: List[str] = []
    last_checked: Optional[datetime] = None
