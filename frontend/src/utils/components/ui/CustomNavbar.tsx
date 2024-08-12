import { Avatar, Button, DarkThemeToggle, Dropdown, Navbar } from "flowbite-react";
import { Link } from "wouter";
import { CustomNavbarLink } from "./CustomNavbarLink";

export function CustomNavbar() {

    return (
        <Navbar fluid rounded>
            <Navbar.Brand as={Link} href="https://flowbite-react.com">
                <img src="/vite.svg" className="mr-3 h-6 sm:h-9" alt="Flowbite React Logo" />
                <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Flowbite React</span>
            </Navbar.Brand>
            <div className="flex md:order-2 space-x-3">
                <DarkThemeToggle />
                <Dropdown
                    arrowIcon={false}
                    inline
                    label={
                        <Avatar alt="User settings" img="https://flowbite.com/docs/images/people/profile-picture-5.jpg" rounded />
                    }
                >
                    <Dropdown.Header>
                        <span className="block text-sm">Bonnie Green</span>
                        <span className="block truncate text-sm font-medium">name@flowbite.com</span>
                    </Dropdown.Header>
                    <Dropdown.Item>Cerrar sección</Dropdown.Item>
                </Dropdown>
                <Button outline color="primary">Get started</Button>
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
        </Navbar>

    )
}