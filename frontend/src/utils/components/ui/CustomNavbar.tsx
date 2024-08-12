import { Avatar, Button, DarkThemeToggle, Dropdown, FloatingLabel, Modal, Navbar } from "flowbite-react";
import { Link } from "wouter";
import { CustomNavbarLink } from "./CustomNavbarLink";
import { useEffect, useState } from "react";
import { useGetLocalStorage, useRemoveLocalStorage, useSetLocalStorage } from "@/utils/hooks/local-storage";
import { usePostFetch } from "@/utils/hooks/fetch-data";
import { SERVER_LOCAL } from "@/utils/constants/server";
import { ResponseLogin, ResponseRegister, UserContent } from "@/utils/domain/types/responses.type";
import { BodyLogin, BodyRegister } from "@/utils/domain/types/body.type";
import { toast } from "react-toastify";

export function CustomNavbar() {
    const [isAuth, setIsAuth] = useState(false)
    const [currentUser, setCurrentUser] = useState<UserContent | null>(null)
    const [openModalRegister, setOpenModalRegister] = useState(false);
    const [openModalLogin, setOpenModalLogin] = useState(false);


    const [usernameRegister, setUsernameRegister] = useState("")
    const [emailRegister, setEmailRegister] = useState("")
    const [passwordRegister, setPasswordRegister] = useState("")

    const [usernameLogin, setUsernameLogin] = useState("")
    const [passwordLogin, setPasswordLogin] = useState("")

    useEffect(() => {
        const authToken = useGetLocalStorage("token")
        const myUser = useGetLocalStorage('user')
        const exec_async = async () => {

            // const response = await usePostFetch<ResponseLogin, BodyLogin>(SERVER_LOCAL, { data: { "username": usernameLogin, "password": passwordLogin } }) as ResponseLogin
        }
        if (authToken && myUser) {
            setIsAuth(true)
            setCurrentUser(JSON.parse(myUser) as UserContent)
            exec_async()
        }
    }, [])
    return (
        <Navbar fluid rounded border>
            <Navbar.Brand as={Link} href="https://flowbite-react.com">
                <img src="/vite.svg" className="mr-3 h-6 sm:h-9" alt="Vite Logo" />
                <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Inventory Management</span>
            </Navbar.Brand>
            <div className="flex md:order-2 space-x-3">
                <DarkThemeToggle />
                {
                    isAuth ?
                        <Dropdown
                            arrowIcon={false}
                            inline
                            label={
                                <Avatar alt="User settings" img="https://flowbite.com/docs/images/people/profile-picture-5.jpg" rounded />
                            }
                        >
                            <Dropdown.Header>
                                <span className="block text-sm">{currentUser?.username}</span>
                                <span className="block truncate text-sm font-medium">{currentUser?.email}</span>
                            </Dropdown.Header>
                            <Dropdown.Item onClick={() => {
                                useRemoveLocalStorage('token')
                                useRemoveLocalStorage('user')
                                setIsAuth(false)
                            }}>Cerrar sección</Dropdown.Item>
                        </Dropdown>
                        :
                        <>
                            <Button outline color="primary" onClick={() => setOpenModalRegister(true)}>Registrarse</Button>
                            <Button color="primary" onClick={() => setOpenModalLogin(true)}>Iniciar sección</Button>
                        </>
                }


                <Navbar.Toggle />
            </div>
            <Navbar.Collapse>
                <CustomNavbarLink href="/">
                    Inventarios
                </CustomNavbarLink>
                <CustomNavbarLink href="/factura">
                    Facturas
                </CustomNavbarLink>
            </Navbar.Collapse>

            <Modal show={openModalLogin} onClose={() => setOpenModalLogin(false)}>
                <Modal.Header>Inicia Sección Ahora</Modal.Header>
                <Modal.Body>
                    <div className="space-y-6">
                        <FloatingLabel variant="outlined" label="username" onChange={(event) => setUsernameLogin(event.target.value)} />
                        <FloatingLabel variant="outlined" type="password" label="password" onChange={(event) => setPasswordLogin(event.target.value)} />
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button color="gray" onClick={() => setOpenModalLogin(false)}>
                        Cancelar
                    </Button>
                    <Button onClick={async () => {
                        const response = await usePostFetch<ResponseLogin, BodyLogin>(SERVER_LOCAL, {
                            path: '/api/v1/credentials/login/', data: {
                                username: usernameLogin,
                                password: passwordLogin
                            }
                        }) as ResponseLogin
                        if (response.token) {
                            useSetLocalStorage('user', JSON.stringify(response.user))
                            useSetLocalStorage('token', response.token)
                            setCurrentUser(response.user ?? null)
                            setIsAuth(true)
                            toast(`Bienvenido de nuevo ${response.user?.username}, te estábamos esperando`, { type: 'success' })
                        } else {
                            toast(response.detail, { type: 'warning' })
                        }
                        setOpenModalLogin(false)
                    }}>Iniciar sección</Button>
                </Modal.Footer>
            </Modal>

            <Modal show={openModalRegister} onClose={() => setOpenModalRegister(false)}>
                <Modal.Header>Registro de usuario</Modal.Header>
                <Modal.Body>
                    <div className="space-y-6">
                        <FloatingLabel variant="outlined" label="username" onChange={(event) => setUsernameRegister(event.target.value)} />
                        <FloatingLabel variant="outlined" label="email" onChange={(event) => setEmailRegister(event.target.value)} />
                        <FloatingLabel variant="outlined" type="password" label="password" onChange={(event) => setPasswordRegister(event.target.value)} />

                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button color="gray" onClick={() => setOpenModalRegister(false)}>
                        Cancelar
                    </Button>
                    <Button onClick={async () => {
                        const response = await usePostFetch<ResponseRegister, BodyRegister>(SERVER_LOCAL, {
                            path: '/api/v1/credentials/', data: {
                                email: emailRegister,
                                username: usernameRegister,
                                password: passwordRegister
                            }
                        }) as ResponseRegister
                        if (response.token) {
                            // useSetLocalStorage('token', response.token)
                            toast(`Te haz registrado ${usernameRegister} exitosamente`, { type: 'success' })
                        } else {
                            toast(response.detail, { type: 'warning' })
                        }
                        setOpenModalRegister(false)
                    }}>Registrarse</Button>
                </Modal.Footer>
            </Modal>
        </Navbar>
    )
}