from sqlalchemy.orm import Session

from models import Symbol, engine, data, convert_letters

with Session(engine) as session:
    all_symbols = []
    for key in data.keys():
        new_symbol = Symbol(
            symbol=convert_letters(data[key][0]),
            company_name=convert_letters(data[key][1]),
            url=key,
            technical_id='',
        )
        session.add(new_symbol)

    session.commit()
