import Service from '@/api/HttpCommon'

export default {
  /**
   * Search for an employee.
   * @param {String} query - search query.
   * @returns {Array} a list of employees matching the query.
   */
  employees (key, value) {
    key = key || '*'
    value = value || '*'
    return Service.get(`http://10.0.3.187/solr/employees/select?q=${key}:${value}`)
      .then(response => {
        return response.data
      })
      .catch(error => {
        console.log(error.response)
      })
  },
  /**
   * Search for an departments.
   * @param {String} query - search query.
   * @returns {Array} a list of departments matching the query.
   */
  departments (query) {
    query = query || ''
    return Service.get(`http://10.0.3.187/solr/departments/select?q=name:${query}`)
      .then(response => {
        return response.data
      })
      .catch(error => {
        console.log(error.response)
      })
  }
}
