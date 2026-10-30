
// Weather Analytics Charts

function createWeatherCharts(data) {

    console.log("Analytics data:", data);
    console.log("Rainfall data:", data.rainfall);

    // 1. Average Temperature by Location
    const temperatureElement = document.getElementById("temperatureChart");

    if (temperatureElement) {
        new Chart(temperatureElement, {
            type: "bar",
            data: {
                labels: data.temperature.map(item => item.location),
                datasets: [
                    {
                        label: "Average Minimum Temperature",
                        data: data.temperature.map(item => item.min)
                    },
                    {
                        label: "Average Maximum Temperature",
                        data: data.temperature.map(item => item.max)
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // 2. Highest Rainfall Locations
    const rainfallElement = document.getElementById("rainfallChart");

    if (rainfallElement) {
        new Chart(rainfallElement, {
            type: "bar",
            data: {
                labels: data.rainfall.map(item => item.location),
                datasets: [{
                    label: "Total Rainfall (mm)",
                    data: data.rainfall.map(item => Number(item.total))
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Total Rainfall (mm)"
                        }
                    }
                }
            }
        });
    }

    // 3. Rain Today Distribution
    const rainyElement = document.getElementById("rainyChart");

    if (rainyElement) {
        new Chart(rainyElement, {
            type: "doughnut",
            data: {
                labels: data.rainy.map(item => item.label),
                datasets: [{
                    label: "Rain Today",
                    data: data.rainy.map(item => item.count)
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // 4. Average Humidity
    const humidityElement = document.getElementById("humidityChart");

    if (humidityElement) {
        new Chart(humidityElement, {
            type: "bar",
            data: {
                labels: data.humidity.map(item => item.location),
                datasets: [
                    {
                        label: "Humidity at 9 AM",
                        data: data.humidity.map(item => item.nine)
                    },
                    {
                        label: "Humidity at 3 PM",
                        data: data.humidity.map(item => item.three)
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}
