import { useState } from "react"
import classNames from "classnames"
import { PlusIcon, MinusIcon } from "@heroicons/react/24/solid"

export const BuyTickets = ({event, email, socket}) => {
    const [amountToBuy, setAmountToBuy] = useState(1)
    const [buying, setBuying] = useState(false)

    const confirmBuy = async () => {
        try {
            const data = JSON.stringify({
                "user_id": email,
                "event_id": event.event_id,
                "quantity": amountToBuy
            })
            await fetch(
                `${process.env.REACT_APP_BACKEND_HOST}/events/buy/`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: data
                }
            )
            .then(response => response.json())
            .then(data => {
                if (data.detail === "Not enough money") {
                    alert("Dinero insuficiente para realzar esta transacción")
                } else {
                    alert(`Se compraron ${amountToBuy} tickets para ${event.name} con éxito!`)
                }}
            )
            socket.send(data)
        } catch(err) {
            console.log(err)
        } finally {
            setBuying(false)

        }
    }

    return(
        <div className="flex-col ml-4 text-sm">
            <div className="flex">
                <button
                    className={classNames(
                        "flex py-1 px-1  bg-gray-700 rounded-l-lg text-white  group border border-gray-800",
                        amountToBuy > 1 ? "hover:bg-gray-800 cursor-pointer" : "cursor-not-allowed"
                    )}
                    onClick={() => {
                        if (amountToBuy > 1) {
                            setAmountToBuy(amountToBuy - 1)
                        }
                    }}
                    disabled={amountToBuy <= 1}
                >
                    <MinusIcon
                        className={classNames(
                            "w-5 h-5",
                            amountToBuy > 1 ? "group-hover:scale-125 transition" : ""
                        )}
                    />
                </button>
                <div
                    className="flex py-[5px] px-3 bg-gray-600 text-white cursor-pointe font-bold border-b border-t border-gray-800"
                >
                    {amountToBuy}
                </div>
                <button
                    className="flex py-1 px-1  bg-gray-700 rounded-r-lg text-white hover:bg-gray-800 group border border-gray-800"
                    onClick={() => {setAmountToBuy(amountToBuy + 1)}}
                >
                    <PlusIcon className="w-5 h-5 group-hover:scale-125 transition"/>
                </button>
            </div>
            <div className="flex mt-2">
                TOTAL: ${amountToBuy * event.price}
            </div>
            <button
                className={classNames(
                    "text-white flex bg-gray-700 py-1 px-3 rounded-lg mt-2",
                    buying ? "cursor-not-allowed" : "hover:bg-gray-600"
                )}
                onClick={() => {
                    setBuying(true)
                    confirmBuy()
                }}
                disabled={buying}
            >
                Comprar entradas
            </button>
        </div>
    )
}
