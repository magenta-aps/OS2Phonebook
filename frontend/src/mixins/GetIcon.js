export default {

  methods: {
    getIcon (locationType) {
      if (locationType === 'PHONE') {
        return 'phone'
      } else if (locationType === 'DAR') {
        return 'map-marker-alt'
      } else if (locationType === 'EMAIL') {
        return 'envelope'
      }
      return null
    }
  }
}
