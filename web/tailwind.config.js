/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: theme => ({
        'mesh': "url('/src/assets/mesh-33.png')",
      }),
    },
  },
  plugins: [],
}

