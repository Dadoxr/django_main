from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField(verbose_name='тело')
    title_image = models.ImageField(upload_to='blog/', verbose_name='обложка')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    count = models.IntegerField(default=0, verbose_name='просмотры')


    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['create_at']