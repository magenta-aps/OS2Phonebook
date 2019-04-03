export default {
  methods: {
    getOrgIcon (locationType) {
      if (locationType === 'Telefon') {
        return 'phone'
      } else if (locationType === 'Henvendelsessted') {
        return 'map-marker-alt'
      } else if (locationType === 'Email') {
        return 'envelope'
      } else if (locationType === 'Webadresse') {
        return 'globe'
      } else if (locationType === 'EAN Nummer') {
        return 'list-ol'
      } else if (locationType === 'P-nummer') {
        return 'list-ol'
      } else if (locationType === 'Lokation') {
        return 'book'
      }
      return null
    },
    getPersonIcon (locationType) {
      if (locationType === 'PHONE') {
        return 'phone'
      } else if (locationType === 'DAR') {
        return 'map-marker-alt'
      } else if (locationType === 'EMAIL') {
        return 'envelope'
      } else if (locationType === 'WWW') {
        return 'globe'
      } else if (locationType === 'EAN') {
        return 'list-ol'
      } else if (locationType === 'PNUMBER') {
        return 'list-ol'
      } else if (locationType === 'TEXT') {
        return 'book'
      }
      return null
    }
  }
}
