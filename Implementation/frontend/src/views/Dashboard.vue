<template>
    <div>
        <h1>Welcome to FurBot</h1>
        <PetList />
    </div>
</template>

<script>
import PetList from '../components/PetList.vue';


export default {
    components: {
        PetList
    }
};
</script>