const path = require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const Dotenv = require('dotenv-webpack')
const env = process.env.NODE_ENV === 'production' ? (
  new webpack.EnvironmentPlugin({ ...process.env })
) : (
  new Dotenv()
)

module.exports = {
  devtool: 'source-map',
  mode: 'development',
  entry: './src/app.js',
  context: path.resolve(__dirname, 'frontend'),
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'frontend/dist')
  },
  module: {
    rules: [
      { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
      { test: /\.s(a|c)ss$/, use: ['style-loader', 'css-loader', 'sass-loader'] },
      { test: /\.woff2?$/, loader: 'file-loader' },
      { test: /\.(jpg|png|gif)$/, loader: 'file-loader' },
      { test: /\.tsx?$/, loader: 'ts-loader' }
    ]
  },
  devServer: {
    static: 'src',
    open: true,
    port: 8000,
    proxy: {
      '/api': { target: 'http://localhost:4000' }
    }
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    env,
    new HtmlWebpackPlugin({
      template: 'src/index.html',
      filename: 'index.html',
      inject: 'body'
    })
  ],
  resolve: {
    fallback: { fs: false },
    extensions: ['*', '.js', '.jsx', '.ts', '.tsx']
  }
}