from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import boto3
from db import crud
import json
import sqlalchemy.orm as orm
from fastapi import Depends
from db.get import get_db


def send_notification(ticket, event, url):
    try:
        sender_email = SENDER_EMAIL

        body = f"""
        <p>Se ha realizado una compra en ArquiTicket</p><br/>
        <p>Detalles de la compra:</p><br/>
        <p>Evento: {event.name}</p>
        <p>Cantidad de entradas: {ticket.quantity}</p>
        <p>Costo total: ${event.price * ticket.quantity}</p><br/>
        <p>Puede descargar sus tickets en: <a href={url}>Descargar</a></p><br/>
        <p>Gracias por usar ArquiTicket</p>
        """

        message = MIMEMultipart('alternative')
        message.attach(MIMEText(body, "html"))
        message["Subject"] = "Compra realizada en ArquiTicket"
        message["From"] = sender_email
        message["To"] = ticket.user_id

        connection = smtplib.SMTP('smtp.gmail.com', 587)

        connection.starttls()
        # contraseña puede no funcionar en otros dispositivos talvez
        connection.login(user=sender_email, password=PASSWORD)
        print("Login success")

        connection.sendmail(from_addr=sender_email, to_addrs=ticket.user_id,
                            msg=message.as_string())

        connection.close()
        print("Connection closed")
    except Exception:
        return False
    return True


def mailer(ticket_id: str, event_id: str, db: orm.Session = Depends(get_db)):
    # Mailing
    ticket = crud.get_ticket(db, ticket_id)
    event = crud.get_event(db, event_id)
    # lambda
    data = {
        "name": event.name,
        "user": ticket.user_id,
        "date": event.date,
        "id": event.event_id,
        "request_id": ticket.request_id,
    }
    session = boto3.Session(
        region_name=REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    lambda_client = session.client('lambda')

    response = lambda_client.invoke(
        FunctionName='generar_ticket',
        Payload=json.dumps(data)
    )

    result = response['Payload'].read().decode('utf-8')
    result = json.loads(result)["body"]

    crud.update_ticket_link(db, request_id=ticket_id, link=result["url"])
    # URL para descargar las entradas de AWS Lambda
    url = result["url"].replace(" ", "")
    return send_notification(ticket=ticket, event=event, url=url)
