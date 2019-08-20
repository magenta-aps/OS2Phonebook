import Service from '@/api/HttpCommon'

let parseAndSortResponseData = results => {
  let docs = results.data.response.docs

  if (docs.length === 0) {
    return []
  }

  // Sorting the data in SOLR requires extensions to the schema, due to the
  // way the 'name' field is tokenized for searching. Sorting in the UI has
  // minimal performance impact, so it should be good enough.
  let parsedDocs = docs.map(val => JSON.parse(val.document))
    .sort(function (a, b) {
      return a.name.localeCompare(b.name, 'da')
    })

  parsedDocs.forEach(doc => Object.values(doc).forEach(val => {
    if (val.constructor === Array) {
      val.sort(function (a, b) {
        return a[0].localeCompare(b[0], 'da')
      })
    }
  }))
  return parsedDocs
}

export default {
  /**
   * Search for employees.
   * @param {String} key - search key.
   * @param {String} value - search value.
   * @returns {Array} a list of employees matching the query.
   */
  employees (key, value, org) {
    key = key || '*'
    value = value || '*'
    org = org || '*'
    return Service.get(`/employees/select?fq=${key}:"${value}" AND root_uuid:"${org}"&rows=100000&q=*:*`)
      .then(response => {
        return parseAndSortResponseData(response)
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
  departments (key, value, org) {
    key = key || '*'
    value = value || '*'
    org = org || '*'
    return Service.get(`/departments/select?fq=${key}:"${value}" AND root_uuid:"${org}"&rows=100000&q=*:*`)
      .then(response => {
        return parseAndSortResponseData(response)
      })
      .catch(error => {
        console.log(error.response)
      })
  },

  roots () {
    return Service.get(`/departments/select?q=parent:ROOT&rows=100000`)
      .then(response => {
        return parseAndSortResponseData(response)
      })
      .catch(error => {
        console.log(error.response)
      })
  },

  treeView (key, value) {
    key = key || '*'
    value = value || '*'
    return Service.get(`/departments/select?q=${key}:${value}&rows=100000`)
      .then(response => {
        return parseAndSortResponseData(response)
      })
      .catch(error => {
        console.log(error.response)
      })
  }
}
