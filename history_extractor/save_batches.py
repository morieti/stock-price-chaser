from sqlalchemy.orm import Session

from models import engine, data, SymbolHistory

with Session(engine) as session:
    s_id = 1
    for key in data:
        history_file = f'../histories/history_{data[key][0]}.csv'
        with open(history_file, 'r') as f:
            history = f.read().split('\n')[1:-1]
            history.reverse()

        symbol_history = {}
        for item in history:
            pcs = item.split(', ')
            date = pcs[0].split('/')

            year = int(date[0])
            if year not in symbol_history.keys():
                symbol_history[year] = {}

            month = int(date[1])
            if month not in symbol_history[year].keys():
                symbol_history[year][month] = {
                    'min': 10000000000000.,
                    'max': 0.
                }

            min_p = pcs[1]
            symbol_history[year][month]['min'] = min(float(min_p), symbol_history[year][month]['min'])

            max_p = pcs[2]
            symbol_history[year][month]['max'] = max(float(max_p), symbol_history[year][month]['max'])

        for year, monthes in symbol_history.items():
            for month, prices in monthes.items():
                history_model = SymbolHistory(
                    symbol_id=s_id,
                    h_year=year,
                    h_month=month,
                    upper_band=prices['max'],
                    lower_band=prices['min'],
                )
                session.add(history_model)

        session.commit()
        print(f"Symbol ID: {s_id} finished")
        s_id += 1

