from django.dispatch import Signal

page_view = Signal(providing_args=['page_path'])
