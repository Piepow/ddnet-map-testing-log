const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = {
  entry: "./resources/assets/app.js",
  output: {
    filename: "app.js",
    path: path.resolve(__dirname, "public/assets"),
    publicPath: "/assets/"
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          // fallback to style-loader in development
          MiniCssExtractPlugin.loader,
          "css-loader",
          "sass-loader"
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "app.css",
    }),
    new CopyWebpackPlugin([
      {
        from: path.resolve(__dirname, "resources/assets/svg"),
        to: path.resolve(__dirname, "public/assets")
      }
    ])
  ],
  optimization: {
    minimizer: [new OptimizeCSSAssetsPlugin({})]
  }
};
