import Service from '@/api/HttpCommon'

export default {
  /**
   * Search for employees.
   * @param {String} key - search key.
   * @param {String} value - search value.
   * @returns {Array} a list of employees matching the query.
   */
  employees (key, value) {
    key = key || '*'
    value = value || '*'
    return Service.get(`/employees/select?q=${key}:${value}`)
      .then(response => {
        return response.data
      })
      .catch(error => {
        console.log(error.response)
      })
  },

  /**
   * Search for departments.
   * @param {String} key - search key.
   * @param {String} value - search value.
   * @returns {Array} a list of departments matching the query.
   */
  departments (key, value) {
    key = key || '*'
    value = value || '*'
    return Service.get(`/departments/select?q=${key}:${value}`)
      .then(response => {
        return response.data
      })
      .catch(error => {
        console.log(error.response)
      })
  }
}
