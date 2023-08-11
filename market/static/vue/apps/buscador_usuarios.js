new Vue({
    el: '#app',
    delimiters: ['{$','$}'],
    data:{
        kword: '',
        lista_usuarios: [],
        page: 1,
        pages: 1,
        i:1,
    },
    mounted(){
        var self = this;
        axios.get('/api/lista-usuarios/')
            .then(function (response){
                self.pages = Math.ceil(response.data.count / 10); // Calcula el número de páginas. Dividimos la cantidad de items totales por el número de items mostrados en cada página
                self.lista_usuarios = response.data;
            })
            .catch(function(error){
                console.log(error);
            })
    },
    watch:{
        kword: function(val){
            this.buscar_usuario(val);
        }
    },
    methods: {
        buscar_usuario: function(kword){
            var self = this;
            axios.get('/api/lista-usuarios/?kword=' + kword)
                .then(function (response){
                    self.pages = Math.ceil(response.data.count / 10); // Calcula el número de páginas. Dividimos la cantidad de items totales por el número de items mostrados en cada página
                    self.lista_usuarios = response.data;
                })
                .catch(function(error){
                    console.log(error);
                })
        },
        editar: function(usuario){
            var self = this;
            window.location.href = "http://127.0.0.1:8000/editar-usuario/"+ usuario;
        },
        eliminar: function(usuario){
            var self = this;
            window.location.href = "http://127.0.0.1:8000/eliminar-usuario/"+ usuario;
        },
        cambiarPagina: function(pagina, page){
            var self = this;
            axios.get(pagina)
                .then(function (response){
                    self.page = page;
                    self.pages = Math.ceil(response.data.count / 10); // Calcula el número de páginas. Dividimos la cantidad de items totales por el número de items mostrados en cada página
                    self.lista_usuarios = response.data;
                })
                .catch(function(error){
                    console.log(error);
                })
        },
    },
})