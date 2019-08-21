import Search from '@/api/Search'

/**
 * Search employees and departments for the term specified by 'searchTerm' (string),
 * in the fields specified by searchFields (array)
 */
function SearchMultipleFields (searchTerm = '*', searchFields = ['*'], organisation, exact = false) {
  let searchResults = []

  searchFields.forEach(field => {
    const employeeSearch = Search.employees(field, searchTerm, organisation, exact)
      .then(response => {
        return response
      })
    const departmentSearch = Search.departments(field, searchTerm, organisation, exact)
      .then(response => {
        return response
      })
    searchResults = searchResults.concat([employeeSearch, departmentSearch])
  })
  return Promise.all(searchResults)
}

export { SearchMultipleFields }
