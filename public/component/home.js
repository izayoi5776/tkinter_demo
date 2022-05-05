// Home.vue
const home = {
  template: `
    <div>
      <h2>sys.version</h2>
      <div>{{ info.data.version }}</div>
      <!--h1>Module List</h1-->
      <h2>sys.builtin_module_names</h2>
      <button
        v-for="(key, index) in info.data.builtin"
        type="button" 
        class="btn btn-outline-primary"
        v-on:click="this.btnclick(key)"
      >{{ key }}</button>
      <br>
      <h2>sys.modules</h2>
      <button
        v-for="(val, key, index) in info.data.ondisk"
        type="button" 
        class="btn btn-outline-info"
        v-on:click="this.btnclick(key)"
        :title="val"
      >{{ key }}</button>
      <h2>sys.stdlib_module_names</h2>
      <button
        v-for="(key, index) in info.data.other"
        type="button" 
        class="btn btn-outline-dark"
        v-on:click="this.btnclick(key)"
      >{{ key }}</button>
    </div>`,
  data () {
    return {
      info: {
        data: {
          search_target: '',
          type: '',
          doc: '',
          dir: []
        }
      },
    }
  },
  mounted () {
    axios
    .get('/module/list') 
    .then(response => (this.info.data = response.data))
  },
  methods: {
    btnclick: function(d) {
      this.$router.push('/detail/' + d);
    }
  }
}
export {home as Home}