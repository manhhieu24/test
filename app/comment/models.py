from django.db import models
from app.models import ProductModel
from django.contrib.auth.models import User




class CommentModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='comments')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    content = models.TextField()
    image = models.ImageField(upload_to='comment/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'customer')

    def __str__(self):
        return self.content