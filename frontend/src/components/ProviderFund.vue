<template>
    <h1>Funds</h1>
    <div>
        <input type="number" v-model="searchAmount" placeholder="Enter the amount you have" />
        <button v-on:click="searchInFunds">search</button>
    </div>
    <table v-if="funds.length > 0" border="1">
        <tr>
            <td>ID</td>
            <td>Min Amount</td>
            <td>Max Amount</td>
            <td>rate</td>
            <td>duration</td>
        </tr>
        <tr v-for="item in funds" :key="item.max_amount">
            <td>{{ item.id }}</td>
            <td>{{ item.min_amount }}</td>
            <td>{{ item.max_amount }}</td>
            <td>{{ item.rate }}</td>
            <td>{{ item.duration }}</td>
        </tr>
    </table>

    <input type="number" v-model="amount" placeholder="Enter the amount you have" />
    <input type="number" v-model="fundId" placeholder="Enter the id of the fund" />
    <button v-on:click="createFund">submit</button>
</template>

<script>
import axios from "axios"

export default {
    name: 'ProviderFund',
    data() {
        return {
            searchAmount: '',
            funds: [],
            amount: null,
            fundId: null
        }
    },
    methods: {
        async searchInFunds() {
            const token = localStorage.getItem('token')
            const config = {
                headers: { Authorization: `Bearer ${token}` }
            };
            const params = {
                amount: this.searchAmount,
            }
            const response = await axios.get("http://localhost:8000/funds/providerFund/", config, { params });
            this.funds = response.data.results

        },
        async createFund() {
            const token = localStorage.getItem('token')
            const config = {
                headers: { Authorization: `Bearer ${token}` }
            };
            const data = {
                fund: this.fundId,
                amount: this.amount,
            }
            const response = await axios.post("http://localhost:8000/funds/providerFund/", data, config);
            alert(response.data.message)
        },
    },
    mounted() {
        if (!localStorage.getItem('token')) {
            this.$router.push({ name: 'SignIn' })
        }
    }
}
</script>