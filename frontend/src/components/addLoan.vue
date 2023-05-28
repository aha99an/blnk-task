<template>
    <h1>Add loan</h1>
</template>
  


<script>
  export default {
    name: 'addLoan',
    mounted()
    {
        if(!localStorage.getItem('user-info'))
        {
            this.$router.push({name:'SignIn'})
        }
    }
}
</script>