from config import celery_app
from melete.core.models.entities import Ticker


@celery_app.task()
def get_tickers_count():
    """A pointless Celery task to demonstrate usage."""
    return Ticker.objects.count()
