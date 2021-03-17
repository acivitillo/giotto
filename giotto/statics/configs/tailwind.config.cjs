const colors = require('tailwindcss/colors')
const tailwindcss = require('tailwindcss');
const plugin = require('tailwindcss/plugin')

module.exports = {
    theme: {
        extend: {
            colors: {
                'light-blue': colors.lightBlue,
                cyan: colors.cyan,
                dark: '#444',
                cgrey_200: '#919191',
                cgrey_300: '444444e1',
                light: '#f8f9fa',
                white: '#fff',
                orange: '#e98300',
            },
        },
    },
    variants: {},
    plugins: [
        tailwindcss('./tailwind.config.cjs'),
        require('autoprefixer'),
        require('@tailwindcss/typography'),
        plugin(function ({ addUtilities }) {
            const newUtilities = {
                '.selected': {
                    "background-color": '#e98300',
                }
            }

            addUtilities(newUtilities)
        }),
    ],
};