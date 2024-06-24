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

// // 添加搜索邏輯
// function searchQuestion() {
// 	const question = document.getElementById('question').value;
// 	alert('You asked: ' + question);
// 	// 在此處添加搜索邏輯
// }

function adjustInputSize(inputElement) {
    var newSize = 200 + Math.max(0, (inputElement.value.length - 20) * 10);
    inputElement.style.width = newSize + 'px';
}

// function hideDialog() {
//     document.getElementById("dialogBox").style.display = 'none';
// }

function searchQuestion() {
    // 實現搜索功能的代碼
    const question = document.getElementById('question').value;
    alert('Search for: ' + question);
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