from django.db import models
from user.models import MyUser
from PIL import Image
from django.urls import reverse_lazy

STATUS = [
    ('O', 'Offer'),
    ('W', 'Wish')
]

CONDITION = [
    ('N', 'New'),
    ('G', 'Good '),
    ('E', 'Excellent'),
    ('S', 'Satisfactory')
]


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, related_name='books')  # x
    status = models.CharField(max_length=1, choices=STATUS)  # x
    condition = models.CharField(choices=CONDITION, max_length=1, blank=True)
    active = models.BooleanField(default=True, blank=True)  # x
    date = models.DateTimeField(auto_now_add=True, null=True)  # x
    cover = models.ImageField(upload_to='book-cover/', default='book-cover/no_cover.png', null=True, blank=True)

    def get_absolute_url(self):
        if self.status == 'O':
            return reverse_lazy('offer-edit', kwargs={'pk': self.pk})
        elif self.status == 'W':
            return reverse_lazy('wish-edit', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title} - {self.author}'
