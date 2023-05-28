<script>
export default {
    name: 'MyHome',
    mounted() {
        const token = localStorage.getItem('token')
        const userType = localStorage.getItem('userType')
        if (token) {
            switch (userType) {
                case 'banker':
                    this.$router.push({ name: 'BankerHome' })
                    break;
                case 'customer':
                    this.$router.push({ name: 'ProviderFund' })
                    break;
                case 'provider':
                    this.$router.push({ name: 'ProviderFund' })
                    break;
                default:
                    break;
            }
        } else {
            this.$router.push({ name: 'SignIn' })
        }
    }
}
</script>