import json
import os

from dotenv import load_dotenv
from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import Response
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from history_extractor.models import Symbol, SymbolHistory, DollarPrice

load_dotenv()

router = APIRouter()
engine = create_engine(os.getenv('database_url'), echo=False)

non_superuser_symbols = [
    'فولاد',
    'خودرو',
    'پتایر',
    'آپ',
    'بورس',
    'وبملت',
    'طلا',
]

non_superuser_symbol_ids = [8, 47, 161, 212, 467, 520, 563]


def check_superuser(request: Request):
    token = request.headers.get('x_token', None)
    return token and token == 'morieti'


@router.get("/api/symbols")
def get_available_symbols(request: Request):
    is_super_user = check_superuser(request)
    with Session(engine) as session:
        if is_super_user:
            stmt = select(Symbol)
        else:
            stmt = select(Symbol).where(Symbol.symbol.in_(non_superuser_symbols))

        symbol_models = session.scalars(stmt)

        result = {}
        for symbol in symbol_models:
            result[symbol.id] = symbol.symbol

    response = Response(
        content=json.dumps(result),
        headers={'content-type': 'application/json'},
        status_code=status.HTTP_200_OK
    )

    return response


@router.get("/api/symbol/{symbol_id}/history")
def get_history(request: Request, symbol_id: int):
    is_super_user = check_superuser(request)
    with Session(engine) as session:
        if not is_super_user:
            if symbol_id not in non_superuser_symbol_ids:
                response = Response(
                    content='You have no access to this data',
                    headers={'content-type': 'application/json'},
                    status_code=status.HTTP_403_FORBIDDEN
                )
                return response

        stmt = select(DollarPrice)
        dollar = session.scalars(stmt).all()
        dollar = {item.get_date(): item.get_avg_price() for item in dollar}

        stmt = select(SymbolHistory).where(SymbolHistory.symbol_id.__eq__(int(symbol_id)))
        history = session.scalars(stmt)
        history = {item.get_date(): item.get_avg_price() for item in history}

        date_keys = list(history.keys())

        ratio = round(dollar[date_keys[0]] / history[date_keys[0]])
        if ratio == 0:
            ratio = 1

        ratio *= 100

        result = {}
        for key in date_keys:
            result[key] = {
                'dollar': dollar[key],
                'stock': history[key],
                'ratio': round(history[key] * ratio / dollar[key], 2),
            }

    return result
