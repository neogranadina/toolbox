from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from toolboximport.resources import EntierroResource 
from tablib import Dataset

class Command(BaseCommand):
    help = "Importa modelos completos en la base de datos"
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--filename', type=str, help='Path to the file to be imported.')
        parser.add_argument('--mappath', type=str, help='Path to the JSON file containing the mapping configuration.')
        parser.add_argument('--filetype', type=str, choices=['xlsx', 'csv'], default='xlsx', help='Type of the file to be imported.')
        parser.add_argument('--sheetnumber', type=int, default=0, help='Sheet number to import from, for Excel files.')
        parser.add_argument('--tablename', type=str, help='Bautismos, Matrimonios, Entierros')
        
    def handle(self, *args: Any, **options: Any) -> str | None:
        filename = options['filename']
        mappath = options['mappath']
        filetype = options['filetype']
        sheetnumber = options['sheetnumber']
        tablename = options['tablename']
        
        