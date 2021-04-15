
# How to contribute to giotto

## First time setup

### Setup webpack

Webpack is a tool to package css, js and other web formats.

> Getting Started guide [here](https://webpack.js.org/guides/getting-started/?_sm_au_=iVVWt45wJPs7QM0jVsBFjK664v423)

Initialize npm in the `giotto/statics/configs` folder:

```bash
> cd giotto/statics/configs
> npm init -y
```

#### Install webpack

```bash
 > install webpack webpack-cli html-webpack-plugin mini-css-extract-plugin  babel-loader @babel/core --save-dev
```

You should now have the below structure in `statics`

```bash
statics
├── /configs
    ├── node_modules
    ├── src
    ├── index.html
    ├── package.json
```

#### Install npm packages

The npm packages are tracked inside `statics/configs/package.json`. In order to make sure you have all the npm packages installed, do the following:

```bash
> cd giotto/statics/configs
> npm install
```

This will save all the required npm packages inside the local folder `node_modules` inside `statics`.

#### Compiling with webpack

You can do:

```bash
> npm run start
```

In order to run 1 compile.

#### Watching with webpack

You can do:

```bash
> npx webpack --watch
```

To watch with webpack.
