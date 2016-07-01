from django.core.management.base import BaseCommand, CommandError
from django.db import models
import os
    
class Command(BaseCommand):
     def handle(self, *args, **options):
         print 'hello, django!'