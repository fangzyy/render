from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

online_users = set()

html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>在线用户查看系统</title>
</head>
<body style="text-align:center; margin-top:50px;">
    <h1>多人在线实时系统</h1>
    <input type="text" id="username" placeholder="输入你的名字">
    <button onclick="join()">上线</button>
    <h3>当前在线人数：<span id="count">0</span></h3>
    <ul id="userList"></ul>

    <script>
        let name = "";
        async function update(){
            const res = await fetch("/list");
            const data = await res.json();
            document.getElementById("count").innerText = data.count;
            document.getElementById("userList").innerHTML = data.users.map(u=>`<li>${u}</li>`).join("");
        }
        async function join(){
            name = document.getElementById("username").value.trim();
            if(!name) return alert("请输入名字");
            await fetch("/join", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({"name":name})
            });
            update();
            setInterval(update,3000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/join', methods=['POST'])
def join():
    data = request.get_json()
    name = data.get('name','').strip()
    if name:
        online_users.add(name)
    return jsonify({"ok":True})

@app.route('/list', methods=['POST','GET'])
def user_list():
    return jsonify({
        "count":len(online_users),
        "users":list(online_users)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
