<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LIFF 表單</title>
    <script src="https://static.line-scdn.net/liff/2.1/sdk.js"></script>
    <script>
        // 初始化 LIFF
        function initializeLiff() {
            console.log("初始化 LIFF 應用中...");

            // 替換為您的 LIFF ID
            liff.init({ liffId: "2003645883-Rn6V0a3n" })
                .then(() => {
                    console.log("LIFF 初始化成功");

                    if (!liff.isLoggedIn()) {
                        console.log("用戶未登入，執行登入流程");
                        liff.login();
                    } else {
                        console.log("用戶已經登入");
                    }
                })
                .catch(err => {
                    console.error("LIFF 初始化錯誤:", err);
                    alert("LIFF 初始化失敗，請重新嘗試。");
                });
        }

        // 提交表單
        function submitForm() {
            // 確保用戶已經登入
            if (!liff.isLoggedIn()) {
                alert("請登入以提交表單");
                return;
            }

            liff.getProfile()
                .then(profile => {
                    const userID = profile.userId;
                    const name = document.getElementById("name").value;
                    const phone = document.getElementById("phone").value;
                    const vaccineName = document.getElementById("vaccine").value;
                    const appointmentDate = document.getElementById("vaccinationDate").value;

                    // 顯示提交的資料
                    console.log("用戶資料：", { userID, name, phone, vaccineName, appointmentDate });

                    if (!name || !phone || !vaccineName || !appointmentDate) {
                        alert("請填寫所有必要的表單欄位。");
                        return;
                    }

                    // 送出資料到後端
                    fetch("https://linedadr29.hkg1.zeabur.app/submit-form", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ userID, name, phone, vaccineName, appointmentDate })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("表單提交成功", data);
                        alert("表單提交成功！");
                    })
                    .catch(error => {
                        console.error("提交失敗", error);
                        alert("提交失敗，請稍後再試。");
                    });
                })
                .catch(err => {
                    console.error("獲取用戶資料錯誤:", err);
                    alert("獲取用戶資料失敗，請重新登入。");
                });
        }

        // 初始化 LIFF 應用
        initializeLiff();
    </script>
</head>
<body>
    <h1>疫苗預約表單</h1>
    <form id="vaccineForm" method="POST">
        <label for="name">姓名：</label><br>
        <input type="text" id="name" name="name"><br><br>

        <label for="phone">電話：</label><br>
        <input type="text" id="phone" name="phone"><br><br>

        <label for="vaccine">選擇疫苗：</label><br>
        <select id="vaccine" name="vaccine">
            <option value="子宮頸疫苗">子宮頸疫苗</option>
            <option value="欣克疹疫苗">欣克疹疫苗</option>
            <option value="A肝疫苗">A肝疫苗</option>
        </select><br><br>

        <label for="vaccinationDate">接種日期：</label><br>
        <input type="date" id="vaccinationDate" name="vaccinationDate"><br><br>

        <button type="button" onclick="submitForm()">提交表單</button>
    </form>
</body>
</html>
