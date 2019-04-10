export default {
  methods: {
    getIcon (locationType) {
      if (locationType === 'PhoneEmployee') {
        return 'phone'
      } else if (locationType === 'PhoneUnit') {
        return 'phone'
      } else if (locationType === 'AdresseHenvendelsessted') {
        return 'map-marker-alt'
      } else if (locationType === 'AdressePostEmployee') {
        return 'map-marker-alt'
      } else if (locationType === 'EmailEmployee') {
        return 'envelope'
      } else if (locationType === 'EmailUnit') {
        return 'envelope'
      } else if (locationType === 'WebUnit') {
        return 'globe'
      } else if (locationType === 'EAN') {
        return 'list-ol'
      } else if (locationType === 'p-nummer') {
        return 'list-ol'
      } else if (locationType === 'LocationUnit') {
        return 'book'
      } else if (locationType === 'LocationEmployee') {
        return 'book'
      }
      return null
    }
  }
}
