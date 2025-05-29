from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_EVAL_LEVELS = [
    {'short_name': 'NEG', 'full_name': 'Negativa', 'color': '#DC3545'},
    {'short_name': 'MIX', 'full_name': 'Mista', 'color': '#FFC107'},
    {'short_name': 'POS', 'full_name': 'Positiva', 'color': '#198754'},
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
        'PROV_CHOICES': PROV_CHOICES,
        'DEFAULT_MARKER_COLOR': '#6C757D',
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
    msg = "DJEOGRAPHY_CONFIG['DEFAULT_MARKER_COLOR'] should be a HTML color name or a HEX string."
    raise ImproperlyConfigured(msg)
