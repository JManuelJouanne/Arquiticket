import React, { useState, useContext } from "react"
import { EyeIcon, EyeSlashIcon } from "@heroicons/react/24/outline"
import { AccountContext } from "./Account"
import UserPool from "../UserPool"
import classNames from "classnames"
import { CognitoUser } from "amazon-cognito-identity-js"

const LogingSubmitForm = ({setStatus}) => {
    const [islogingIn, setIsLogingIn] = useState(true)
    const [name, setName] = useState("");
    const [lastname, setLastname] = useState("");
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [isPasswordVisible, setIsPasswordVisible] = useState(false)
    const [error, setError] = useState(null)
    const [isWritingPassword, setIsWritingPassword] = useState(false)
    const [emailVerification, setEmailVerification] = useState(false);
    const [verificationCode, setVerificationCode] = useState("");

    const { authenticate } = useContext(AccountContext)

    //Funcion que solicita creacion de usuarios
    const onSubmit = async (event) => {
        if (islogingIn) {
            event.preventDefault()

            authenticate(email, password)
                .then((data) => {
                    console.log("Logged in!", data)
                    setStatus(true)
                })
                .catch((err) => {
                    console.log(err)
                    setError("Email o contraseña incorrecta!")
                })
        } else {
            event.preventDefault()

            const attributes = [
                { Name: "name", Value: name },
                { Name: "family_name", Value: lastname },
            ];

            if (password === confirmPassword) {
                UserPool.signUp(email, password, attributes, null, (err, data) => {
                    if (err) {
                        console.log(err)
                        setError("La contraseña no cumple con los requisitos o email ya está en uso")
                    } else {
                        console.log(data)
                        setEmailVerification(true)
                        fetch(
                            `${process.env.REACT_APP_BACKEND_HOST}/user/`,
                            {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json"
                                },
                                body: JSON.stringify({
                                    "user_id": email,
                                    "money": 0,
                                })
                            }
                        )
                    }
                })
            } else {
                setError("Las contraseñas no coindicen!")
            }
        }
    }

    //Función para validar usuario con codigo enviado al mail, usando Cognito
    const handleVerificationSubmit = async (event) => {
        event.preventDefault();

        const user = new CognitoUser({
            Username: email,
            Pool: UserPool,
        })

        user.confirmRegistration(verificationCode, true, (err, data) => {
            if (err) {
                console.error(err);
            } else {
                console.log(data);
                setEmailVerification(false);
                setIsLogingIn(!islogingIn);
                setStatus(true);
            }
        });
    };


    return (
        <div className="flex mx-auto mt-4 max-w-md md:max-w-2xl rounded-lg bg-gray-200 p-6">
            {!emailVerification && (
            <form onSubmit={onSubmit}  className="flex-col w-full">
                <div className="flex justify-center text-lg border-b-2 pb-2 border-gray-800">
                    { islogingIn ? "Iniciar Sesión" : "Formulario Registro"}
                </div>
                <div className={classNames(error ? "flex justify-center mt-1 text-red-500" : "")}>
                    {error}
                </div>
                {!islogingIn && (
                    <div className="flex-col mt-2">
                        <label htmlFor="name">Nombre:</label>
                        <input
                            type="text"
                            value={name}
                            className="w-full rounded-md focus:outline-gray-800 px-2"
                            onChange={(event) => setName(event.target.value)}
                        />
                    </div>

                )}
                {!islogingIn && (
                    <div className="flex-col mt-2">
                        <label htmlFor="lastname">Apellido:</label>
                        <input
                            type="text"
                            value={lastname}
                            className="w-full rounded-md focus:outline-gray-800 px-2"
                            onChange={(event) => setLastname(event.target.value)}
                        />
                    </div>
                )}
                <div className="flex-col mt-2">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        value={email}
                        className="w-full rounded-md focus:outline-gray-800 px-2"
                        onChange={(event) => setEmail(event.target.value)}
                    />
                </div>
                <div className="flex-col mt-2">
                    <label htmlFor="password">Contraseña:</label>
                    <div className="flex">
                        <input
                            type={isPasswordVisible ? "text" : "password"}
                            value={password}
                            className="w-full rounded-l-md focus:outline-gray-800 px-2"
                            onChange={(event) => setPassword(event.target.value)}
                            onFocus={() => {setIsWritingPassword(true)}}
                            onBlur={() => {setIsWritingPassword(false)}}
                        />
                        <button
                            type="button"
                            className="flex bg-gray-600 text-white px-1 rounded-r-md hover:bg-gray-700"
                            onClick={() => {
                                setIsPasswordVisible(!isPasswordVisible)
                            }}
                        >
                            {isPasswordVisible ? <EyeIcon className="h-6 w-6"/> : <EyeSlashIcon className="h-6 w-6"/>}
                        </button>

                    </div>
                    <div className={classNames(isWritingPassword && !islogingIn ?  "flex" : "hidden", "text-xs text-gray-700 ml-4")}>
                        {"La contraseña debe tener: 8 Caracteres Mínimo, 1 Letra Mayúscula, y 1 Letra Minúscula"}
                    </div>
                </div>
                {!islogingIn && (
                    <div className="flex-col mt-2">
                        <label htmlFor="Confirmpassword">Confirmar Contraseña:</label>
                        <div className="flex">
                            <input
                                type={isPasswordVisible ? "text" : "password"}
                                value={confirmPassword}
                                className="w-full rounded-l-md focus:outline-gray-800 px-2"
                                onChange={(event) => setConfirmPassword(event.target.value)}
                                onFocus={() => {setIsWritingPassword(true)}}
                                onBlur={() => {setIsWritingPassword(false)}}
                            />
                            <button
                                type="button"
                                className="flex bg-gray-600 text-white px-1 rounded-r-md hover:bg-gray-700"
                                onClick={() => {
                                    setIsPasswordVisible(!isPasswordVisible)
                                }}
                            >
                                {isPasswordVisible ? <EyeIcon className="h-6 w-6"/> : <EyeSlashIcon className="h-6 w-6"/>}
                            </button>
                        </div>
                        <div className={classNames(isWritingPassword ?  "flex" : "hidden", "text-xs text-gray-700 ml-4")}>
                            {"La contraseña debe tener: 8 Caracteres Mínimo, 1 Letra Mayúscula, y 1 Letra Minúscula"}
                        </div>
                    </div>
                )}
                <div className="flex justify-end">
                    <button
                        type="submit"
                        className="flex mt-4 px-2 py-1 bg-gray-600 text-white rounded-lg"
                    >
                        {islogingIn ? "Iniciar sesión" : "Registrarse"}
                    </button>
                </div>
                <div className="flex justify-center hover:text-gray-500">
                    <button
                        type="button"
                        className="flex text-sm"
                        onClick={() => {
                            setIsLogingIn(!islogingIn)
                            setError(null)
                        }}
                    >
                        {islogingIn ? "No tienes una cuenta? Crea una acá" : "Ya tienes una cuenta? Inicia Sesión acá"}
                    </button>
                </div>
            </form>
            )}

            {emailVerification && (
                <form onSubmit={handleVerificationSubmit}  className="flex-col w-full">
                    <div className="flex justify-center text-lg border-b-2 pb-2 border-gray-800">
                        { islogingIn ? "Iniciar Sesión" : "Confirma tu Email"}
                    </div>
                    <div className={classNames(error ? "flex justify-center mt-1 text-red-500" : "")}>
                        {error}
                    </div>
                    <div className="flex-col mt-2">
                        <label htmlFor="verificationCode">Código de Verificación:</label>
                        <input
                            type="text"
                            value={verificationCode}
                            className="w-full rounded-md focus:outline-gray-800 px-2"
                            onFocus={() => {setIsWritingPassword(true)}}
                            onBlur={() => {setIsWritingPassword(false)}}
                            onChange={(event) => setVerificationCode(event.target.value)}
                        />
                    </div>
                    <div className={classNames(isWritingPassword ?  "flex" : "hidden", "text-xs text-gray-700 ml-4")}>
                        {"Enviamos un código de verificación a tu correo electrónico"}
                    </div>
                    <button
                        type="submit"
                        className="flex mt-4 px-2 py-1 bg-gray-600 text-white rounded-lg">
                        Confirmar
                    </button>
                </form>
            )}
        </div>
    )
}

export default LogingSubmitForm
