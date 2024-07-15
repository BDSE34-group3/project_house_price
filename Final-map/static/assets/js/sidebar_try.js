document.addEventListener('DOMContentLoaded', function() {
    
    
    
    const citySelect = document.getElementById('citySelect');
    const districtSelect = document.getElementById('districtSelect');

    
     // 當城市選擇發生變化時更新地區選項
     citySelect.addEventListener('change', function() {
        // 假設 fetchDistricts 是一個函數，根據城市從伺服器獲取地區選項
        fetchDistricts(this.value);

    });

    // 當地區選擇發生變化時，根據城市和地區更新地圖
    districtSelect.addEventListener('change', function() {
        if (this.value !== 'Choose') {
            updateMapMarkers(citySelect.value, this.value);
        }
    });

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

    function updateDistrictOptions(districts) {
        districtSelect.innerHTML = '<option value="Choose" selected>請選擇</option>';
        districts.forEach(function(district) {
            const option = document.createElement('option');
            option.value = district.value;
            option.textContent = district.text;
            districtSelect.appendChild(option);
        });
    }

    if (citySelect && districtSelect) {
        citySelect.addEventListener('change', function() {
            let districts = [];
            if (this.value === 'Taipei') {
                districts = taipeiDistricts;
            } else if (this.value === 'NewTaipei') {
                districts = newTaipeiDistricts;
            }
            updateDistrictOptions(districts);

            this.size = 1;
        });

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
        document.getElementById(popupId).style.display = 'block';
        if (popupId === 'ping-popup') {
            updatePingSliderValue('ping-slider', 'ping-slider-value');
        } else if (popupId === 'price-popup') {
            updatePriceSliderValue('price-slider', 'price-slider-value');
        }
        // const popup = document.getElementById(popupId);
        // if (popup) {
        //     popup.style.display = 'block';
        // }
    }

    function closePopup(popupId) {
        const popupElement = document.getElementById(popupId);
        popupElement.style.display = 'none';
    }


//PingSlider

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




    function updatePriceSliderValue() {
        const slider = document.getElementById('price-slider');
        const sliderValueDisplay = document.getElementById('price-slider-value');
        sliderValueDisplay.textContent = slider.value;

        const sliderWidth = slider.offsetWidth - sliderValueDisplay.offsetWidth;
        const newValue = Number((slider.value - slider.min) * sliderWidth / (slider.max - slider.min));
        const newPosition = 10 + newValue - sliderValueDisplay.offsetWidth / 2;
        sliderValueDisplay.style.left = `${newPosition}px`;
    }

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
        alert(document.getElementById('ping-slider').value);
        closePopup();
    }

    function applyPriceSlider() {
        alert('Apply clicked: ' + document.getElementById('price-slider').value);
        closePopup();
    }

    document.getElementById('total_ping').addEventListener('click', function() {
        event.preventDefault(); 
        openPopup('ping-popup');
    });

    document.getElementById('total_price').addEventListener('click', function() {
        event.preventDefault(); 
        openPopup('price-popup');
        updatePriceSliderValue('price-slider', 'price-slider-value');
    });

    const closeBtns = document.querySelectorAll('.close');
    closeBtns.forEach(btn => btn.addEventListener('click', function() {
        const popupId = btn.getAttribute('data-popup');
        closePopup(popupId);
    }));

   
    document.getElementById('price-slider').addEventListener('input', function() {
        updatePriceSliderValue('price-slider', 'price-slider-value');
    });


    //總價格按apply
    document.getElementById('price_btn_apply').addEventListener('click', function() {
        event.preventDefault(); // 阻止默認動作
        closePopup('price-popup');
    });

   //總價格按clear
    document.getElementById('price_btn_clear').addEventListener('click', function() {
        const slider = document.getElementById('price-slider');
        slider.value = 0;
        updatePriceSliderValue('price-slider', 'price-slider-value');
    });

   //總坪數按apply
    document.getElementById('ping_btn_apply').addEventListener('click', function() {
        event.preventDefault(); // 阻止默認動作
        closePopup('ping-popup');
    });

    //總坪數按clear
    document.getElementById('ping_btn_clear').addEventListener('click', function() {
        const slider = document.getElementById('ping-slider');
        slider.value = 0;
        updatePingSliderValue('ping-slider', 'ping-slider-value');
    });


//型態
    const popup = document.getElementById('type-popup');
    const openPopupBtn = document.getElementById('openPopupBtn');
    const closeBtn = document.querySelector('.popup .close');

    openPopupBtn.addEventListener('click', function() {
        // event.stopPropagation();
        popup.style.display = 'block';
    });

    closeBtn.addEventListener('click', function() {
        popup.style.display = 'none';
    });

    window.addEventListener('click', function() {
        if (event.target === popup) {
            popup.style.display = 'none';
        } else {
            event.stopPropagation(); // Prevent this click from affecting other elements
        }
    });

    document.getElementById('type_btn_clear').addEventListener('click', function() {
        document.querySelectorAll('.property-list input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
    });
    function closetypePopup(popupId) {
        document.getElementById(popupId).style.display = 'none';
    }
    document.getElementById('openPopupBtn').addEventListener('click', function(event) {
        event.preventDefault(); // 阻止默認動作
        document.getElementById('type-popup').style.display = 'block';
    });
    

    //型態按apply
    document.getElementById('type_btn_apply').addEventListener('click', function() {
        event.preventDefault(); // 阻止默認動作
        closePopup('type-popup');
    });

    //型態按clear
      document.getElementById('type_btn_clear').addEventListener('click', function() {
        const slider = document.getElementById('ping-slider');
        slider.value = 0;
        updatePingSliderValue('ping-slider', 'ping-slider-value');
    });

    
    function submitForm() {
        const form = document.getElementById('myForm');
        form.submit();
        const city = form.city.value;
        const district = form.district.value;
        const totalPing = form.document.getElementById('total_ping').value;;
        const pricePing = form.price_ping.value;
        const property_type = form.property_type.value
    
        const baseUrl = 'http://127.0.0.1:5000/submit';
        const queryParams = `?city=${encodeURIComponent(city)}&district=${encodeURIComponent(district)}&total_ping=${totalPing}&price_ping=${pricePerPing}&property_type=${property_type}`;
    
        const finalUrl = baseUrl + queryParams;
        
        // Redirect to the constructed URL
        window.location.href = finalUrl;
  
    }





    
    // Initialize map
    let map = L.map('map').setView([25.0339145, 121.5412233], 8);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);


    let layerGroup = null;
    let arrMarkers = [];

    document.querySelector('button#submitButton').addEventListener('click', function(event) {
        event.preventDefault();  // 阻止按钮默认的提交行为（如果它是表单的一部分）
        event.stopPropagation(); // 阻止事件继续传播到其他节点
        fetch('http://127.0.0.1:5000/submit', {
            method: "GET"
        }).then(function(response){
            return response.json();
        
        }).then(function(data) {
            if (layerGroup != null && map.hasLayer(layerGroup)) {
                layerGroup.clearLayers();
                map.removeLayer(layerGroup);

                layerGroup = null;
                arrMarkers = [];
            }

            let tbody = document.querySelector('table > tbody');

            tbody.innerHTML = '';

           
            for (let o of data.extracted_data) {
                let tr = document.createElement("tr");
                tr.innerHTML = `<td>${o['實際價格']}</td>
                                <td>${o['屋齡']}</td>
                                <td>${o['權狀坪數']}</td>
                                <td>${o['地址']}</td>
                                <td>${o['含車位']}</td>
                                <td>${o['longtitude']}</td>
                                <td>${o['latitude']}</td>
                                <td>${o['地址']}</td>
                                <td><img src="${o['房屋圖片']}" alt="房屋圖片" width="100"></td>`;
                document.querySelector("table").appendChild(tr);

            if (o['latitude'] && o['longitude']) {
                //建立 markers
                let marker = L.marker([o['latitude'], o['longtitude']])
                .bindPopup(`<img src="${o['房屋圖片']}" alt="房屋圖片" width="100"><br><a href="${o['地址']}" target="_blank">連結</a>`);
                // .openPopup();
                    //自訂事件
                    marker.addEventListener('click', function() {
                        console.log("Marker clicker:");
                        console.log("Data object:", o);
                    });
                    
                    arrMarkers.push(marker);
                } else {
                    console.warn("Invalid latitude or longitude for data object:", o);
                };

        }
    
                
            layerGroup = L.layerGroup(arrMarkers);

            //將 layerGroup 放到 map 當中
            layerGroup.addTo(map);
        });

    })
})