<template>
    <h1>Sign in</h1>
    <div class="log">
        <input type="text" v-model="username" placeholder="Enter User name" />
        <input type="password" v-model="password" placeholder="Enter Password" />
        <button v-on:click="signIn">Sign In</button>
    </div>
</template>
  



<script>
import axios from "axios"
export default {
    name: 'SignIn',
    data() {
        return {
            username: '',
            password: '',
        }
    },
    methods: {
        async signIn() {
            const results = await axios.post("http://127.0.0.1:8000/api/token/", {
                username: this.username,
                password: this.password,
            });

            const token = results.data.access
            const userType = results.data.user_type

            localStorage.setItem("token", token)
            localStorage.setItem("userType", userType)
            this.$router.push({ name: 'MyHome' })
        },
    },

    mounted() {
        const token = localStorage.getItem('token')
        if (token) {
            this.$router.push({ name: 'MyHome' })
        }
    }
}
</script>
  




<style>
.log label select {
    width: 320px;
    height: 40px;
    border: 1px solid skyblue;
    background: skyblue;
    color: #fff;
    cursor: pointer;
}
</style>