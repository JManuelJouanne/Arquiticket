from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def send_notification(ticket, event, url):
    try:
        sender_email = "arquiticket@gmail.com"

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
        connection.login(user=sender_email, password="vmpfavtatdoftaby")
        print("Login success")

        connection.sendmail(from_addr=sender_email, to_addrs=ticket.user_id,
                            msg=message.as_string())

        connection.close()
        print("Connection closed")
    except Exception:
        return False
    return True
