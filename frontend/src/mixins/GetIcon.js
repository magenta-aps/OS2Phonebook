export default {
  methods: {
    getIcon (locationType) {
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
    }
  }
}
