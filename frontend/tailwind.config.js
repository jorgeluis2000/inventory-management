const flowbite = require("flowbite-react/tailwind");

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    flowbite.content(),
  ],
  theme: {
    extend: {
      colors:{
        "primary": {
          100: "#ede1f2",
          200: "#dbc3e5",
          300: "#c9a5d7",
          400: "#b787ca",
          500: "#a569bd",
          600: "#845497",
          700: "#633f71",
          800: "#422a4c",
          900: "#211526"
},
      }
    },
  },
  plugins: [
    flowbite.plugin(),
  ],
}

