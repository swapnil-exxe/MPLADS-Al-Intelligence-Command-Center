/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        neo: {
          bg: '#FFFDF5',
          ink: '#000000',
          red: '#FF6B6B',
          yellow: '#FFD93D',
          violet: '#C4B5FD',
          white: '#FFFFFF',
          green: '#10B981',
          amber: '#F59E0B',
          darkred: '#DC2626',
        }
      },
      fontFamily: {
        sans: ['"Space Grotesk"', 'sans-serif'],
        mono: ['monospace'],
      },
      boxShadow: {
        'neo-sm': '4px 4px 0px 0px #000000',
        'neo': '8px 8px 0px 0px #000000',
        'neo-lg': '12px 12px 0px 0px #000000',
        'neo-xl': '16px 16px 0px 0px #000000',
        'neo-white': '8px 8px 0px 0px #FFFFFF',
      }
    },
  },
  plugins: [],
}
