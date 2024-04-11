from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=10, choices=[('M', '男'), ('F', '女')], verbose_name='性別')
    borrowing_quantity = models.IntegerField(verbose_name='預約數量', default=0)

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', '可預約'),
        ('unavailable', '不可預約'),
    ]
     
    bname = models.CharField(max_length=50, verbose_name='書名')
    ISBN = models.CharField(max_length=15, verbose_name='ISBN')
    author = models.CharField(max_length=20, verbose_name='作者')
    genre = models.CharField(max_length=10, verbose_name='類別')
    picture = models.ImageField(upload_to='books/',null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='狀態')

    def __str__(self):
        return f"{self.bname} {self.ISBN} {self.author} {self.genre} {self.status}"

class ReservedBook(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='預約者')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='書籍')
    reservation_date = models.DateTimeField(auto_now_add=True, verbose_name='預約日期')

    def __str__(self):
        return f"{self.user.username} - {self.book.bname} - {self.reservation_date}"


