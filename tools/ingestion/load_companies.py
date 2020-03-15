import csv
from os import path

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from melete.core.models import Company, Exchange, Ticker
from melete.status.models import Room

channel_layer = get_channel_layer()
file_dir = path.dirname(path.abspath(__file__))
expected_files = [
    {
        'file': file_dir+'/resources/nasdaq.csv',
        'symbol': 'NASDAQ'
    },
    {
        'file': file_dir+'/resources/nyse.csv',
        'symbol': 'NYSE'
    },
    {
        'file': file_dir+'/resources/amex.csv',
        'symbol': 'NYSE'
    },
]


class CompanyLoader:

    @staticmethod
    def load_default_files():
        room, created = Room.objects.get_or_create(name="Test")
        for item in expected_files:
            exchange = Exchange.objects.get(symbol=item['symbol'])

            with open(item['file'], 'r') as exchange_file:
                exchange_reader = csv.reader(exchange_file, delimiter=',', quotechar='"')
                next(exchange_reader)  # strip headers
                for row in exchange_reader:
                    ipo = None if row[5] == 'n/a' else int(row[5])
                    sector = None if row[6] == 'n/a' else str(row[6])
                    industry = None if row[7] == 'n/a' else str(row[7])
                    comp, comp_created = Company.objects.get_or_create(name=row[1], industry=industry, sector=sector,
                                                                       ipo_year=ipo)
                    ticker, ticker_created = Ticker.objects.get_or_create(name=row[0], symbol=row[0],
                                                                          ticker_company=comp, ticker_exchange=exchange)
                    async_to_sync(room.send)(
                        {
                            "type": "chat.message",
                            "username": "MeleteIngestionBot-Companies",
                            "message": "%s loaded - created: %s" % (ticker.symbol, ticker_created),
                        }
                    )
