from django.core.management.base import BaseCommand, CommandParser
from tools.ingestion.load_companies import CompanyLoader


class Command(BaseCommand):

    help = "Utility to load default companies into the database"

    def add_arguments(self, parser: CommandParser) -> None:
        # Named (optional) arguments
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Log Output',
        )

    def handle(self, *args, **options):
        CompanyLoader.load_default_files()
