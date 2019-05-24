const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
   entry: './main.js',
   output: {
      path: path.join(__dirname, '/assets/js'),
      filename: 'script.js'
   },
   devServer: {
      inline: true,
      host: '0.0.0.0',
      port: 3000
   },
   node: {
      fs: 'empty',
      net: 'empty',
      tls: 'empty',
    },
   module: {
      rules: [
         {
            test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
               presets: ['@babel/react', '@babel/preset-env']
            }
         },
         {
            test: /\.styl$/,
            use: [
              'style-loader',
              'css-loader',
              {
                loader: 'stylus-loader',
              },
            ],
          },
          {
            test: /\.css?$/,
            use: [
              'style-loader',
              {
                loader: 'css-loader',
              },
            ],
          }
      ]
      
   },
   plugins:[
      new HtmlWebpackPlugin({
         template: './index.html'
      })
   ]
}