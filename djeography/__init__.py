from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_EVAL_LEVELS = [
    {'db': 'NEG', 'display': 'Negativa', 'marker_color': 'red'},
    {'db': 'MIX', 'display': 'Mista', 'marker_color': 'orange'},
    {'db': 'POS', 'display': 'Positiva', 'marker_color': 'green'},
]

PROV_CHOICES = [
    ('AG', 'Agrigento'),
    ('AL', 'Alessandria'),
    ('AN', 'Ancona'),
    ('AO', 'Aosta'),
    ('AR', 'Arezzo'),
    ('AP', 'Ascoli Piceno'),
    ('AT', 'Asti'),
    ('AV', 'Avellino'),
    ('BA', 'Bari'),
    ('BT', 'Barletta-Andria-Trani'),
    ('BL', 'Belluno'),
    ('BN', 'Benevento'),
    ('BG', 'Bergamo'),
    ('BI', 'Biella'),
    ('BO', 'Bologna'),
    ('BZ', 'Bolzano'),
    ('BS', 'Brescia'),
    ('BR', 'Brindisi'),
    ('CA', 'Cagliari'),
    ('CL', 'Caltanissetta'),
    ('CB', 'Campobasso'),
    ('CE', 'Caserta'),
    ('CT', 'Catania'),
    ('CZ', 'Catanzaro'),
    ('CH', 'Chieti'),
    ('CO', 'Como'),
    ('CS', 'Cosenza'),
    ('CR', 'Cremona'),
    ('KR', 'Crotone'),
    ('CN', 'Cuneo'),
    ('EN', 'Enna'),
    ('FM', 'Fermo'),
    ('FE', 'Ferrara'),
    ('FI', 'Firenze'),
    ('FG', 'Foggia'),
    ('FC', 'Forlì-Cesena'),
    ('FR', 'Frosinone'),
    ('GE', 'Genova'),
    ('GO', 'Gorizia'),
    ('GR', 'Grosseto'),
    ('IM', 'Imperia'),
    ('IS', 'Isernia'),
    ('SP', 'La Spezia'),
    ('AQ', "L'Aquila"),
    ('LT', 'Latina'),
    ('LE', 'Lecce'),
    ('LC', 'Lecco'),
    ('LI', 'Livorno'),
    ('LO', 'Lodi'),
    ('LU', 'Lucca'),
    ('MC', 'Macerata'),
    ('MN', 'Mantova'),
    ('MS', 'Massa-Carrara'),
    ('MT', 'Matera'),
    ('ME', 'Messina'),
    ('MI', 'Milano'),
    ('MO', 'Modena'),
    ('MB', 'Monza Brianza'),
    ('NA', 'Napoli'),
    ('NO', 'Novara'),
    ('NU', 'Nuoro'),
    ('OR', 'Oristano'),
    ('PD', 'Padova'),
    ('PA', 'Palermo'),
    ('PR', 'Parma'),
    ('PV', 'Pavia'),
    ('PG', 'Perugia'),
    ('PU', 'Pesaro e Urbino'),
    ('PE', 'Pescara'),
    ('PC', 'Piacenza'),
    ('PI', 'Pisa'),
    ('PT', 'Pistoia'),
    ('PN', 'Pordenone'),
    ('PZ', 'Potenza'),
    ('PO', 'Prato'),
    ('RG', 'Ragusa'),
    ('RA', 'Ravenna'),
    ('RC', 'Reggio Calabria'),
    ('RE', 'Reggio Emilia'),
    ('RI', 'Rieti'),
    ('RN', 'Rimini'),
    ('RM', 'Roma'),
    ('RO', 'Rovigo'),
    ('SA', 'Salerno'),
    ('SS', 'Sassari'),
    ('SV', 'Savona'),
    ('SI', 'Siena'),
    ('SR', 'Siracusa'),
    ('SO', 'Sondrio'),
    ('SU', 'Sud Sardegna'),
    ('TA', 'Taranto'),
    ('TE', 'Teramo'),
    ('TR', 'Terni'),
    ('TO', 'Torino'),
    ('TP', 'Trapani'),
    ('TN', 'Trento'),
    ('TV', 'Treviso'),
    ('TS', 'Trieste'),
    ('UD', 'Udine'),
    ('VA', 'Varese'),
    ('VE', 'Venezia'),
    ('VB', 'Verbano-Cusio-Ossola'),
    ('VC', 'Vercelli'),
    ('VR', 'Verona'),
    ('VV', 'Vibo Valentia'),
    ('VI', 'Vicenza'),
    ('VT', 'Viterbo'),
]

DJEOGRAPHY_CONFIG = getattr(settings, 'DJEOGRAPHY_CONFIG', {})

app_settings = dict(
    {
        'EVAL_LEVELS': DEFAULT_EVAL_LEVELS,
        'PROV_CHOICES': PROV_CHOICES,
        'DEFAULT_MARKER_COLOR': 'gray',
        'PAGINATION': 6,
    },
    **DJEOGRAPHY_CONFIG,
)


msg = "DJEOGRAPHY_CONFIG['PAGINATION']  should be an integer >= 1."
try:
    app_settings['PAGINATION'] = int(app_settings.get('PAGINATION', 0))  # type: ignore[str]
    if app_settings['PAGINATION'] < 1:
        raise ImproperlyConfigured(msg)
except TypeError as err:
    raise ImproperlyConfigured(msg) from err


if not isinstance(app_settings.get('DEFAULT_MARKER_COLOR'), str):
    msg = "JEOGRAPHY_CONFIG['DEFAULT_MARKER_COLOR'] should be a HTML color name or a HEX string."
    raise ImproperlyConfigured(msg)

imp_cong_msg = """
    DJEOGRAPHY_CONFIG['EVAL_LEVELS'] should be a list of dictionaries.
    For each evaluation level the following attributes are required:
        - 'db' a non empty string with length <= 3 (should be unique)
        - 'display' a string (should be unique)
        - 'marker_color' a string representing a html color or a HEX code"""

if not isinstance(app_settings.get('EVAL_LEVELS'), list) or not app_settings.get(
    'EVAL_LEVELS',
):
    raise ImproperlyConfigured(imp_cong_msg)
else:
    try:
        for eval_level in app_settings.get('EVAL_LEVELS'):  # type: ignore[none]
            if not isinstance(eval_level, dict):
                raise TypeError
            elif (
                len(eval_level.get('db', '')) > 3 or len(eval_level.get('db', '')) == 0
            ):
                raise ValueError
            elif not isinstance(eval_level.get('display'), str) or not isinstance(
                eval_level.get('marker_color'),
                str,
            ):
                raise TypeError

        db_strings = [
            eval_level.get('db')
            for eval_level in app_settings.get('EVAL_LEVELS')  # type: ignore[none]
        ]
        display_strings = [
            eval_level.get('display')
            for eval_level in app_settings.get('EVAL_LEVELS')  # type: ignore[none]
        ]
        if len(set(db_strings)) != len(db_strings):
            msg = "In DJEOGRAPHY_CONFIG['EVAL_LEVELS'] db values should be unique."
            raise ValueError(msg)
        if len(set(display_strings)) != len(display_strings):
            msg = "In DJEOGRAPHY_CONFIG['EVAL_LEVELS] display values should be unique."
            raise ValueError(msg)

        EVAL_LEVELS = [
            (level['db'], level['display'])
            for level in app_settings.get('EVAL_LEVELS')  # type: ignore[none]
        ]
        COLOR_MAP = dict(
            {
                level['db']: level['marker_color']
                for level in app_settings.get('EVAL_LEVELS')  # type: ignore[none]
            },
            default=app_settings.get('DEFAULT_MARKER_COLOR'),
        )

    except (ValueError, KeyError, TypeError) as err:
        raise ImproperlyConfigured(imp_cong_msg) from err
