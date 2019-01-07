export default {
  methods: {
    // Depending on search criteria, return which field to perform the search in.
    getSearchFields (option) {
      if (option === 'emails' || option === 'phone_numbers') {
        // put option in an array, because the method 'SearchMultpleFields' expects second argument to be an array.
        return ['locations']
      } else if (option === 'job_titles') {
        return ['departments']
      } else if (option === 'departments') {
        return ['name']
      }
      return option ? [option] : ['name', 'locations', 'departments']
    }
  }
}
