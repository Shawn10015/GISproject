<template>
    <div id="map"></div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { ref, onMounted } from 'vue';

export default {
    name: "MapPage",
    setup() {
        const map = ref(null);

        onMounted(() => {
            map.value = L.map("map").setView([59.420161, 30.01832], 15);
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: "Map data &copy; OpenStreetMap contributors",
            }).addTo(map.value);
        });

        return { map };
    }
}
</script>

<style>
#map {
    height: 100vh;
    width: 100%;
}
</style>