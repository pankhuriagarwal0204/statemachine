import base
from archives import models

print models.Event.objects.filter(id = 1372).values()
print models.Event.objects.filter(id = 1373).values()