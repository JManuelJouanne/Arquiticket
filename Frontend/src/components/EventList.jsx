import { useEffect, useState } from "react"
import { ChevronDownIcon } from "@heroicons/react/24/outline"
import { w3cwebsocket } from 'websocket'
import { PageController } from "./PageController"
import { BuyTickets } from "./BuyTickets"
import { MoneyManager } from "./Money"
import classNames from "classnames"

export const EventDetail = ({ number, page, count, event, email, socket }) => {
    const [displayDetails, setDisplayDetails] = useState(false)

    return (
        <div className="mb-2 shadow-lg rounded-lg flex-col">
            <div
                className={classNames(
                    "text-sm text-white bg-gray-700 px-4 py-2  border-b border-gray-800 flex hover:bg-gray-800",
                    "cursor-pointer",
                    displayDetails ? "rounded-t-lg" : "rounded-lg"
                )}
                onClick={() => {setDisplayDetails(!displayDetails)}}
                aria-hidden
            >
                <div className="flex w-[99%]">
                    <p>{number + (page - 1) * count + 1}. {event.name}</p>
                </div>
                <div className="flex" >
                    <ChevronDownIcon className={classNames("w-6 h-5 transition", displayDetails ? "rotate-180" : "")}/>
                </div>
            </div>
            <div className={classNames(
                "bg-gray-300 px-4 py-2 rounded-b-lg",
                displayDetails ? "flex" : "hidden"
            )}>
                <div className="flex">
                    <div className="border border-gray-800 flex-col min-w-[60px] text-center text-xs">
                        <p>Fecha</p>
                        <p className="bg-gray-400">Precio</p>
                        <p>Cantidad</p>
                        <p className="bg-gray-400">Lugar</p>
                        <p>Latitud</p>
                        <p className="bg-gray-400">Longuitud</p>
                    </div>
                    <div className="border border-gray-800 border-l-0 flex-col min-w-[120px] text-xs">
                        <p className="px-2">{event.date}</p>
                        <p className="bg-gray-400 px-2">{event.price}</p>
                        <p className="px-2">{event.quantity}</p>
                        <p className="bg-gray-400 px-2">{event.location}</p>
                        <p className="px-2">{event.latitude}</p>
                        <p className="bg-gray-400 px-2">{event.longitude}</p>
                    </div>
                </div>
                <BuyTickets event={event} email={email} socket={socket} />
            </div>
        </div>
    )
}

export const EventList = ({email}) => {
    const [events, setEvents] = useState([])
    const [page, setPage] = useState(1)
    const [count, setCount] = useState(25)
    const [socket, setSocket] = useState(null)

    useEffect(() => {
        const socket = new w3cwebsocket(`${process.env.REACT_APP_BACKEND_HOST_WS}/ws/sales`) //editar
        setSocket(socket)

        socket.onopen = () => {
          console.log('Conexión establecida')
        };

        socket.onmessage = (message) => {
            console.log('Mensaje recibido:', message.data)
            const data = JSON.parse(message.data)
            for (let i = 0; i < events.length; i++) {
                if (events[i].id === data.event_id) {
                    if (data.user_id === "admin") {
                        events[i].quantity += data.quantity
                    } else {
                        events[i].quantity -= data.quantity
                    }
                    //setEvents(events)
                    setEvents([...events])
                }
            }
        }

        return () => {
          socket.close();
        }
    }, [])

    useEffect(() => {
        fetch(
            `${process.env.REACT_APP_BACKEND_HOST}/events/?page=${page}&count=${count}`,
            { method: "GET" }
        )
        .then(response => response.json())
        .then(data => {setEvents(data)})
    }, [page, count])
    return (
        <div className="mx-8 my-4 p-4 flex-row">
            <MoneyManager email={email}/>
            <div className="text-xl py-1 mb-4 flex justify-center border-b-2 border-gray-800">
                LISTA DE EVENTOS EVENTS/CHILE
            </div>
            <PageController page={page} count={count} setPage={setPage} setCount={setCount} />
            {events[0] ? (
                events.map((event, number) => (
                    <div key={number}>
                        <EventDetail number={number} page={page} count={count} event={event} email={email} socket={socket}/>
                    </div>
                ))
            ) : (
                <p>No se encontraron resultados</p>
            )}
        </div>
    )
}
