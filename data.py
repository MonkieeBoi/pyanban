from json import dump, load, decoder


def load_data(path) -> dict:
    try:
        with open(path) as f:
            return load(f)
    except (decoder.JSONDecodeError, FileNotFoundError, IOError):
        return {"index": 0, "todo": {}, "doing": {}, "done": {}, "users": {}}


def move_item(path, item_id, left):
    data = load_data(path)
    sfrom = get_section(data, item_id)
    sto = ""
    match sfrom:
        case "todo":
            sto = "todo" if left else "doing"
        case "doing":
            sto = "todo" if left else "done"
        case "done":
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


def get_item(path, item_id):
    data = load_data(path)
    section = get_section(data, item_id)
    if section is None:
        return None
    return data[section][item_id]


def get_section(data, item_id):
    if (item_id in data["todo"]):
        return "todo"
    if (item_id in data["doing"]):
        return "doing"
    if (item_id in data["done"]):
        return "done"
    return None


def edit_item(path, item_id, text, due):
    data = load_data(path)
    section = get_section(data, item_id)
    if section is None:
        return None

    data[section][item_id]["text"] = text
    data[section][item_id]["date"] = due

    save_data(path, data)


def del_item(path, item_id):
    data = load_data(path)
    section = get_section(data, item_id)
    if section is None:
        return
    data[section].pop(item_id)
    save_data(path, data)


def add_user(path, username, password, ext):
    data = load_data(path)
    if username in data["users"]:
        return
    data["users"][username] = {"password": password, "ext": ext}
    save_data(path, data)


def save_data(path, data):
    with open(path, 'w') as f:
        dump(data, f, indent=4)
