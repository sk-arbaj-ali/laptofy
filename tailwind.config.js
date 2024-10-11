/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./base/**/*.{html,js}",
    "./accounts/**/*.{html,js}",
    "./cart/**/*.{html,js}",
    "./orders/**/*.{html,js}",
    "./products/**/*.{html,js}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
        DEFAULT: '#3B82F6',
        50: '#f5f3ff',
        100: '#e0e7ff',
        200: '#ddd6fe',
        300: '#c4b5fd',
        400: '#a78bfa',
        500: '#8b5cf6',
        600: '#7c3aed',
        700: '#6d28d9',
        800: '#5b21b6',
        900: '#4c1d95'
        }
    }
    },
  },
  plugins: [],
}

