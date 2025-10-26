from django.db import models
from django.utils import timezone

NODE_TYPES = [
    ('Extract', 'Extract'),
    ('Transform', 'Transform'),
    ('Train', 'Train'),
    ('Predict', 'Predict'),
]

class Node(models.Model):
    name = models.CharField(max_length=100)
    node_type = models.CharField(max_length=50, choices=NODE_TYPES)
    config = models.JSONField(default=dict, blank=True, null=True) # store parameters like dataset name, features etc.
    inputs = models.ManyToManyField('self', symmetrical=False, related_name='outputs', blank=True)
    status = models.CharField(max_length=20, default='idle')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    node_id = models.PositiveIntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.name} ({self.node_type})"