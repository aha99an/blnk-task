<template>
    <h1>All fund</h1>
    <table border="1">
        <tr>
            <td>Max Amount</td>
            <td>Min Amount</td>
            <td>rate</td>
            <td>duration</td>
        </tr>
        <tr v-for="item in funds" :key="item.max_amount">

            <td>{{ item.max_amount }}</td>
            <td>{{ item.min_amount }}</td>
            <td>{{ item.rate }}</td>
            <td>{{ item.duration }}</td>
        </tr>
    </table>

    <h1>Add new fund</h1>
    <input type="number" v-model="min_amount" placeholder="Enter Min Amount" />
    <input type="number" v-model="max_amount" placeholder="Enter Max Amount" />
    <input type="number" v-model="rate" placeholder="Enter Interest Rate" />
    <input type="number" v-model="duration" placeholder="Enter Fund Duration in Years" />
    <button v-on:click="addFund">Add fund</button>
</template>

<script>
import axios from "axios"

export default {
    name: 'addFund',
    data() {
        return {
            max_amount: '',
            min_amount: '',
            rate: '',
            duration: '',
            funds: [],
        }
    },
    methods: {
        async allFunds() {
            const token = localStorage.getItem('token')
            const config = {
                headers: { Authorization: `Bearer ${token}` }
            };
            const bankerResponse = await axios.get("http://localhost:8000/funds/", config);

            this.funds = bankerResponse.data.results
        },

        async addFund() {
            const token = localStorage.getItem('token')
            const config = {
                headers: { Authorization: `Bearer ${token}` }
            };
            const data = {
                max_amount: this.max_amount,
                min_amount: this.min_amount,
                rate: this.rate,
                duration: this.duration,
            }
            const bankerResponse = await axios.post("http://localhost:8000/funds/", data, config);
            if (bankerResponse.status == 201) {
                this.$router.push({ name: 'BankerHome' });
                alert("The Fund created successfully");
            }

        },

    },
    mounted() {
        if (!localStorage.getItem('token')) {
            this.$router.push({ name: 'SignIn' })
        }
    },
    beforeMount() {
        this.allFunds()
    },
}
</script>