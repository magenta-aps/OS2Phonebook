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
      '/solr': {
        target: 'http://10.0.3.187/',
        changeOrigin: true
      }
    }
  }
}
