function haversine(lon1, lat1, lon2, lat2) {
    const R = 6371;  // 地球半径（公里）
    const dLat = radians(lat2 - lat1);
    const dLon = radians(lon2 - lon1);

    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(radians(lat1)) * Math.cos(radians(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const distance = R * c;
    return distance;
}

function radians(degrees) {
    return degrees * (Math.PI / 180);
}

// 示例坐标点
const centerLon = -73.935242;  // 示例经度
const centerLat = 40.730610;   // 示例纬度

// 城市坐标数组
const cities = [
    { name: '城市1', lat: 40.7128, lon: -74.0060 },
    { name: '城市2', lat: 34.0522, lon: -118.2437 }
    // 更多城市可以加入这个数组
];

// 半径限制（公里）
const radius = 200;

// 筛选距离小于200公里的城市
const citiesWithinRadius = cities.filter(city => {
    const distance = haversine(centerLon, centerLat, city.lon, city.lat);
    return distance <= radius;
});

// 返回结果
console.log(citiesWithinRadius);
