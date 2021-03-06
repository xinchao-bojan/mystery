from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **kwargs):
        if not (email and first_name and last_name):
            raise ValueError('User must have all necessary information')
        user = self.model(email=self.normalize_email(email), first_name=first_name.capitalize(),
                          last_name=last_name.capitalize(), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **kwargs):
        user = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='Адрес электронной почты', max_length=63, unique=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    attempts = models.PositiveIntegerField(default=3, verbose_name='Количество попыток')
    # promocode = models.CharField(max_length=8, verbose_name='Промокод', blank=True, null=True)
    # promocode = models.ForeignKey('Promocode', on_delete=models.CASCADE, verbose_name='Промокод', null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}. Email: {self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def lose_attempt(self, attempts=1):
        self.attempts = max(self.attempts - 1, 0)
        self.save()

    def enough_attempts(self):
        return self.attempts > 0 or self.is_staff


class Sale(models.Model):
    text = models.CharField(max_length=255, verbose_name='Описание акции')
    max_users = models.PositiveIntegerField(verbose_name='Максимальное количество пользователей')
    slug = models.SlugField(max_length=31, unique=True, verbose_name='Буквенный идентификатор')


class Promocode(models.Model):
    text = models.CharField(max_length=8, verbose_name='Промокод', blank=True, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Скидка')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                                related_name='promocode', null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name='Активный')
    qr = models.ImageField(upload_to='qr', verbose_name='Qr код', blank=True, null=True)


class Question(models.Model):
    STATUS_NODE = 1
    STATUS_FINAL = 2
    STATUS_DEADLOCK = 3
    STATUS_FIRST = 4
    STATUSES = (
        (STATUS_NODE, 'Узел'),
        (STATUS_FINAL, 'Финальный'),
        (STATUS_DEADLOCK, 'Тупик'),
        (STATUS_FIRST, 'Первый'),
    )
    text = models.TextField(verbose_name='Текст вопроса')
    supporting_image = models.ImageField(upload_to='support', verbose_name='Вспомогательное изображение', blank=True,
                                         null=True)
    slug = models.SlugField(max_length=31, unique=True, verbose_name='Буквенный идентификатор')
    status = models.PositiveIntegerField(choices=STATUSES, default=STATUS_NODE, verbose_name='Статус вопроса')


class UserAnswerInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='Вопрос')
    date = models.DateTimeField(default=timezone.now)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='answers')
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    subsequent_question = models.OneToOneField(Question, on_delete=models.CASCADE, verbose_name='Следующий вопрос',
                                               blank=True, null=True, related_name='previous_answer')
    user_list = models.ManyToManyField(CustomUser, through=UserAnswerInfo,
                                       verbose_name='Список ответивших пользователей')

    def save(self, *args, **kwargs):
        self.text = self.text.capitalize()
        super().save(*args, **kwargs)


class Prompt(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    file = models.FileField(upload_to='prompt', verbose_name='Файл с подсказкой', blank=True, null=True)
    visible = models.BooleanField(default=False, verbose_name='Видимость')
    text = models.TextField(verbose_name='Текст подсказки')

    def make_visibility(self):
        self.visible = True
        self.save()
