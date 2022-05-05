// Item.vue
const item = {
  props: ["todo"],
  template:`
  <tr>
    <td><a :href="'?s=' + info.data.search_target">{{ info.data.search_target }}</a></td>
    <td>{{ info.data.type }}</td>
    <td v-html="rdoc"></td>
  </tr>`,
  data(){
    return {
      info: {
        data: {
          search_target: '',
          type: '',
          doc: '',
          dir: []
        }
      }
    }
  },
  computed:{
    rdoc : function(){
      try{
        return this.info.data.doc.replace(/\n/g, '<br>');
      } catch{
        return '';
      }
    }
  },
  mounted () {
    //print("this=" + this);
    //console.log("this.todo=" + this.todo);
    //print("prpos=" + this);
    axios
    .get('/rest/' + this.todo)
    .then(response => (this.info = response))
    .catch(error => console.log(error))
  },
}
export {item as Item}