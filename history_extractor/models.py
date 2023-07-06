import json
import os

from dotenv import load_dotenv
from sqlalchemy import String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Symbol(Base):
    __tablename__ = "symbols"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32))
    company_name: Mapped[str] = mapped_column(String(128))
    url: Mapped[str] = mapped_column(String(128))
    technical_id: Mapped[str] = mapped_column(String(32))

    def __repr__(self) -> str:
        return f"Symbol(id={self.id!r}, symbol={self.symbol!r}, url={self.url!r})"


class SymbolHistory(Base):
    __tablename__ = "symbol_histories"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol_id: Mapped[int] = mapped_column(ForeignKey("symbols.id"))
    h_year: Mapped[int] = mapped_column()
    h_month: Mapped[int] = mapped_column()
    upper_band: Mapped[float] = mapped_column()
    lower_band: Mapped[float] = mapped_column()

    symbol: Mapped["Symbol"] = relationship()

    def __repr__(self) -> str:
        return f"SymbolHistory(id={self.id!r}, symbol={self.symbol.symbol!r}, date={self.h_year!r}/{self.h_month!r}," \
               f" bands=({self.lower_band!r}, {self.upper_band!r}))"

    def get_date(self):
        return f"{self.h_year!r}-{self.h_month!r}"

    def get_avg_price(self):
        return round((self.upper_band + self.lower_band) / 2)


class DollarPrice(Base):
    __tablename__ = "dollar_prices"
    id: Mapped[int] = mapped_column(primary_key=True)
    h_year: Mapped[int] = mapped_column()
    h_month: Mapped[int] = mapped_column()
    lower_band: Mapped[float] = mapped_column()
    upper_band: Mapped[float] = mapped_column()

    def __repr__(self) -> str:
        return f"DollarPrice(id={self.id!r}, date={self.h_year!r}/{self.h_month!r}," \
               f" bands=({self.lower_band!r}, {self.upper_band!r}))"

    def get_date(self):
        return f"{self.h_year!r}-{self.h_month!r}"

    def get_avg_price(self):
        return round((self.upper_band + self.lower_band) / 2) * 10


def convert_letters(text: str):
    replaceable_letters = {
        'ك': 'ک',
        'دِ': 'د',
        'بِ': 'ب',
        'زِ': 'ز',
        'ذِ': 'ذ',
        'شِ': 'ش',
        'سِ': 'س',
        'ى': 'ی',
        'ي': 'ی',
        '١': '۱',
        '٢': '۲',
        '٣': '۳',
        '٤': '۴',
        '٥': '۵',
        '٦': '۶',
        '٧': '۷',
        '٨': '۸',
        '٩': '۹',
        '٠': '۰'
    }

    for ar_letter in replaceable_letters:
        text = text.replace(ar_letter, replaceable_letters[ar_letter])

    return text


load_dotenv()

engine = create_engine(os.getenv('database_url'), echo=False)

with open('history_extractor/all_symbols.json', 'r') as f:
    data = f.read()
    data = json.loads(data)
