<template>
    <div class="container">
        <div id="map"></div>
        <div class="info-panel">
            <div class="radius">
                <h2>Choss Radius</h2>
                <input type="number" v-model="radius">
                <button class="radius-button" @click="confirmRadius">Confirm</button>
            </div>
            <div class="basic-info">
                <h2>Basic Information</h2>
                <!-- //  -->
                <!-- <button @click="toggleMarkers">Scenic Spots</button> -->
                <div v-if="in_circle_cities.length > 0">
                <button v-for="city in in_circle_cities" :key="city.adcode" class="city-button" @click="showDetails(city.adcode)">
                    Name: {{ city.name }} Poupulation: {{ city.population }}
                </button>
                </div>
            </div>
            <div class="detailed-info">
                <h2>Details</h2>
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
        const spot_info = ref(null);
        const scenic_points = ref([]);
        const showMarkers = ref(false);
        let markers = [];

        const selectedCity = ref('');
        const selectedCityDetails = ref('');
        const radius = ref('200');
        const choose_radius = ref(null);

        const showDetails = async (adcode) => {
            console.log("Selected City Adcode:", adcode);
            const selectedCityInfo = in_circle_cities.value.find(city => city.adcode === adcode);
            if (!selectedCityInfo) {
                selectedCityDetails.value = 'Do Not Find City';
                return;
            }
            console.log("Selected City:", selectedCityInfo);

            selectedCity.value = selectedCityInfo.name;
            try {
                const detailedInfo = await get_info_details(selectedCityInfo);

                let spot_name = "Null";
                if (detailedInfo.info && detailedInfo.info.scenic_spots_info && detailedInfo.info.scenic_spots_info.length > 0) {
                    spot_info.value = detailedInfo.info.scenic_spots_info;
                }
                spot_name = spot_info.value.map(spot => spot.scenic_spots_name).join(',');
                selectedCityDetails.value = `Province: ${detailedInfo.province || 'null'}\n` +
                                            `Lower Area Num: ${(detailedInfo.info && detailedInfo.info.childrenNum) || 'null'}\n` +
                                            `Level: ${(detailedInfo.info && detailedInfo.info.level) || 'null'}\n` +
                                            `Scenic Spots: ${spot_name}\n`;
            } catch (error) {
                console.error("Error in get_info_details:", error);
                selectedCityDetails.value = `Province: null\nLower Area Num: null\nLevel: null\nScenic Spots: null\n`;
            }
        };

        let largeCircle = ref(null); 
        let smallCircle = ref(null); 

        function radians(degrees) {
            return degrees * (Math.PI / 180);
        }

        function confirmRadius() {
            choose_radius.value = radius.value;
        }

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

        async function get_all_scenic() {
            try {
                const all_scenics_response = await axios.get('http://localhost:5000/scenic/all_scenic_spots')
                const all_scenic_data = all_scenics_response.data;
                scenic_points.value = all_scenic_data.map(spot => ({
                    coordinates: spot.geom.coordinates,
                    name: spot.scenic_spots_name
                }));
            } catch (error) {
                console.error(error)
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
                        console.log(choose_radius.value);
                        return distance <= choose_radius.value;
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
                    // get_scenic_data()
                } catch (error) {
                    console.error(error)
                }
            }


        onMounted(() => {
            if (document.getElementById('map')) {
                map.value = L.map("map").setView([33.3603, 108.5457], 5);
                L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                    attribution: "Map data &copy; OpenStreetMap contributors",
                }).addTo(map.value);
            }
            get_all_scenic()

            map.value.on('click', function(e) {
                // 移除之前的圆和标记
                if (largeCircle.value) {
                    largeCircle.value.remove();
                }
                if (smallCircle.value) {
                    smallCircle.value.remove();
                }

                currentClick.latitude = e.latlng.lat; 
                currentClick.longtitude = e.latlng.lng; 
                console.log(`Location: Longtitude ${currentClick.longtitude}, Latitude ${currentClick.latitude}`);

                largeCircle.value = L.circle(e.latlng, {
                    color: 'blue',
                    fillColor: '#f03',
                    fillOpacity: 0.5,
                    radius: 5 
                }).addTo(map.value);

                smallCircle.value = L.circle(e.latlng, {
                    color: 'green',
                    fillColor: '#0f3',
                    fillOpacity: 0.5,
                    radius: choose_radius.value * 1000
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
                map.value.remove(); 
                map.value = null;
            }
        });

        function toggleMarkers() {
            if (!map.value) {
                console.erroe("Map haven't init")
                return;
            }

            const myIcon = L.icon({
                iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
            });

            if (showMarkers.value) {
            scenic_points.value.forEach(spot => {
                const marker = L.marker([spot.coordinates[1], spot.coordinates[0]], { icon: myIcon});
                marker.bindPopup(spot.name);
                markers.push(marker);
                marker.addTo(map.value);
            });
            } else {
                markers.forEach(marker => marker.remove());
                markers = [];
            }

            showMarkers.value = !showMarkers.value;
        }
        

        // return { map, basicInfo: info.basicInfo, detailedInfo: info.detailedInfo };
        return {
            map,
            selectedCity, 
            selectedCityDetails, 
            select_scenic_data,
            // get_scenic_data,
            showDetails,
            center_cities,
            get_city,
            get_response_data,
            currentClick,
            in_circle_cities,
            toggleMarkers,
            scenic_points,
            get_all_scenic,
            confirmRadius,
            radius,
            choose_radius
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
    overflow-y: auto; 
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