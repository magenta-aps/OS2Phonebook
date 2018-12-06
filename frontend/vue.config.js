module.exports = {
  pluginOptions: {
    i18n: {
      locale: 'da',
      fallbackLocale: 'en',
      localeDir: 'i18n',
      enableInSFC: true
    }
  },

  devServer: {
    proxy: {
      '/service': {
        target: process.env.BASE_URL || '10.0.3.187/solr',
        changeOrigin: true
      }
    }
  }
}
