import { useEffect, useState } from "react"
import { StatusContoller } from "./PageController"
import classNames from "classnames"

export const MyTickets = ({email, isMyTickets}) => {
    const [events, setEvents] = useState([])
    const [status, setStatus] = useState(1)

    useEffect(() => {
        fetch(
            `${process.env.REACT_APP_BACKEND_HOST}/tickets_user/?user_id=${email}&status=${status}`,
            { method: "GET" }
        )
        .then(response => response.json())
        .then(data => {
            setEvents(data)
        })
    }, [status, email, isMyTickets])

    return(
        <div className="mx-8 my-4 p-4 flex-row">
            <div className="text-xl py-1 mb-4 flex justify-center border-b-2 border-gray-800">
                MIS COMPRAS
            </div>
            <StatusContoller status={status} setStatus={setStatus} />
            {events[0] ? (
                events.map((event, number) => (
                    <div key={number} className="mx-2 mb-2 rounded-lg flex-col px-4 bg-gray-700 text-white py-2">
                        <p>Id del evento: {event.event_id}</p>
                        <p>Cantidad: {event.quantity}</p>
                        <p className={classNames(event.status === 1 ? "flex" : "hidden")}>
                            <a href={event.link}>Descargar</a>
                        </p>
                    </div>
                ))
            ) : (
                <p>No se encontraron resultados</p>
            )}
        </div>
    )
}
