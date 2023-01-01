from django.db import models

class Tag(models.Model):

    name = models.CharField(max_length=50, verbose_name='Тематика')

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.name

class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    scope = models.ManyToManyField(Tag, through='Scope', verbose_name='Тематика')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

class Scope(models.Model):

    article = models.ForeignKey(Article, default=None, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, default=None, on_delete=models.CASCADE, related_name='scopes', verbose_name='Раздел')
    is_main = models.BooleanField(default=False, verbose_name='Основной') # поставил по умолчанию False вместо None

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статей'
        ordering = ['-is_main', 'tag__name']

    def __str__(self):
        return self.article.title