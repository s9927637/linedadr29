function initializeLiff() {
    console.log("初始化 LIFF 應用中...");
    
    liff.init({ liffId: "2003645883-Rn6V0a3n" }) // 替換為您的 LIFF ID
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

function submitForm() {
    liff.getProfile()
        .then(profile => {
            const userID = profile.userId;
            const name = document.getElementById("name").value;
            const phone = document.getElementById("phone").value;
            const vaccineName = document.getElementById("vaccine").value;
            const appointmentDate = document.getElementById("vaccinationDate").value;

            if (!name || !phone || !vaccineName || !appointmentDate) {
                alert("請填寫所有必要的表單欄位。");
                return;
            }

            console.log("提交資料:", { userID, name, phone, vaccineName, appointmentDate });

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

initializeLiff();
