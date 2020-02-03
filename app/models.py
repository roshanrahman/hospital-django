from django.db import models
from safedelete.models import SafeDeleteModel


class BaseModel(SafeDeleteModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
