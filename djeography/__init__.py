from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_EVAL_LEVELS = [
    {'db': 'NEG', 'display': 'Negativa', 'marker_color': 'red'},
    {'db': 'MIX', 'display': 'Mista', 'marker_color': 'orange'},
    {'db': 'POS', 'display': 'Positiva', 'marker_color': 'green'},
]

DJEOGRAPHY_CONFIG = getattr(settings, 'DJEOGRAPHY_CONFIG', {})

app_settings = dict({
    'EVAL_LEVELS': DEFAULT_EVAL_LEVELS,
    'DEFAULT_MARKER_COLOR': 'gray',
    'PAGINATION': 6
}, **DJEOGRAPHY_CONFIG)


try:
    app_settings['PAGINATION'] = int(app_settings.get('PAGINATION'))
except ValueError:
    raise ImproperlyConfigured("DJEOGRAPHY_CONFIG['PAGINATION'] should be an integer.")

if not isinstance(app_settings.get('DEFAULT_MARKER_COLOR'), str):
    raise ImproperlyConfigured("DJEOGRAPHY_CONFIG['DEFAULT_MARKER_COLOR'] should be a HTML color name or a HEX string")

try:
    if not isinstance(app_settings.get('EVAL_LEVELS'), list):
        raise ImproperlyConfigured()
    elif not app_settings.get('EVAL_LEVELS'):
        raise ImproperlyConfigured()
    else:
        for eval_level in app_settings.get('EVAL_LEVELS'):
            assert isinstance(eval_level, dict)
            assert 0 < len(eval_level['db']) <= 3
            assert isinstance(eval_level['display'], str)
            assert isinstance(eval_level['marker_color'], str)
    db_strings = [eval_level.get('db') for eval_level in app_settings.get('EVAL_LEVELS')]
    assert len(set(db_strings)) == len(db_strings)

    EVAL_LEVELS = [(level['db'], level['display']) for level in app_settings.get('EVAL_LEVELS')]
    COLOR_MAP = dict({level['db']: level['marker_color'] for level in app_settings.get('EVAL_LEVELS')},
                     **{'default': app_settings.get('DEFAULT_MARKER_COLOR')})


except (AssertionError, ImproperlyConfigured, KeyError):
    raise ImproperlyConfigured("""
    DJEOGRAPHY_CONFIC['EVAL_LEVELS'] should be a list of dictionaries.
    For each evaluation level the following attributes are required:
        - 'db' a non empty string with length <= 3 (should be unique)
        - 'display' a string
        - 'marker_color' a string representing a html color or a HEX code""")
