from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Name')
    content = models.TextField(verbose_name='Text')
    pub_date = models.DateTimeField(auto_now_add=True)
    up_data = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Publish')

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True,
                            verbose_name='Category')

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

class Category(models.Model):
    category = models.CharField(max_length=100, verbose_name='Categories')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category