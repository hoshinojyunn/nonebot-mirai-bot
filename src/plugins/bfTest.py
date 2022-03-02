import requests


def getWeaponData():
    try:
        all_data: dict
        weapon_data: list
        message = ''
        name = input("输入查询姓名")
        r = requests.get(url="https://api.gametools.network/bf1/weapons/",
                         params={"format_values": "true", "name": name, "platform": "pc", "lang": "en-us"})
        r.raise_for_status()
        all_data = r.json()
        userName = all_data.get("userName")
        # weapons为一个列表
        weapon_data = all_data["weapons"]
        print(type(weapon_data))
        # weapons内元素均为字典
        data = sorted(weapon_data, key=lambda i: i['kills'], reverse=True)
        print("你的名字是:", userName)
        print("你的前十名武器:")
        for i in range(0, 10):
            message += str(i + 1) + "." + data[i].get('weaponName') + ":" + str(data[i].get('kills')) + "\n"
        print(message)
    except:
        print("name wrong")


if __name__ == "__main__":
    getWeaponData()
