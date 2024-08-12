import { CustomFlowbiteTheme } from "flowbite-react";


export const customTheme: CustomFlowbiteTheme = {
    button: {
        color: {
            primary: "bg-primary-500 hover:bg-primary-600 text-white dark:bg-primary-600 dark:hover:bg-primary-700",
        },
    },
    navbar: {
        link: {
            active: {
                on: "text-primary-500 font-medium hover:text-primary-600 active:text-primary-400",
                off: "hover:text-primary-600 active:text-primary-400 dark:hover:text-primary-600 dark:active:text-primary-400 dark:text-white"
            },
            base: "text-base"
        }
    }
};