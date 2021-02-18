## Setup webpack

Webpack is a tool to package css, js and other web formats.

> Getting Started guide [here](https://webpack.js.org/guides/getting-started/?_sm_au_=iVVWt45wJPs7QM0jVsBFjK664v423)

Initialize npm in the `assets` folder:

`cd assets`
`npm init -y`

### Install webpack:

`npm install webpack webpack-cli html-webpack-plugin mini-css-extract-plugin  babel-loader @babel/core --save-dev`

You should now have the below structure in `assets`

```bash
assets
├── package.json
├── node_modules
├── index.html
├── /src
    ├── index.js
```

### Install tailwind css

`npm install tailwindcss autoprefixer postcss-cli mini-css-extract-plugin postcss-loader css-loader --save-dev`

### Compiling with webpack

You can do:

`npm run start`

In order to run 1 compile. This will create a `/dist` folder inside `assets`. `dist` as `node_modules` is in the `gitignore` file so you need the build step in order to get this folder.

### Testing everything works

You can do a quick test by opening `assets/dist/index.html` in a browser.
