/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          main: '#3366FF',
          dark: '#1A1A3F',
        },
        secondary: {
          teal: '#00B3A6',
          yellow: '#FFD700',
        },
        neutral: {
          light: '#F4F4F4',
          dark: '#333333',
        }
      },
      fontFamily: {
        heading: ['Nunito', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'h1': ['3rem', { lineHeight: '1.2' }],
        'h2': ['2.25rem', { lineHeight: '1.3' }],
        'h3': ['1.75rem', { lineHeight: '1.4' }],
        'body': ['1rem', { lineHeight: '1.5' }],
        'small': ['0.875rem', { lineHeight: '1.5' }],
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(90deg, #3366FF 0%, #00B3A6 100%)',
        'gradient-background': 'linear-gradient(180deg, #F4F4F4 0%, #FFFFFF 100%)',
      },
    },
  },
  plugins: [],
}
