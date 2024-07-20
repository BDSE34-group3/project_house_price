document.getElementById("map-link").addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("map-iframe").src = "tableau_embed.html";});

// 打開對話框
function openDialog() {
    document.getElementById('dialogBox').style.display = 'block';
}

// 隱藏對話框
function hideDialog() {
    var dialogBox = document.getElementById('dialogBox');
    dialogBox.style.display = 'none';
}
document.getElementById('hideButton').addEventListener('click', hideDialog);

function adjustInputSize(inputElement) {
    var newSize = 200 + Math.max(0, (inputElement.value.length - 20) * 10);
    inputElement.style.width = newSize + 'px';
}

// function searchQuestion() {
//     // 實現搜索功能的代碼
//     const question = document.getElementById('question').value;
//     alert('Search for: ' + question);
// }

// 對話區域的問答顯示區
function sendQuestion() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value;
    if (question.trim() === '') return;

    // 在用戶消息區域顯示用戶輸入
    const userMessages = document.getElementById('userMessages');
    const userMessage = document.createElement('div');
    userMessage.textContent = question;
    userMessage.style.textAlign = 'right';
    userMessages.appendChild(userMessage);

    // 清空輸入框
    questionInput.value = '';

    // 發送AJAX請求到伺服器
    fetch('/map', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        // 在機器人回應區域顯示回應
        const botResponses = document.getElementById('botResponses');
        const botResponse = document.createElement('div');
        botResponse.textContent = data.response;
        botResponse.style.textAlign = 'left';
        botResponses.appendChild(botResponse);
    })
    .catch(error => console.error('Error:', error));
}


// 讓側邊欄不會隨頁面滑動而移動
// function adjustLayout() {
// 	var sidebar = document.getElementById('sidebar');
// 	var sidebarWidth = sidebar.offsetWidth; // 獲取側邊欄當前寬度
// 	var mainContent = document.getElementById('content'); // 確保此 ID 與您主要內容容器匹配

// 	if (mainContent) {
// 		mainContent.style.marginLeft = sidebarWidth + 'px'; // 調整主內容的左邊距
// 	}
// }

// 調整側邊欄和內容的位置
// window.addEventListener('resize', adjustLayout);
// document.addEventListener('DOMContentLoaded', adjustLayout);

// window.addEventListener('resize', adjustLayout);
// document.addEventListener('DOMContentLoaded', adjustLayout);