import { Navbar } from "flowbite-react";
import { useRoute } from "wouter";

interface Props {
    href: string
    children: React.ReactNode
}

export function CustomNavbarLink(props: Props) {
    const [isActive] = useRoute(props.href);
    return (
        <Navbar.Link color="primary" href={props.href} active={isActive}>
            {props.children}
        </Navbar.Link>
    )
}