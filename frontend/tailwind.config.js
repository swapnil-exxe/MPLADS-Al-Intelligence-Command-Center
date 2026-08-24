/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f7ff',
          100: '#e0effe',
          500: '#0284c7',
          600: '#0265d2',
          900: '#0f172a',
        },
        emergency: {
          500: '#ef4444',
          600: '#dc2626',
          900: '#450a0a',
        }
      }
    },
  },
  plugins: [],
}
