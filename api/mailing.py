import smtplib


def send_notification(ticket, event, url):
    try:
        sender_email = "arquiticket@gmail.com"

        body = f"Se ha realizado una compra en ArquiTicket\n\nDetalles de la compra:\n" \
            f"Evento: {event.name}\n" \
            f"Cantidad de entradas: {ticket.quantity}\n" \
            f"Costo total: {event.price * ticket.quantity}\n\n" \
            f"Puede descargar sus tickets en: {url}\n\n" \
            f"Gracias por usar ArquiTicket"
        connection = smtplib.SMTP('smtp.gmail.com', 587)

        connection.starttls()
        # contraseña puede no funcionar en otros dispositivos talvez
        connection.login(user=sender_email, password="vmpfavtatdoftaby")
        print("Login success")

        connection.sendmail(from_addr=sender_email, to_addrs=ticket.user_id,
                            msg=f"Subject:Compra realizada en ArquiTicket\n\n{body}")

        connection.close()
        print("Connection closed")
    except Exception:
        return False
    return True
