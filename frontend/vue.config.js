const { defineConfig } = require('@vue/cli-service');
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new MonacoWebpackPlugin({
        languages: ['javascript', 'typescript', 'python'], // Add the languages you need
      }),
    ],
  },
  devServer: {
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  },
});