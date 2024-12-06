import React, { useState, useContext, useEffect } from "react"
import LogingSubmitForm from "../components/LogingSubmitForm"
import { Navbar } from "../components/Navbar"
import { AccountContext } from "../components/Account"
import { EventList } from "../components/EventList"
import { MyTickets } from "../components/MyTickets"


export const MainPage = () => {
    const [status, setStatus] = useState(false)
    const [email, setEmail] = useState(false)
    const { getSession, logout } = useContext(AccountContext)
    const [reload, setReload] = useState(false)
    const [isMyTickets, setIsMyTickets] = useState(false)

    const endSesion = () => {
        logout()
        setStatus(false)
    }

    useEffect(() => {
        getSession()
            .then((session) => {
                setStatus(true)
                setEmail(session.idToken.payload.email)
                console.log("Session:", session)
            })
            .catch((err) => console.error(err))
    }, [getSession, reload, email, isMyTickets])

    return (
        <div>
            <div className="sticky top-0 z-50">
                <Navbar
                    status={status}
                    endSesion={endSesion}
                    reload={reload}
                    setReload={setReload}
                    setIsMyTickets={setIsMyTickets}
                />
            </div>
            {!status ? <LogingSubmitForm setStatus={setStatus}/> : null}
            {status && !isMyTickets ? <EventList email={email}/> : null}
            {status && isMyTickets ? <MyTickets email={email} isMyTickets={isMyTickets} /> : null}
        </div>
    )
}
