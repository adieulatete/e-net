import random
import io
import qrcode
from django.core.mail import EmailMessage
from celery import shared_task
from .models import NetworkNode


@shared_task
def increase_debt_to_supplier():
    """
    Increases debt_to_supplier for all NetworkNode instances by a random
    amount between 5 and 500.
    """
    nodes = NetworkNode.objects.all()
    for node in nodes:
        increase_amount = random.uniform(5, 500)
        node.debt_to_supplier += increase_amount
        node.save()


@shared_task
def decrease_debt_to_supplier():
    """
    Decreases debt_to_supplier for all NetworkNode instances by a random
    amount between 100 and 10,000. Ensures debt does not fall below 0.
    """
    nodes = NetworkNode.objects.all()
    for node in nodes:
        decrease_amount = random.uniform(100, 10000)
        node.debt_to_supplier = max(0, node.debt_to_supplier - decrease_amount)
        node.save()


@shared_task
def clear_data_async(node_ids):
    """
    Resets debt_to_supplier to 0 for NetworkNode instances whose IDs are
    in node_ids.
    """
    nodes = NetworkNode.objects.filter(id__in=node_ids)
    nodes.update(debt_to_supplier=0)


@shared_task
def send_qr_code_via_email(contact_data, email):
    """Generate a QR code and send it via email."""
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(contact_data)
    qr.make(fit=True)

    # Create QR code image
    img = qr.make_image(fill='black', back_color='white')

    # Save QR code to a bytes buffer
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)

    # Create email with attached QR code
    email_message = EmailMessage(
        subject="Your Network Node QR Code",
        body="Please find attached the QR code with contact information.",
        to=[email]
    )
    email_message.attach('networknode_qr.png', buf.getvalue(), 'image/png')

    # Send email
    email_message.send()
