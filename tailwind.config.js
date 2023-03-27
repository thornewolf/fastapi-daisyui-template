/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/templates/**/*.html', './**/static/**/*.js',],
  theme: {
    fontFamily: {
    },
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
}
