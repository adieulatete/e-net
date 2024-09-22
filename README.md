## E-net

### General information about the project
Online platform of electronics trading network.

#### Functional

Endpoints:  
• Admin panel - /admin;
• Endpoint for receiving tokens - /api/token/; api/token/refresh/
• Endpoint for receiving a QR code with contact details of a network object - api/generate_qr/;
• Endpoint for obtaining information about all network objects, create, delete - api/nodes/; api/products/
• Endpoint for obtaining Statistics about objects whose debt exceeds the average debt of all objects - api/stats/debt;

#### Technologies used

`Python`, `PostgreSQL`, `Git`, `Docker`, `Celery`

#### Libraries used

[`Django`](https://github.com/django/django),
[`Django REST framework`](https://github.com/encode/django-rest-framework),
[`Simple JWT`](https://github.com/jazzband/djangorestframework-simplejwt),
[`Redis`](https://github.com/redis/redis)
[`Celery`](https://github.com/celery/celery)

### Deploy 

```bash
cd ~
git clone https://github.com/adieulatete/e-net.git
cd ~/e-net
docker-compose up --build -d
```
