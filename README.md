# Running the main application

```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/testapp`.

# Setup webpack

Webpack is a tool to package css, js and other web formats.

> Getting Started guide [here](https://webpack.js.org/guides/getting-started/?_sm_au_=iVVWt45wJPs7QM0jVsBFjK664v423)

Initialize npm in the `giotto/statics` folder:

`cd giotto/statics`
`npm init -y`

### Install webpack:

`npm install webpack webpack-cli html-webpack-plugin mini-css-extract-plugin  babel-loader @babel/core --save-dev`

You should now have the below structure in `statics`

```bash
statics
├── package.json
├── node_modules
├── index.html
├── /src
    ├── index.js
```

### Install npm packages

The npm packages are tracked inside `statics/package.json`. In order to make sure you have all the npm packages installed, do the following:

```bash
cd giotto/statics
npm install
```

This will save all the required npm packages inside the local folder `node_modules` inside `statics`.

### Compiling with webpack

You can do:

`npm run start`

In order to run 1 compile.

### Watching with webpack

You can do:

`npx webpack --watch`

To watch with webpack.

### Testing everything works

You can do a quick test by opening `giotto/statics/dist/index.html` in a browser.