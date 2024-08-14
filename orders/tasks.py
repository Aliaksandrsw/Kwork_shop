from celery import shared_task
from django.core.mail import send_mail
from .models import Order

import logging

logger = logging.getLogger(__name__)


@shared_task
def order_created(order_id):
    logger.info(f"Starting task for order_id: {order_id}")
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Номер заказа. {order.id}'
        message = f'Уважаемые {order.first_name},\n\n' \
                  f'Вы успешно разместили заказ.' \
                  f'Идентификатор вашего заказа {order.id}.'
        mail_sent = send_mail(subject, message,
                              'admin@kworkshop.com',
                              [order.email])
        logger.info(f"Mail sent: {mail_sent}")
        return mail_sent
    except Exception as e:
        logger.error(f"Error in task: {e}")
        raise




@shared_task
def test_task():
    print("Task is running")
    return 'Done'
