from sqlalchemy.orm import Session

from models import engine, DollarPrice

with Session(engine) as session:

    with open('dollar.csv', 'r') as f:
        data = f.read().split('\n')

    for row in data:
        pcs = row.split(',')
        year = int(pcs[0])
        month = int(pcs[1])
        min_p = float(pcs[2])
        max_p = float(pcs[3])

        if month == 0:
            for i in range(1, 13):
                history_model = DollarPrice(
                    h_year=year,
                    h_month=i,
                    upper_band=max_p,
                    lower_band=min_p,
                )
                session.add(history_model)
        else:
            history_model = DollarPrice(
                h_year=year,
                h_month=month,
                upper_band=max_p,
                lower_band=min_p,
            )
            session.add(history_model)

    session.commit()

