<template>
    <div id="map" style="height: 100vh; width: 100vw;"></div>
  </template>
  
  <script>
  import L from 'leaflet';
  import { onMounted } from 'vue';
  
  export default {
    setup() {
      onMounted(() => {
        // 初始化地图
        const map = L.map('map').setView([51.505, -0.09], 13); // 使用伦敦作为示例位置
  
        // 添加OpenStreetMap图层
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors'
        }).addTo(map);
  
        // 添加一个标记点
        const marker = L.marker([51.505, -0.09]).addTo(map);
      });
    }
  };
  </script>
  
  <style>
  #map {
    height: 100vh;
    width: 100vw;
  }
  </style>
  