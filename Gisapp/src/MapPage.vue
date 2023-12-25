<template>
    <div class="container">
        <div id="map"></div>
        <div class="info-panel">
            <div class="basic-info">
                <h2>基本信息</h2>
                <div v-if="in_circle_cities.length > 0">
                <button v-for="city in in_circle_cities" :key="city.adcode" class="city-button" @click="showDetails(city.adcode)">
                    Name: {{ city.name }} Poupulation: {{ city.population }}
                </button>
                </div>
            </div>
            <div class="detailed-info">
                <h2>详细信息</h2>
                <p v-if="selectedCity">{{ selectedCityDetails }}</p>
            </div>
            <div class="scenic-info">
                <h2>景点信息</h2>
                <p v-if="selectedCityScenics">{{ selectedCityScenics }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { ref, onMounted, onUnmounted, reactive } from 'vue';  
import axios from 'axios';
import * as turf from '@turf/turf';

export default {
    name: "MapPage",
    setup() {
        const map = ref(null);
        const center_cities = ref([]);
        const get_city = ref(null);
        const currentClick = reactive({ latitude: null, longtitude: null });
        const in_circle_cities = ref([]);
        const select_scenic_data = ref(null);

        const selectedCity = ref('');
        const selectedCityDetails = ref('');
        // 显示城市的详细信息
        const showDetails = async (adcode) => {
            console.log("Selected City Adcode:", adcode);
            const selectedCityInfo = in_circle_cities.value.find(city => city.adcode === adcode);
            if (!selectedCityInfo) {
                selectedCityDetails.value = '未找到城市';
                return;
            }
            console.log("Selected City:", selectedCityInfo);

            selectedCity.value = selectedCityInfo.name;
            try {
                const detailedInfo = await get_info_details(selectedCityInfo);
                // 处理景点信息
                let scenicSpots = 'null';
                if (detailedInfo.info && detailedInfo.info.scenic_spots_info && detailedInfo.info.scenic_spots_info.length > 0) {
                    scenicSpots = detailedInfo.info.scenic_spots_info.map(spot => spot.scenic_spots_name).join(', ');
                }
                selectedCityDetails.value = `所属省: ${detailedInfo.province || 'null'}\n` +
                                            `child: ${(detailedInfo.info && detailedInfo.info.childrenNum) || 'null'}\n` +
                                            `级别: ${(detailedInfo.info && detailedInfo.info.level) || 'null'}\n` +
                                            `景点: ${scenicSpots}\n`;
                                            // `景点: ${((detailedInfo.info && detailedInfo.info.scenic_spots_info && detailedInfo.info.scenic_spots_info[0]) ? detailedInfo.info.scenic_spots_info[0].scenic_spots_name : 'null')}\n`;
            } catch (error) {
                console.error("Error in get_info_details:", error);
                selectedCityDetails.value = `所属省: null\nchild: null\n级别: null\n景点: null\n`;
            }
        };

        let largeCircle = ref(null); // 用于跟踪当前的大圆
        let smallCircle = ref(null); // 用于跟踪当前的小圆

        function radians(degrees) {
            return degrees * (Math.PI / 180);
        }

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

        function calculate_area(city) {
            city.geom.coordinates.forEach(polygon => {
                const coordinates = polygon[0];
                const turfPolygon = turf.polygon([coordinates]);
                const area = turf.area(turfPolygon);
                city.area = area;
            });
            return city;
        }


        async function get_scenic_data() {
            try {
                const scenic_response = await axios.get(`http://localhost:5000/scenic/scenic/id/1`)
                const scenicData = scenic_response.data;
                select_scenic_data.value = scenicData
                console.log("Scenic spots:", select_scenic_data.value)
            } catch (error) {
                console.error(`Error scenic id ${select_scenic_data.value.id}`)
            } 
        }

        async function get_province_data(city) {
            try {
                const province_response = await axios.get(`http://localhost:5000/province/province/${city.adcode}`)
                console.log(province_response);
                city.province = province_response.data.province;
                console.log(city);
                return city;
            } catch (error) {
                console.error(`Error adcode ${city.adcode}`)
            }
        }

        async function get_info_details(city) {
            try {
                const info_details_response = await axios.get(`http://localhost:5000/info/info/${city.adcode}`)
                console.log(info_details_response);
                city.info = info_details_response.data;
                console.log(city);
                return city;
            } catch (error) {
                console.error(`Error adcode ${city.adcode}`)
            }
        }

        async function get_response_data() {
                try {
                    const city_response = await axios.get('http://localhost:5000/city/cities');
                    const cityData = city_response.data;
                    center_cities.value = cityData.map(city => ({
                        adcode: city.adcode,
                        name: city.name,
                        center: city.center,
                        center_longtitude: city.center[0],
                        center_latitude: city.center[1],
                        geom: city.geom,
                        population: city.population
                    }));

                    in_circle_cities.value = center_cities.value.filter(city => {
                        const distance = haversine(currentClick.longtitude, currentClick.latitude, city.center_longtitude, city.center_latitude);
                        return distance <= choose_radius;
                    });

                    const add_province = in_circle_cities.value.map(city =>
                        get_province_data(city)
                    );
                    in_circle_cities.value = await Promise.all(add_province);

                    const add_info = in_circle_cities.value.map(city => 
                        get_info_details(city)
                    );
                    in_circle_cities.value = await Promise.all(add_info);

                    const add_area = in_circle_cities.value.map(city => 
                        calculate_area(city)
                    );
                    in_circle_cities.value = await Promise.all(add_area);

                    console.log(in_circle_cities)
                    get_scenic_data()
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

                showDetails(center_cities.value[0]);
                get_response_data();
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
        return {
            map,
            selectedCity, 
            selectedCityDetails, 
            select_scenic_data,
            get_scenic_data,
            showDetails,
            center_cities,
            get_city,
            get_response_data,
            currentClick,
            in_circle_cities
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
.city-button {
    margin: 10px 0;
    padding: 10px;
    border: 1px solid #007bff;
    background-color: #fff;
    color: #007bff;
    text-align: left;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s;
}

.city-button:hover {
    background-color: #007bff;
    color: #fff;
    cursor: pointer;
}
.container {
    display: flex;
    height: 100vh;
}
#map {
    width: 80%;
    height: 100%;
}
.detailed-info p {
    white-space: pre-line;
}
</style>