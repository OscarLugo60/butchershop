new Vue({
    el: '#app',
    delimiters: ['{$','$}'],
    data:{
        kword: '',
        lista_articulos: [],
        page: 1,
        pages: 1,
        i:1,
    },
    mounted(){
        var self = this;
        axios.get('/api/lista/')
            .then(function (response){
                self.pages = Math.ceil(response.data.count / 10); // Calcula el número de páginas. Dividimos la cantidad de items totales por el número de items mostrados en cada página
                self.lista_articulos = response.data;
            })
            .catch(function(error){
                console.log(error);
            })
    },
    watch:{
        kword: function(val){
            this.buscar_articulo(val);
        }
    },
    methods: {
        buscar_articulo: function(kword){
            var self = this;
            axios.get('/api/lista/?kword=' + kword)
                .then(function (response){
                    self.pages = Math.ceil(response.data.count / 10); // Calcula el número de páginas. Dividimos la cantidad de items totales por el número de items mostrados en cada página
                    self.lista_articulos = response.data;
                })
                .catch(function(error){
                    console.log(error);
                })
        },
        cambiarPagina: function(pagina, page){
            var self = this;
            axios.get(pagina)
                .then(function (response){
                    self.page = page;
                    self.pages = Math.ceil(response.data.count / 10); // Calcula el número de páginas. Dividimos la cantidad de items totales por el número de items mostrados en cada página
                    self.lista_articulos = response.data;
                })
                .catch(function(error){
                    console.log(error);
                })
        },
    },
})