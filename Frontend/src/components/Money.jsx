import { useEffect, useState } from "react"
import { PlusCircleIcon } from "@heroicons/react/24/outline"

export const MoneyManager = ({ email }) => {
    const [currentMoney, setCurrentMoney] = useState(0)
    const [moreMoney, setMoreMoney] = useState(0)

    useEffect(() => {
        fetch(
            `${process.env.REACT_APP_BACKEND_HOST}/user/wallet?user_id=${email}`,
            { method: "GET" }
        )
        .then(response => response.json())
        .then(data => {setCurrentMoney(data.money)})
    })

    const addMoney = async () => {
        try {
            const data = JSON.stringify({
                "user_id": email,
                "quantity": moreMoney,
            })
            await fetch(
                `${process.env.REACT_APP_BACKEND_HOST}/user/wallet`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: data
                }
            )
            alert(`Se agregaron $${moreMoney} a ${email} con éxito!`)
        } catch(err) {
            console.log(err)
        } finally {
            await fetch(
                `${process.env.REACT_APP_BACKEND_HOST}/user/wallet?user_id=${email}`,
                { method: "GET" }
            )
            .then(response => response.json())
            .then(data => {setCurrentMoney(data.money)})
        }
    }

    return(
        <div className="flex text-white mb-4">
            <div className="w-[99%] pl-4 bg-gray-700 rounded-l-lg py-1">Dinero actual: {currentMoney}</div>
            <input
                id="moneyAmount"
                type="number"
                min="0"
                max="1000000"
                className="bg-gray-600 py-1 px-4 min-w-[5%]"
                onChange={() => {setMoreMoney(parseInt(document.getElementById("moneyAmount").value))}}
            />
            <button
                type="button"
                className="flex min-w-[165px] py-1 hover:bg-gray-800 hover:cursor-pointer border border-gray-800 rounded-r-lg group px-4 bg-gray-700"
                onClick={() => {addMoney()}}
            >
                Agregar dinero
                <PlusCircleIcon className="w-5 h-5 mt-1 ml-1 group-hover:scale-110"/>
            </button>
        </div>
    )
}
