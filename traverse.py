import json


def main():
    # Specify the path to your JSON file
    file_path = "securing_assets.json"

    # Open the JSON file and load its contents into a dictionary
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Now you can access the data as a dictionary
    name = 'proton account'
    asset = data["access"][name]
    get_security(name, asset, 0, data)


def get_security(name, asset, n, data):
    if asset['type'] in ['one', 'all']:
        sub_securities = []
        print(f"{n * '  '}{name} - {asset['type']}:")
        for factor, sub_asset in asset['factors'].items():
            sub_security = get_security(factor, sub_asset, n + 1, data)
            sub_securities.append(sub_security)
        if asset['type'] == 'one':
            sub_security = min(sub_securities)
            print(f"{n * '  '}{sub_security * 100:.2f} %")
            return sub_security
        if asset['type'] == 'all':
            prod = 1
            for sub_security in sub_securities:
                prod *= 1 - sub_security
            sub_security = 1 - prod
            print(f"{n * '  '}{sub_security * 100:.2f} %")
            return sub_security

    if asset['type'] == 'access':
        sub_asset = data[asset['type']][asset['name']]
        if sub_asset == {}:
            print(f"{n * '  '}{asset['type']}: {asset['name']} - ?")
            return 1
        sub_security = get_security(asset['name'], sub_asset, n, data)
        return sub_security

    if asset['type'] == 'knowledge':
        complexity = data[asset['type']][asset['name']]['complexity']
        usage = data[asset['type']][asset['name']]['usage']
        sub_security = (1 - 1 / complexity) * (1 - 1 / usage)
        print(f"{n * '  '}{asset['type']}: {asset['name']} - {sub_security * 100:.2f} %")
        return sub_security

    if asset['type'] == 'possesion':
        secrecy = data[asset['type']][asset['name']]['secrecy']
        location = data[asset['type']][asset['name']]['location']
        physical = data['physical protection'][location]['unknown']
        sub_security = (1 - 1 / secrecy) * (1 - 1 / physical)
        print(f"{n * '  '}{asset['type']}: {asset['name']} - {sub_security * 100:.2f} %")
        return sub_security

    if asset['type'] == 'biometric':
        sub_security = 1 - 1 / data[asset['type']][asset['name']]['unknown']
        print(f"{n * '  '}{asset['type']}: {asset['name']} - {sub_security * 100:.2f} %")
        return sub_security
    print(asset['type'], '?')
    return 0


if __name__ == "__main__":
    main()
