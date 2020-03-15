# flake8: noqa
import inspect
import sys

from .entities import *
from .information import *
from .ingestion import *
from .models import *
from .portfolios import *
from .tags import *

__all__ = model_members = inspect.getmembers(
    sys.modules[__name__],
    lambda x: not (not inspect.isclass(x) or not x.__module__.startswith('melete.core.models'))
)
#
#
# from .entities import (
#     Alias,
#     Company,
#     Country,
#     Currency,
#     Entity,
#     EntityEntity,
#     Exchange,
#     Index,
#     IndexTicker,
#     Language,
#     Person,
#     PersonEntity,
#     Product,
#     ProductEntity,
#     TagEntity,
#     Ticker,
# )
# from .information import (
#     Article,
#     ArticleEntity,
#     Comment,
#     CommentCollection,
#     CommentCollectionEntity,
#     CommentEntity,
#     Credentials,
#     Fill,
#     Frequency,
#     Function,
#     Report,
#     ReportEntity,
#     Series,
#     SeriesEntity,
#     Source,
#     Thread,
#     ThreadSeries,
#     Tick,
#     TickEntity,
#     TickType,
#     Website,
# )
# from .ingestion import ThreadLoad, ThreadSeriesLoad, TickLoad, WebsiteLoad
# from .models import (
#     Dataframe,
#     DataframeManager,
#     DataframeTicker,
#     DataframeTickType,
#     ErrorType,
#     Metric,
#     MetricMetric,
#     Model,
#     ModelConfig,
#     ModelConfigDataframe,
#     ModelDataframe,
#     Prediction,
#     PredictionSet,
#     Score,
# )
# from .portfolios import (
#     Asset,
#     AssetOrder,
#     AssetType,
#     OrderType,
#     Portfolio,
#     PortfolioPermission,
#     UserPortfolio,
# )
# from .tags import Tag, TagGroup, TagGroupTagGroup, TagTagGroup
#
#
# model_members = [
#     Entity,
#     Person,
#     Company,
#     Ticker,
#     Exchange,
#     Alias,
#     Product,
#     Index,
#     Language,
#     Country,
#     Currency,
#     EntityEntity,
#     TagEntity,
#     PersonEntity,
#     IndexTicker,
#     ProductEntity,
#     Article,
#     Thread,
#     ThreadSeries,
#     Comment,
#     CommentCollection,
#     Report,
#     Series,
#     Source,
#     Website,
#     Credentials,
#     Tick,
#     TickType,
#     Fill,
#     Frequency,
#     Function,
#     SeriesEntity,
#     TickEntity,
#     ArticleEntity,
#     ReportEntity,
#     CommentCollectionEntity,
#     CommentEntity,
#     TickLoad,
#     ThreadLoad,
#     ThreadSeriesLoad,
#     WebsiteLoad,
#     ModelConfig,
#     Model,
#     ModelConfigDataframe,
#     ModelDataframe,
#     Dataframe,
#     DataframeTicker,
#     DataframeTickType,
#     Prediction,
#     PredictionSet,
#     ErrorType,
#     Score,
#     Metric,
#     MetricMetric,
#     Tag,
#     TagGroup,
#     TagGroupTagGroup,
#     TagTagGroup,
#     Portfolio,
#     PortfolioPermission,
#     UserPortfolio,
#     Asset,
#     AssetOrder,
#     AssetType,
#     OrderType
# ]
#
# __all__ = model_members
