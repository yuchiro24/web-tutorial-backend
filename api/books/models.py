from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="書籍名")
    author = models.CharField(max_length=255, verbose_name="著者名")
    description = models.TextField(verbose_name="説明", null=True, blank=True) 
    
    class Meta:
        db_table = "book"
        verbose_name = "書籍"

class BookDetail(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="書籍")
    genre = models.CharField(verbose_name="ジャンル", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    class Meta:
        db_table = "book_detail"
        verbose_name = "書籍詳細"