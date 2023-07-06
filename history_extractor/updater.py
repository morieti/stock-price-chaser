from typing import Union

import requests
from jdatetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import convert_letters, engine, Symbol, SymbolHistory


def validate_symbol(text):
    return not (text.find('اخزا') > 0 or text.find('ض') == 0 or text[-1].isdigit() or text[-1] == 'ح')


url = 'http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0'
data = requests.get(url).text

with Session(engine) as session:
    for row in data.split(';')[1:]:
        pcs = row.split(',')
        if len(pcs) < 20:
            continue

        symbol = convert_letters(pcs[2])
        if not validate_symbol(symbol):
            continue

        stmt = select(Symbol).where(Symbol.symbol.__eq__(symbol))
        symbol_model: Union[Symbol, None] = session.scalar(stmt)
        if not symbol_model:
            continue

        technical_id = pcs[1]
        symbol_model.technical_id = technical_id

        lowest = float(pcs[11])
        highest = float(pcs[12])

        now_dt = datetime.now()
        year = int(now_dt.year)
        month = int(now_dt.month)

        stmt = select(SymbolHistory).where(
            SymbolHistory.symbol_id.__eq__(symbol_model.id),
            SymbolHistory.h_year.__eq__(year),
            SymbolHistory.h_month.__eq__(month),
        )
        history_model: Union[SymbolHistory, None] = session.scalar(stmt)
        if not history_model:
            new_history_model = SymbolHistory(
                symbol_id=symbol_model.id,
                h_year=year,
                h_month=month,
                upper_band=highest,
                lower_band=lowest,
            )
            session.add(new_history_model)
        else:
            if highest > history_model.upper_band:
                history_model.upper_band = highest

            if lowest < history_model.lower_band:
                history_model.lower_band = lowest

            session.commit()
