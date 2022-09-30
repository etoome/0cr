const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		colors: {
			// https://dribbble.com/shots/17373528-Year-of-the-Tiger
			primary: '#f65a43',
			accent: '#341302',
			secondary: '#f6ae48',
			background: '#ffdcbe',
			white: '#ffffff'
		}
	},
	plugins: []
};
