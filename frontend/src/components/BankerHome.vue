<template>
    <h1>Bank personal home</h1>
    <div class="home">
        <button v-on:click="addFund">Funds</button>
        <button v-on:click="addLoan">Loans</button>
    </div>
</template>

<script>
export default {
    name: 'BankerHome',

    methods: {
        addFund() {
            this.$router.push({ name: 'addFund' })
        },
        addLoan() {
            this.$router.push({ name: 'addLoan' })
        },
    },

    mounted() {
        if (!localStorage.getItem('token')) {
            this.$router.push({ name: 'SignIn' })
        }
    }
}
</script>