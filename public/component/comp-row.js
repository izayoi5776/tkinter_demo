Vue.defineComponent('todo_item', {
  name: 'todo_item',
  prpos: ['todo'],
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
    axios
    .get('/rest/' + this.todo)
    .then(response => (this.info = response))
    .catch(error => console.log(error))
  },
template:`
  <tr>
  <td>{{ info.data.search_target }}</td>
  <td>{{ info.data.type }}</td>
  <td v-html="rdoc"></td>
  </tr>`
})
