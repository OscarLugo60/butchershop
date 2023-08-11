new Vue({
    el: '#app',
    delimiters: ['{$','$}'],
    data:{
        kword: '',
        lista_carrito: [],
        lista_articulos: [],
        dolar: 29.50,
        total: 0,
        mostrarModal: false,
        articuloSeleccionado: null,
        nuevaCantidad: 0
    },
    mounted(){
        var self = this;
        axios.get('/carshop/list/')
            .then(function (response){
                self.lista_carrito = response.data;
                console.log(self.lista_carrito);
            })
            .catch(function(error){
                console.log(error);
            })
    },
    watch:{
        kword: function(val){
            this.buscar_articulo(val);
        },
    },
    methods: {
        buscar_articulo: function(kword){
            var self = this;
            axios.get('/producto/api-list/?kword=' + kword)
                .then(function (response){
                    if(kword == ''){
                        self.lista_articulos.splice(0);
                    }
                    self.lista_articulos = response.data;
                    console.log(response.data);
                })
                .catch(function(error){
                    console.log(error);
                })
        },
        seleccionar: function(seleccion){
            this.kword = seleccion;
            this.lista_articulos.splice(0,this.lista_articulos.length);
        },
        actualizarTotal() {
            let total = 0;
            for (let articulo of this.lista_carrito) {
              total += articulo.product.sale_price * articulo.count;
            }
            return total;
          },
        guardarCantidad(id, cantidad) {
            numero = parseFloat(cantidad)
            console.log(id, numero)
            this.editandoCantidad = false;
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.put('http://127.0.0.1:8000/carshop/update/' +id + '/', {
                count: numero
            })
            .catch(function(error){
                console.log(error);
            });
            location.reload();
        },
        abrirModalEditar(articulo) {
            this.articuloSeleccionado = articulo;
            this.mostrarModal = true;
            console.log(articulo);
        },
        cerrarModal() {
            this.mostrarModal = false;
        },
        eliminarCarro(id) {
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios.defaults.xsrfCookieName = 'csrftoken';
            if(confirm('¿Estas seguro de eliminar este elemento?')){
                axios.delete('http://127.0.0.1:8000/carshop/delete/' +id + '/',)
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
                location.reload();
            }
            
        },
    },
})