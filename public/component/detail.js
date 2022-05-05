// Detail.vue
import {Item} from './item.js'

const detail = {
  template: `
    <div>
    <!-- breadcrumb  -->
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        <li 
          v-for="(b, index) in bread"
          class="breadcrumb-item"
          v-bind:class="{active: index < bread.length - 1}"
        >
          <a 
            v-if="index < bread.length - 1"
            v-bind:href="'?s=' + breadlink[index]"
          >{{ b }}</a>
          <span v-else>{{ b }}</span>
        </li>
        <!--li class="breadcrumb-item active" aria-current="page">Data</li-->
      </ol>
    </nav>
    <!-- self  -->
    <div class="container">
      <div class="row">
        <div class="col-5">
          <div class="card">
            <div class="card-header">
              type
            </div>
            <div class="card-body">
              <p class="card-text">{{ info.data.type }}</p>
            </div>
          </div>
          <br>
          <div class="card">
            <div class="card-header">
              pydoc.render_doc(..., renderer=pydoc.plaintext)
            </div>
            <div class="card-body">
              <p class="card-text" v-html="rpdoc"></p>
            </div>
          </div>
        </div>
        <div class="col-7">
          <div class="card">
            <div class="card-header">
              pydoc.render_doc(act, renderer=pydoc.html)
            </div>
            <div class="card-body">
              <p class="card-text" v-html="rpdoch"></p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- dir()  -->
    <br>
    <table class="table table-bordered table-hover">
      <tr class="table-primary">
        <th>dir( {{ info.data.search_target }} )</th>
        <th>type</th>
        <th>__doc__</th>
      </tr>
      <tr is='vue:Item'
        v-for="d in info.data.dir"
        v-bind:todo="info.data.search_target + '.' + d"
        v-bind:key="d"
      ></tr>
    </table>
  </div>`,

  data () {
    return {
      info: {
        data: {
          search_target: '',
          type: '',
          doc: '',
          pydoc: '',
          pydoch: '<div></div>',
          dir: []
        }
      },
    }
  },
  mounted () {
    const search_target = this.$route.params.target;
    axios
    .get('/rest/' + search_target)
    .then(response => {this.info = response})
    .catch(error => console.log(error))
  },
  computed:{
    bread: function() {
      return this.info.data.search_target.split('.');
    },
    breadlink: function() {
      ret = [this.bread[0]];
      for(var i = 1; i < this.bread.length; i++) {
        ret[i] = ret[i-1] + "." + this.bread[i];
      }
      return ret;
    },
    rdoc : function(){
      try{
        return this.info.data.doc.replace(/\n/g, '<br>');
      } catch{
        return '';
      }
    },
    rpdoc : function(){
      try{
        var ret = this.info.data.pydoc
        ret = ret.replace(/^(\s*[A-Z\s]+\s*)$/mg, '<b>$1</b>');
        ret = ret.replace(/\n/g, '<br>');
        return ret;
      } catch(e){
        console.log(e)
        return '';
      }
    },
    // rewrite <a> links
    rpdoch : function(){
      try{
        const div = this.htmlToElement(this.info.data.pydoch)
        const links = div.getElementsByTagName("a");
        //console.log(links.length)
        for (var i = 0; i < links.length; i++) {
          //links[i].setAttribute("target", "_blank");
          //console.log("i=" + i + " link=" + links[i])
          const href = links[i].getAttribute("href")
          if(href) {
            if(href.startsWith("http://") || href.startsWith("https://")) {
              // skip external links
              //console.log("skip external link: " + href)
            }else if(href.startsWith("#")) {
              // skip internal link
              //console.log("skip internal link: " + href)
            }else{
              // rewrite link
              const newhref = "?s=" + href.replace(/\.html/g, "")
              //console.log("i=" + i + "rewrite link: " + href + " to " + newhref)
              links[i].setAttribute("href", newhref);
            }
          }
        }
        //return div.outerHTML;
        return "DEBUG"
      } catch(e){
        console.log(e)
        return '';
      }
    }
  },
  methods:{
    /**
     * @param {String} HTML representing a single element
     * @return {Element}
     * @see https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
     */
    htmlToElement: function(html) {
        var template = document.createElement('template');
        //html = html.trim(); // Never return a text node of whitespace as the result
        template.innerHTML = html;
        return template.content.firstChild;
    }
  }
}
export {detail as Detail}