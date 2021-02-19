const colors = require('tailwindcss/colors')
const tailwindcss = require('tailwindcss');

module.exports = {
    theme: {
        extend: {
            colors: {
                'light-blue': colors.lightBlue,
                cyan: colors.cyan,
                dark: '#444',
                light: '#f8f9fa',
                white: '#fff',
                orange: '#e98300'
            },
        },
    },
    variants: {},
    plugins: [
        tailwindcss('./tailwind.config.cjs'),
        require('autoprefixer'),
    ],
};