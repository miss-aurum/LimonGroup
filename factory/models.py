from django.db import models
from client.models import Client
from employees.models import Employee


class Price(models.Model):
    objects = None
    created_at = models.DateTimeField("Запись создана", auto_now_add=True)
    updated_at = models.DateTimeField("Запись обновлена", auto_now=True)
    start_date = models.DateTimeField("Цена действительна с")
    end_date = models.DateTimeField("Цена действительна до")
    is_actual = models.BooleanField("Актуально?", default=True)
    value = models.DecimalField("Стоимость", max_digits=7, decimal_places=2)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Стоимость пошива"
        # verbose_name = "Цены"
        ordering = ['updated_at']


# Create your models here.


class SewingModel(models.Model):
    client = models.ManyToManyField(Client,  verbose_name='Клиент')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    material = models.CharField(
        max_length=50,
        verbose_name='Материал',
        blank=True,
        null=True)
    type = models.CharField(max_length=50, verbose_name='Тип модели')
    price_for_one = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена за штуку')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модель'


class Order(models.Model):
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        on_delete=models.CASCADE)
    name_order = models.ForeignKey(
        SewingModel,
        verbose_name='Модель',
        on_delete=models.CASCADE)
    data_poluchenia = models.DateField(
        auto_now_add=True, verbose_name='Дата Получения')
    quantity_zayav = models.IntegerField(
        default=0, verbose_name='Количество Заявленное')
    quantity_fact = models.IntegerField(
        default=0, verbose_name='Количество Фактически выполненного')
    data_zakup = models.DateField(
        auto_now=True,
        verbose_name='Дата закупа',
        blank=True,
        null=True)
    raskroi_tkani = models.DateField(
        verbose_name='Дата когда раскроили',
        blank=True,
        null=True)
    pod_flizelin = models.DateField(
        verbose_name='Дата подклейки флизелина',
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f'Имя клиента {self.client}. Имя продутка {self.name_order}.'


class DailyWork(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Cотрудник")
    product = models.ForeignKey(
        SewingModel,
        on_delete=models.CASCADE,
        verbose_name="Модель")  # модель
    payment_per_day = models.IntegerField(
        default=0, verbose_name="Зарплата за день")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    prepayment = models.IntegerField(default=0, verbose_name="Аванс")

    def __str__(self):
        return self.date

    class Meta:
        verbose_name = "Ежедневник"
        verbose_name_plural = "Ежедневники"


class NewOrder(models.Model):
    product = models.ForeignKey(
        SewingModel,
        on_delete=models.CASCADE,
        verbose_name="Модель")
    price = models.PositiveIntegerField(verbose_name="Стоимость")
    color = models.CharField(max_length=25, verbose_name="Цвет")
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Изображение")
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент")
    received_date = models.DateField(verbose_name="Дата получения")
    delivery_date = models.DateField(verbose_name="Дата отправки")

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = "Образец"
        verbose_name_plural = "Образцы"


class RawStuff(models.Model):
    name = models.CharField(
        max_length=50,
        null=True,
        verbose_name='Наименование')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт из склада'
        verbose_name_plural = 'Продукт из склада'


class Storage(models.Model):
    code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Код')
    product = models.ForeignKey(
        RawStuff,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Сырье")
    color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Цвет')
    quantity = models.IntegerField(
        default=0, null=True, verbose_name='Количество')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        verbose_name='Сумма')
    data_purchase = models.DateField(verbose_name='Дата закупки')
    is_ready = models.BooleanField(default=True, verbose_name='Готово')
    remainder = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Остаток')
    defect = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name='Брак')
    created_at = models.DateTimeField(verbose_name='')
    where_was_purchase = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Поставщик')

    def __str__(self):
        return self.product

    class Meta:
        # verbose_name = "Образец"
        # verbose_name_plural = "Образцы"
        #
        verbose_name = 'Склад-Сырье'
        verbose_name_plural = 'Склад-Сырье'


class FabricCutting(models.Model):
    material = models.ForeignKey(Storage, null=True, on_delete=models.SET_NULL)
    model_id = models.ForeignKey(
        SewingModel,
        null=True,
        on_delete=models.SET_NULL)
    quantity_model_total = models.IntegerField(default=0, null=True)
    data_start_day = models.DateField(verbose_name='Дата начала')
    data_start_end = models.DateField(verbose_name='Дата окончания')

    def __str__(self):
        return self.material

    class Meta:
        verbose_name = 'Раскрой ткани'
        verbose_name_plural = 'Раскрой ткани'
