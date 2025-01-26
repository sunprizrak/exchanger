/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.css",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
        "./node_modules/flowbite/**/*.js",
    ],
    darkMode: 'class',
    theme: {
        extend: {},
        screens: {
          sm: '480px',
          md: '768px',
          lg: '976px',
          xl: '1440px',
        },
    },
    plugins: [
        require('flowbite/plugin')
    ],
}

