from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from djgeojson.fields import PointField

from djeography import app_settings


class EntityManager(models.Manager):
    """
    Un manager per le segnalazioni.

    Evita ulteriori richieste al database per categoria, indirizzo e contatti
    """

    def get_queryset(self) -> models.QuerySet:
        return (
            super()
            .get_queryset()
            .select_related('category', 'evaluation')
            .prefetch_related('address_set', 'contact_set')
        )


class PublishedEntityManager(EntityManager):
    """
    Un manager per le segnalazioni che restituisce solo le segnalazioni pubblicate.

    (eredita da EntityManager)
    """

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(published=True)


class Category(models.Model):
    """Modella le categorie per le segnalazioni."""

    name = models.CharField('nome', max_length=60)
    icon = models.CharField(
        'icona',
        max_length=20,
        blank=True,
        null=False,
        help_text=(
            "inserisci il nome di un'icona da "
            '<a href="https://fontawesome.com/search?ic=free" target="_blank">'
            'https://fontawesome.com/search?ic=free</a>'
        ),
    )

    # Lo slug server per filtrare le segnalazioni sulla base delle categorie
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorie'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """Crea slug prima di salvare."""
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    @property
    def url(self):
        return reverse('djeography:data', kwargs={'slug': self.slug})


class EvaluationLevel(models.Model):
    """
    Models the evaluation levels.

    Evaluation levels are defined in the database in order to
    allow for user customization.
    """

    short_name = models.CharField(verbose_name='id', max_length=3, primary_key=True)
    full_name = models.CharField(
        verbose_name='nome',
        max_length=32,
        null=False,
        unique=True,
    )
    color = models.CharField(
        verbose_name='colore',
        max_length=32,
        null=False,
        unique=True,
    )

    class Meta:
        verbose_name = 'Livello di valutazione'
        verbose_name_plural = 'Livelli di valutazione'

    def __str__(self) -> str:
        return self.full_name


class Entity(models.Model):
    """
    Modella le segnalazioni.

    Le segnalazioni possono essere salvate come bozze senza essere pubblicate.
    Ogni segnalazione appartiene a una sola categoria e deve avere:
    - titolo
    - descrizione (o note aggiuntive) *
    - valutazione (positiva, neutra, negativa)*
    - contatti (0, N)
    - indirizzi (0, N)
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        verbose_name='categoria',
        null=False,
    )
    title = models.CharField('titolo', max_length=60)
    description = models.TextField('info', null=False, blank=True)
    evaluation = models.ForeignKey(
        EvaluationLevel,
        on_delete=models.RESTRICT,
        verbose_name='valutazione',
        null=True,
        blank=True,
    )
    published = models.BooleanField('pubblicata', default=False)

    # Model default manager
    objects = EntityManager()
    # Only published objects
    published_objects = PublishedEntityManager()

    class Meta:
        verbose_name = 'segnalazione'
        verbose_name_plural = 'segnalazioni'

    def __str__(self) -> str:
        return f'{self.title} ({self.category})'

    def get_absolute_url(self):
        return reverse('djeography:detail', kwargs={'pk': self.pk})

    def publish(self):
        self.published = True
        self.save()

    def unpublish(self):
        self.published = False
        self.save()


class Address(models.Model):
    """
    Modella gli indirizzi.

    Ciascun indirizzo può essere associato a più di una segnalazione se necessario
    e ha i seguenti campi:
    - via
    - numero civico
    - città
    - provincia
    - coordinate
    """

    road = models.CharField('via/piazza', max_length=120, null=False, blank=True)
    number = models.CharField('numero civico', max_length=20, null=False, blank=True)
    city = models.CharField('città', max_length=60)
    province = models.CharField(
        'provincia',
        max_length=2,
        choices=app_settings['PROV_CHOICES'],
    )
    coords = PointField()
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'indirizzo'
        verbose_name_plural = 'indirizzi'

    def __str__(self) -> str:
        return f'{self.road}, {self.number} {self.city} ({self.province})'

    @property
    def popupUrl(self):
        return reverse('djeography:popup', kwargs={'pk': self.pk})


class Contact(models.Model):
    """
    Modella i contatti.

    Ogni contatto può essere associato a una o più segnalazioni e deve avere:
    - tipo (email, numero di telefono, sito)
    - contatto
    """

    TYPE_CHOICES = [('P', 'numero di telefono'), ('E', 'e-mail'), ('S', 'sito')]
    typology = models.CharField('tipo', max_length=2, choices=TYPE_CHOICES)
    contact = models.CharField('contatto', max_length=60)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'contatto'
        verbose_name_plural = 'contatti'

    def __str__(self) -> str:
        return str(self.contact)


class Report(models.Model):
    """
    Modella le testimonianze (ogni segnalazione può avere 0, N testimonanze).

    Ogni testimonianza ha un titolo, un corpo e la data.
    """

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    title = models.CharField('titolo', max_length=100, null=False)
    body = models.TextField('testo', null=False, blank=True)
    date_added = models.DateField('data', default=timezone.now)

    class Meta:
        verbose_name = 'testimonianza'
        verbose_name_plural = 'testimonianze'
        get_latest_by = 'date_added'

    def __str__(self):
        return self.title
