import Search from '@/api/Search'

/**
 * Search employees and departments for the term specified by 'searchTerm' (string),
 * in the fields specified by searchFields (array)
 */
function SearchMultipleFields (searchTerm = '*', searchFields = ['*'], organisation) {
  let searchResults = []

  searchFields.forEach(field => {
    const employeeSearch = Search.employees(field, searchTerm, organisation)
      .then(response => {
        let employeeResults = response.response.docs.length > 0 ? response.response.docs : []
        return employeeResults
      })
    const departmentSearch = Search.departments(field, searchTerm, organisation)
      .then(response => {
        let departmentResults = response.response.docs.length > 0 ? response.response.docs : []
        return departmentResults
      })
    searchResults = searchResults.concat([employeeSearch, departmentSearch])
  })
  return Promise.all(searchResults)
}

export { SearchMultipleFields }
