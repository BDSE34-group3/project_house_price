document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('citySelect');
    const districtSelect = document.getElementById('districtSelect');
    //  // 當城市選擇發生變化時更新地區選項
    //  citySelect.addEventListener('change', function() {
    //     // 假設 fetchDistricts 是一個函數，根據城市從伺服器獲取地區選項
    //     fetchDistricts(this.value);

    // });


    const taipeiDistricts = [
        { value: "Songshan", text: "松山區" },
        { value: "Xinyi", text: "信義區" },
        { value: "Daan", text: "大安區" },
        { value: "Zhongshan", text: "中山區" },
        { value: "Zhongzheng", text: "中正區" },
        { value: "Datong", text: "大同區" },
        { value: "Wanhua", text: "萬華區" },
        { value: "Wenshan", text: "文山區" },
        { value: "Nangang", text: "南港區" },
        { value: "Neihu", text: "內湖區" },
        { value: "Shilin", text: "士林區" },
        { value: "Beitou", text: "北投區" }
    ];

    const newTaipeiDistricts = [
        { value: "Banqiao", text: "板橋區" },
        { value: "Sanchong", text: "三重區" },
        { value: "Zhonghe", text: "中和區" },
        { value: "Yonghe", text: "永和區" },
        { value: "Xinzhuang", text: "新莊區" },
        { value: "Xindian", text: "新店區" },
        { value: "Tucheng", text: "土城區" },
        { value: "Luzhou", text: "蘆洲區" },
        { value: "Shulin", text: "樹林區" },
        { value: "Tamsui", text: "淡水區" },
        { value: "Xizhi", text: "汐止區" },
        { value: "Sanxia", text: "三峽區" },
        { value: "Ruifang", text: "瑞芳區" },
        { value: "Wugu", text: "五股區" },
        { value: "Taishan", text: "泰山區" },
        { value: "Linkou", text: "林口區" },
        { value: "Shenkeng", text: "深坑區" },
        { value: "Shiding", text: "石碇區" },
        { value: "Pinglin", text: "坪林區" },
        { value: "Sanzhi", text: "三芝區" },
        { value: "Shimen", text: "石門區" },
        { value: "Bali", text: "八里區" },
        { value: "Pingxi", text: "平溪區" },
        { value: "Wanli", text: "萬里區" },
        { value: "Wulai", text: "烏來區" },
        { value: "Shuangxi", text: "雙溪區" },
        { value: "Gongliao", text: "貢寮區" },
        { value: "Jinshan", text: "金山區" },
        { value: "Yingge", text: "鶯歌區" }
    ];

    // const districtSelect = document.getElementById('districtSelect');
    function updateDistrictOptions(districts) {
        districtSelect.innerHTML = '<option value="Choose" selected>請選擇</option>';
        districts.forEach(function(district) {
            //創建一個新的 option 元素，這個元素將被添加到 districtSelect 下拉列表中。
            const option = document.createElement('option');
            //將 option 元素的 value 屬性設置為地區對象的 value。將 option 元素的 textContent 屬性設置為地區對象的 text，這將是用戶在下拉列表中看到的文本。
            option.value = district.value;
            option.textContent = district.text;
            districtSelect.appendChild(option);
        });
    }
    function fetchDistricts(city) {
        let districts = [];
        if (city === 'Taipei') {
            districts = taipeiDistricts;
        } else if (city === 'NewTaipei') {
            districts = newTaipeiDistricts;
        }
        updateDistrictOptions(districts);
    }


    if (citySelect && districtSelect) {
        citySelect.addEventListener('change', function() {
          
            fetchDistricts(this.value);
            this.size = 1;
            // updateDistrictOptions(districts);
        });
        //當地區選項發生變化時，觸發這個事件處理器。將 size 設置為 1，確保下拉列表只顯示一個選項。
        districtSelect.addEventListener('change', function() {
            this.size = 1;
        });

        
        citySelect.addEventListener('invalid', function() {
            if (this.value === 'Choose') {
                this.setCustomValidity('請選擇一個縣市');
            } else {
                this.setCustomValidity('');
            }
        });

        districtSelect.addEventListener('invalid', function() {
            if (this.value === 'Choose') {
                this.setCustomValidity('請選擇一個地區');
            } else {
                this.setCustomValidity('');
            }
        });
    }














//總坪數與總價格

function openPopup(popupId) {

    document.querySelectorAll('.popup').forEach(popup => {
        popup.style.display = 'none';
    });
    const popupElement = document.getElementById(popupId);
    popupElement.style.display = 'block';
    
    if (popupId === 'ping-popup') {
        updatePingSliderValue('ping-slider', 'ping-slider-value');
        console.log(popupId)
        
    } else if (popupId === 'price-popup') {
        updatePriceSliderValue('price-slider', 'price-slider-value');
        console.log(popupId)

    } else if (popupId === 'type-popup') {
        updateTypeSliderValue();
        console.log(popupId)
}
}


    function closePopup(popupId) {
        const popupElement = document.getElementById(popupId);
        popupElement.style.display = 'none';
    }


//總坪數Slider

    const minSlider = document.getElementById('min-range');
    const maxSlider = document.getElementById('max-range');
    const sliderTrack = document.getElementById('slider-track');
    const minValueDisplay = document.getElementById('total_ping_min');
    const maxValueDisplay = document.getElementById('total_ping_max');

    function updatePingSliderValue() {
        const min = parseFloat(minSlider.value);
        const max = parseFloat(maxSlider.value);

        if (min > max) {
            const temp = minSlider.value;
            minSlider.value = maxSlider.value;
            maxSlider.value = temp;
        }

        const minPercentage = (minSlider.value / minSlider.max) * 100;
        const maxPercentage = (maxSlider.value / maxSlider.max) * 100;

        sliderTrack.style.left = minPercentage + '%';
        sliderTrack.style.width = (maxPercentage - minPercentage) + '%';

        minValueDisplay.textContent = minSlider.value;
        maxValueDisplay.textContent = maxSlider.value;
        document.getElementById('total_ping').value = minSlider.value + '-' + maxSlider.value;
    }

    minSlider.addEventListener('input', updatePingSliderValue);
    maxSlider.addEventListener('input', updatePingSliderValue);

    // Initialize slider positions
    updatePingSliderValue();


//總價格slider
    const minSlider_price = document.getElementById('min-range');
    const maxSlider_price = document.getElementById('max-range');
    const sliderTrack_price = document.getElementById('slider-track');
    const minValueDisplay_price = document.getElementById('total_price_min');
    const maxValueDisplay_price = document.getElementById('total_price_max');

    function updatePriceSliderValue() {
        const min_price = parseFloat(minSlider_price .value);
        const max_price = parseFloat(maxSlider_price .value);

        if (min_price > max_price) {
            const temp = minSlider_price.value;
            minSlider_price.value = maxSlider_price.value;
            maxSlider_price.value = temp;
        }

        const minPercentage_price = (minSlider_price.value / minSlider_price.max) * 100;
        const maxPercentage_price = (maxSlider_price.value / maxSlider_price.max) * 100;

        sliderTrack_price.style.left = minPercentage_price + '%';
        sliderTrack_price.style.width = (maxPercentage_price - minPercentage_price) + '%';

        minValueDisplay_price.textContent = minSlider_price.value;
        maxValueDisplay_price.textContent = maxSlider_price.value;
        document.getElementById('total_price').value = minSlider_price.value + '-' + maxSlider_price.value;
    }
    minSlider_price.addEventListener('input', updatePriceSliderValue);
    maxSlider_price.addEventListener('input', updatePriceSliderValue);

    // Initialize slider positions
    updatePriceSliderValue();

    function clearPingSlider() {
        const slider = document.getElementById('ping-slider');
        slider.value = 0;
        updatePingSliderValue();
    }

    function clearPriceSlider() {
        const slider = document.getElementById('price-slider');
        slider.value = 0;
        updatePriceSliderValue();
    }

    function applyPingSlider() {
        alert(document.getElementById('ping_btn_apply').value);
        closePopup();
    }

    function applyPriceSlider() {
        alert('Apply clicked: ' + document.getElementById('price_btn_apply').value);
        closePopup();
    }

    document.getElementById('total_ping').addEventListener('click', function() {
        event.preventDefault(); 
        openPopup('ping-popup');
    });

    document.getElementById('total_price').addEventListener('click', function() {
        event.preventDefault(); 
        openPopup('price-popup');
        updatePriceSliderValue();
    });

    const closeBtns = document.querySelectorAll('.close');
    closeBtns.forEach(btn => btn.addEventListener('click', function() {
        const popupId = btn.getAttribute('data-popup');
        closePopup(popupId);
    }));

   
    document.getElementById('total_price').addEventListener('input', function() {
        updatePriceSliderValue();
    });


    //總價格按apply
    document.getElementById('price_btn_apply').addEventListener('click', function(event) {
        event.preventDefault(); // 阻止默認動作
        closePopup('price-popup');
    });

   //總價格按clear
    document.getElementById('price_btn_clear').addEventListener('click', function() {
        const slider = document.getElementById('price-slider');
        clearPriceSlider();
    });

   //總坪數按apply
    document.getElementById('ping_btn_apply').addEventListener('click', function() {
        event.preventDefault(); // 阻止默認動作
        closePopup('ping-popup');
    });

    //總坪數按clear
    document.getElementById('ping_btn_clear').addEventListener('click', function() {
        clearPingSlider();
    });


//型態
    const typePopup = document.getElementById('type-popup');
    const openTypePopupBtn = document.getElementById('property_type');
    const closeTypeBtn = typePopup.querySelector('.type-close');

    openTypePopupBtn.addEventListener('click', function() {
        event.stopPropagation();
        typePopup.style.display = 'block';
    });

    closeTypeBtn.addEventListener('click', function() {
        typePopup.style.display = 'none';
    });
    function updateTypeSliderValue() {
        const selectedType = document.querySelector('.type-container input[type="radio"]:checked');
        const typeValueDisplay = document.getElementById('type-container');
    
        if (selectedType) {
            typeValueDisplay.textContent = selectedType.nextSibling.textContent.trim();
        } else {
            typeValueDisplay.textContent = '未選擇';
        }
    }
    
    function applyPropertyType() {
        const selectedType = document.querySelector('.type-container input[type="radio"]:checked');
        if (selectedType) {
            document.getElementById('property_type').value = selectedType.value;
            // 不要在這裡觸發表單提交
        }
        closePopup('type-popup');
    }
    
    
    // 型態按apply
    document.getElementById('type_btn_apply').addEventListener('click', function() {
        event.preventDefault(); // 阻止默認動作
        applyPropertyType();
    });
    
    // 型態按clear
    document.getElementById('type_btn_clear').addEventListener('click', function() {
        document.querySelectorAll('.type-container input[type="radio"]').forEach(radio => {
            radio.checked = false;
        });
        updateTypeSliderValue(); // Clear 之後更新顯示
    });
    
    // });
    

    
    let map;
let layerGroup;

function initMap() {
    map = L.map('map').setView([25.0339145, 121.5412233], 7);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}
document.addEventListener('DOMContentLoaded', function() {
    initMap();
});
function submitForm(event) {
    event.preventDefault();
    const form = document.getElementById('myForm');
    const city = form.city.value;
    const district = form.district.value;
    const totalPing = document.getElementById('total_ping').value;
    const totalPrice = document.getElementById('total_price').value;
    const propertyType = document.querySelector('input[name="property_type"]:checked').value;
    
    const baseUrl = 'http://127.0.0.1:5000/submit';
    const queryParams = `?city=${encodeURIComponent(city)}&district=${encodeURIComponent(district)}&total_ping=${totalPing}&total_price=${totalPrice}&property_type=${propertyType}`;
    const finalUrl = baseUrl + queryParams;

    fetchDataAndUpdateMap(finalUrl);
}

function fetchDataAndUpdateMap(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.extracted_data) {
                updateMap(data);
                updateTable(data);
            }else {
                console.error('No extracted data in response');
            }
        })
        .catch(error => console.error('Error:', error));
}

function updateMap(data) {
    console.log('Updating map with data:', data);
    if (!map) {
        initMap();
    }

    if (layerGroup) {
        layerGroup.clearLayers();
        map.removeLayer(layerGroup);
    }

    let arrMarkers = [];

    for (let o of data.extracted_data) {
        if (o.latitude && o.longitude) {
            let marker = L.marker([o.latitude, o.longitude])
                .bindPopup(`<img src="${o['房屋圖片']}" alt="房屋圖片" width="100％; height:auto;"><br><a href="${o['地址']}" target="_blank">連結</a>`);
            
            marker.addEventListener('click', function() {
                console.log("Marker clicked:", o);
            });
            
            arrMarkers.push(marker);
        } else {
            console.warn("Invalid latitude or longitude for data object:", o);
        }
    }

    layerGroup = L.layerGroup(arrMarkers);
    layerGroup.addTo(map);
}

function updateTable(data) {
    let tbody = document.querySelector('table > tbody');
    tbody.innerHTML = '';
    
    for (let o of data.extracted_data) {
        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${o['售價總價']}</td>
            <td>${o['屋齡']}</td>
            <td>${o['權狀坪數']}</td>
            <td>${o['地址']}</td>
            <td>${o['含車位']}</td>
        `;
        tbody.appendChild(tr);
    }
}

// 页面加载完成后初始化地图
document.addEventListener('DOMContentLoaded', initMap);

// 添加提交按钮的事件监听器
document.querySelector('button#submit').addEventListener('click', submitForm);
    })
