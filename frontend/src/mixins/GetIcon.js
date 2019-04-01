export default {
  methods: {
    getIcon (locationType) {
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
