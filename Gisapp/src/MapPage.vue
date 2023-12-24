<template>
    <div class="container">
        <div id="map"></div>
        <div class="info-panel">
            <div class="basic-info">
                <h2>基本信息</h2>
                <p v-for="(info, index) in cities" :key="index" @click="showDetails(info)">
                    {{ info.city }} (人口: {{ info.population }})
                </p>
            </div>
            <div class="detailed-info">
                <h2>详细信息</h2>
                <p v-if="selectedCity">{{ selectedCityDetails }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { ref, onMounted, onUnmounted, reactive } from 'vue';  

export default {
    name: "MapPage",
    setup() {
        const map = ref(null);
        const cities = reactive([
            { city: '预设城市1', population: '1000000', details: '景点1, 景点2' },
            { city: '预设城市2', population: '500000', details: '景点3, 景点4' },
            // 可以添加更多预设城市
        ]);
        const selectedCity = ref('');
        const selectedCityDetails = ref('');
        // 显示城市的详细信息
        const showDetails = (cityInfo) => {
            selectedCity.value = cityInfo.city;
            selectedCityDetails.value = cityInfo.details;
        };

        let largeCircle = ref(null); // 用于跟踪当前的大圆
        let smallCircle = ref(null); // 用于跟踪当前的小圆
        // const info = reactive({
        //     basicInfo: '',
        //     detailedInfo: ''
        // });

        onMounted(() => {
            map.value = L.map("map").setView([59.420161, 30.01832], 15);
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: "Map data &copy; OpenStreetMap contributors",
            }).addTo(map.value);

            map.value.on('click', function(e) {
                // 移除之前的圆和标记
                if (largeCircle.value) {
                    largeCircle.value.remove();
                }
                if (smallCircle.value) {
                    smallCircle.value.remove();
                }

                // const { lat, lng } = e.latlng;
                // const city = "预设城市";
                // const population = "预设人口";

                // // 更新信息
                // info.basicInfo = `坐标: ${lat.toFixed(5)}, ${lng.toFixed(5)}`;
                // info.detailedInfo = `城市: ${city}<br>人口: ${population}`;

                // 创建大圆
                largeCircle.value = L.circle(e.latlng, {
                    color: 'blue',
                    fillColor: '#f03',
                    fillOpacity: 0.5,
                    radius: 5 // 半径 5m
                }).addTo(map.value);

                // 创建小圆
                smallCircle.value = L.circle(e.latlng, {
                    color: 'green',
                    fillColor: '#0f3',
                    fillOpacity: 0.5,
                    radius: 200000 // 半径 200 公里
                }).addTo(map.value);

                showDetails(cities[0]);
            });    
        });

        onUnmounted(() => {
            if (largeCircle.value) {
                largeCircle.value.remove();
            }
            if (smallCircle.value) {
                smallCircle.value.remove();
            }
            if (map.value) {
                map.value.remove(); // 清理地图实例
            }
        });

        // return { map, basicInfo: info.basicInfo, detailedInfo: info.detailedInfo };
        return { map, cities, selectedCity, selectedCityDetails, showDetails };
    }
}
</script>

<style>
.info-panel {
    display: flex;
    flex-direction: column;
    width: 20%;
    padding: 20px;
    box-sizing: border-box;
    overflow-y: auto; /* 如果内容过多，可滚动查看 */
}
/* .basic-info, .detailed-info {
    flex: 1;
} */
.container {
    display: flex;
    height: 100vh;
}
#map {
    width: 80%;
    height: 100%;
}
</style>