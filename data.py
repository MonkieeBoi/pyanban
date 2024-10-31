from json import dump, load, decoder


def load_data(path) -> dict:
    try:
        with open(path) as f:
            return load(f)
    except (decoder.JSONDecodeError, FileNotFoundError, IOError):
        return {"index": 0, "todo": {}, "doing": {}, "done": {}, "users": {}}


def move_item(path, item_id, left):
    data = load_data(path)
    sfrom = ""
    sto = ""
    if (item_id in data["todo"]):
        sfrom = "todo"
        sto = "todo" if left else "doing"
    elif (item_id in data["doing"]):
        sfrom = "doing"
        sto = "todo" if left else "done"
    elif (item_id in data["done"]):
        sfrom = "done"
        sto = "doing" if left else "done"

    if sfrom == sto:
        return sto

    data[sto][item_id] = data[sfrom].pop(item_id)
    save_data(path, data)
    return sto


def add_item(path, section, text, due, owner):
    data = load_data(path)
    item = {"text": text, "date": due, "owner": owner}
    data["index"] += 1
    data[section][data["index"]] = item
    save_data(path, data)


def add_user(path, username, password):
    data = load_data(path)
    if username in data["users"]:
        return
    data["users"][username] = {"password": password, "pfp": False}
    save_data(path, data)


def save_data(path, data):
    with open(path, 'w') as f:
        dump(data, f, indent=4)
