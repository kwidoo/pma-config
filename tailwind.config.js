/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Adjust this path to where your HTML templates are located
  ],
  theme: {
    extend: {
      colors: {
        'waikawa-gray': {
          50: '#f2f7fb',
          100: '#e7f0f8',
          200: '#d3e2f2',
          300: '#b9cfe8',
          400: '#9cb6dd',
          500: '#839dd1',
          600: '#6a7fc1',
          700: '#6374ae',
          800: '#4a5989',
          900: '#414e6e',
          950: '#262c40',
        },
        // Add any other custom colors or extend existing ones
      },
      // Any additional customizations can go here
    },
  },
  plugins: [
    // Include any Tailwind plugins you might be using, for example:
    require('@tailwindcss/forms'), // If you're using Tailwind CSS Forms plugin
  ],
};
