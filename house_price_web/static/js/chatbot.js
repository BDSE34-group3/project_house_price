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

// 對話區域的對話顯示區
function sendQuestion() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value;
    if (question.trim() === '') return;

    // 在對話訊息區域顯示用戶輸入
    const chatMessages = document.getElementById('chatMessages');

    // 添加使用者訊息
    const userMessage = document.createElement('div');
    userMessage.textContent = question;
    userMessage.className = 'message user-message';
    chatMessages.appendChild(userMessage);

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
        // 在對話訊息區域顯示機器人回應
        const botResponse = document.createElement('div');
        botResponse.textContent = data.response;
        botResponse.className = 'message bot-message';
        chatMessages.appendChild(botResponse);
    })
    .catch(error => console.error('Error:', error));
}