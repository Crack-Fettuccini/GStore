const { defineConfig } = require('@vue/cli-service')
const fs = require('fs')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    server:{
      type:'https',
      options: {
        cert: fs.readFileSync('./cert/dev.local+4.pem'),
        key: fs.readFileSync('./cert/dev.local+4-key.pem'),
      },
    }
  }
})
