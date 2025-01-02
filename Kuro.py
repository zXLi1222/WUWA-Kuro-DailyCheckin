import os
import requests
from datetime import datetime

# 鸣潮UID
ROLE_ID = os.getenv("ROLE_ID", "这里改成鸣潮UID")
# 库街区UID
USER_ID = os.getenv("USER_ID", "这里改成库街区UID")
# 签到token，可以在 POST /encourage/signIn/v2 请求头中的 token 字段找到
TOKEN = os.getenv("TOKEN", "这里改成你的Token")

# 默认为鸣潮无需修改。
GAME_ID = os.getenv("GAME_ID", "3")
SERVER_ID = os.getenv("SERVER_ID", "76402e5b20be2c39f095a152090afddc")
REQ_MONTH = datetime.now().strftime("%m")

def get_public_ip():
    response = requests.get("https://v4.ident.me/")
    return response.text.strip()

# 签到请求头
def get_game_headers(token):
    public_ip = get_public_ip()
    return {
        "Host": "api.kurobbs.com",
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-site",
        "devCode": f"{public_ip}, Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)  KuroGameBox/2.2.9",
        "source": "ios",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "token": token,
        "Origin": "https://web-static.kurobbs.com",
        "Content-Length": "83",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KuroGameBox/2.2.9",
        "Connection": "keep-alive"
    }

# 签到奖励具体内容
def get_sign_prize(game_headers, game_id, server_id, role_id, user_id):
    url = "https://api.kurobbs.com/encourage/signIn/queryRecordV2"
    data = {
        "gameId": game_id,
        "serverId": server_id,
        "roleId": role_id,
        "userId": user_id
    }
    response = requests.post(url, headers=game_headers, data=data)
    if response.status_code != 200:
        return f"请求失败，状态码: {response.status_code}, 消息: {response.text}"
    response_data = response.json()
    if response_data.get("code") != 200:
        return f"请求失败，响应代码: {response_data.get('code')}, 消息: {response_data.get('msg')}"
    data = response_data.get("data", [])
    if isinstance(data, list) and data:
        return data[0].get("goodsName", "未知奖励")
    return "数据格式不正确或数据为空"

# 鸣潮签到
def game_sign_in(game_headers, role_id, user_id, month):
    url = "https://api.kurobbs.com/encourage/signIn/v2"
    data = {
        "gameId": GAME_ID,
        "serverId": SERVER_ID,
        "roleId": role_id,
        "userId": user_id,
        "reqMonth": month
    }
    response = requests.post(url, headers=game_headers, data=data)
    if response.status_code != 200:
        return f"[错误] 签到失败，状态码: {response.status_code}, 错误信息: {response.text}"
    response_data = response.json()
    if response_data.get("code") != 200:
        return f"[失败] 签到失败，原因: {response_data.get('msg')} (代码: {response_data.get('code')})"
    try:
        prize = get_sign_prize(game_headers, GAME_ID, SERVER_ID, role_id, user_id)
        return f"[成功] 签到完成，获得奖励: {prize}"
    except ValueError as e:
        return f"[错误] 获取奖励失败: {e}"

#库街区签到
def bbs_sign_in(bbs_headers):
    url = "https://api.kurobbs.com/user/signIn"
    data = {"gameId": "2"}
    response = requests.post(url, headers=bbs_headers, data=data)
    response_data = response.json()
    if response_data.get("code") == 200:
        return "[成功] 街区签到完成"
    return f"[失败] 签到失败，原因: {response_data.get('msg')} (代码: {response_data.get('code')})"

if __name__ == "__main__":
    if not TOKEN:
        print("请设置 TOKEN 环境变量")
        exit(1)

    public_ip = get_public_ip()
    print(f"[本机IP: {public_ip}]\n")
    game_headers = get_game_headers(TOKEN)
    bbs_result = bbs_sign_in(game_headers)
    print(f"街区签到结果:\n{bbs_result}\n")
    game_result = game_sign_in(game_headers, ROLE_ID, USER_ID, REQ_MONTH)
    print(f"鸣潮签到结果:\n{game_result}\n")
