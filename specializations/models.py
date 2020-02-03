from django.db import models
from app.models import BaseModel
# Create your models here.


class Specialization(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f'Specialization({self.id}) {self.name}'
