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
import axios from 'axios';

export default {
    name: "MapPage",
    setup() {
        const map = ref(null);
        const center_cities = ref([]);
        const get_city = ref(null);
        const currentClick = reactive({ latitude: null, longtitude: null }); // 存储当前点击的坐标

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

        function radians(degrees) {
            return degrees * (Math.PI / 180);
        }

        // click potin coordinates
        const click_lon = 109.00;
        const click_lat = 40.00;

        const choose_radius = 200;

        function haversine(lon1, lat1, lon2, lat2) {
            //Earth Radius
            const R = 6371;
            const difference_lat = radians(lat2 - lat1);
            const difference_lon = radians(lon2 - lon1);

            const half_eqution = Math.sin(difference_lat / 2) * Math.sin(difference_lat / 2) + Math.cos(radians(lat1)) * Math.cos(radians(lat2)) * Math.sin(difference_lon / 2) * Math.sin(difference_lon / 2);
            const final_eqution = 2 * Math.atan2(Math.sqrt(half_eqution), Math.sqrt(1 - half_eqution));

            const distance = R * final_eqution;
            return distance;
        }

        async function get_response_data() {
                try {
                    const city_response = await axios.get('http://localhost:5000/city/cities');
                    const cityData = city_response.data;
                    center_cities.value = cityData.map(city => ({
                        name: city.name,
                        center: city.center,
                        center_longtitude: city.center[0],
                        center_latitude: city.center[1],
                        geom: city.geom
                    }));
                const in_circle_cities = center_cities.value.filter(city => {
                        const distance = haversine(click_lon, click_lat, city.center_longtitude, city.center_latitude);
                        return distance <= choose_radius;
                });
                console.log(in_circle_cities)

                } catch (error) {
                    console.error(error)
                }
            }

        onMounted(() => {
            map.value = L.map("map").setView([33.3603, 108.5457], 6);
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

                currentClick.latitude = e.latlng.lat; // 纬度
                currentClick.longtitude = e.latlng.lng; // 经度
                console.log(`Location: Longtitude ${currentClick.longtitude}, Latitude ${currentClick.latitude}`);

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
            get_response_data();
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
        return {
            map,
            cities, 
            selectedCity, 
            selectedCityDetails, 
            showDetails,
            center_cities,
            get_city,
            get_response_data
        };
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