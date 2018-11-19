import axios from 'axios'

/**
 * Defines the base url and headers for http calls
 */

const Service = axios.create({
  baseURL: '10.0.3.187/solr',
  headers: {}
})

export default {
  get (url) {
    return Service
      .get(url)
      .catch(err => {
        console.warn('request failed', err)

        return new Promise(function (resolve, reject) {
          reject(err)
        })
      })
  }
}
