Vue.component('todo-item', {
    props: ['todo'],
    template: `
            <div class="card tooltip" :data-tooltip="todo.description">
                <div class="card-content">
                    <div class="field">
                        <div class="control">
                            <label class="checkbox">
                                <input type="checkbox">
                                {{todo.title}}
                            </label>
                        </div>
                    </div>
                </div>
            </div>`
})

var app = new Vue({
    el: '#app',
    data: {
        inputMongo: 'Test',
        inputEs: 'Test',
        todosMongo: [],
        todosEs: []
    },
    watch: {
        inputMongo() {
            axios
                .get('http://localhost:5000/mongo?q=' + this.inputMongo)
                .then(response => (this.todosMongo = response.data))
        },
        inputEs() {
            axios
                .get('http://localhost:5000/es?q=' + this.inputEs)
                .then(response => (this.todosEs = response.data))
        }
    },
    mounted() {
        axios
            .get('http://localhost:5000/mongo?q=' + this.inputMongo)
            .then(response => (this.todosMongo = response.data));

        axios
            .get('http://localhost:5000/es?q=' + this.inputEs)
            .then(response => (this.todosEs = response.data));
    }
});
