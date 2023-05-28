import SignIn from './components/SignIn.vue'
import BankerHome from './components/BankerHome.vue'
import { createRouter, createWebHistory } from 'vue-router'
import addFund from './components/addFund.vue'
import addLoan from './components/addLoan.vue'
import MyHome from './components/MyHome.vue'
import ProviderFund from './components/ProviderFund.vue'

const routes = [
    {
        name: 'BankerHome',
        component: BankerHome,
        path: '/BankerHome'
    },
    {
        name: 'SignIn',
        component: SignIn,
        path: '/sign-in'
    },
    {
        name: 'addFund',
        component: addFund,
        path: '/add-fund'
    },
    {
        name: 'addLoan',
        component: addLoan,
        path: '/add-loan'
    },
    {
        name: 'ProviderFund',
        component: ProviderFund,
        path: '/ProviderFund'
    },
    {
        name: 'MyHome',
        component: MyHome,
        path: '/'
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});
export default router;