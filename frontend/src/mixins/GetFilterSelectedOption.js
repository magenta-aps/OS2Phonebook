export default {
  methods: {
    getFilterSelectedOption (option, results, inputVal) {
      if (option) {
        if (option === 'emails') {
          return results.filter(result => {
            const res = JSON.parse(result.document)
            return res.locations.some(loc => {
              // if we are searching in emails, inputVal needs to be on position 1 in a locations array whose 0th item === 'EMAIL' for the result to be valid.
              return loc[0] === 'EMAIL' && loc[1].indexOf(inputVal) !== -1
            })
          })
        } else if (option === 'phone_numbers') {
          return results.filter(result => {
            const res = JSON.parse(result.document)
            return res.locations.some(loc => {
              return loc[0] === 'PHONE' && loc[1].indexOf(inputVal) !== -1
            })
          })
        } else if (option === 'job_titles') {
          return results.filter(result => {
            const res = JSON.parse(result.document)
            // only include results where the 3rd item in departments array contains our search string (3rd item is job title).
            return res.departments.some(dept => dept[3].indexOf(inputVal) !== 1)
          })
        }
      }
      return results
    }
  }
}
