// Home.vue
const home = {
  template: '<div>Home</div>',
  
  computed: {
    username() {
      // 我们很快就会看到 `params` 是什么
      //return this.$route.params.username
      return ""
    },
  },
  methods: {
    render: function() {
      return "<div>Home2</div>"
    },
    goToDashboard() {
      //if (isAuthenticated) {
        this.$router.push('/dashboard')
      //} else {
      //  this.$router.push('/login')
      //}
    },
  },
}
export {home as Home}