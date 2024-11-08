function toggle_dark() {
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        document.body.classList.toggle("light-mode");
    } else {
        document.body.classList.toggle("dark-mode");
    }
    if (document.body.classList.contains("light-mode")) {
        document.getElementById("toggle_dark").textContent = "☀️"
    } else {
        document.getElementById("toggle_dark").textContent = "🌙"
    }
}

function move(e, dir) {
    let item = e.parentElement.parentElement;

    fetch(`/move/${item.id.split("-")[1]}/${dir}`, {method: "POST"})
        .then((res) => res.text())
        .then((text) => {
            let newParent = document.getElementById(`${text}-box`)
            newParent.appendChild(item);
        });
}

function move_right(e) {
    move(e, "right")
}

function move_left(e) {
    move(e, "left")
}


intervals = new Set();

window.onload = () => {
    document.getElementById("popup").childNodes.forEach((child) => {
        child.onclick = (event) => {
            event.stopPropagation();
        };
    })

    if (window.matchMedia("(prefers-color-scheme: light)").matches) {
        document.getElementById("toggle_dark").textContent = "☀️"
    }

    add_countdown();

    let chooser = document.getElementById("choose-pfp");
    if (chooser) {
        chooser.onchange = () => {
            let preview = document.getElementById("pfp-preview");
            preview.classList.add("hidden");
            if (chooser.files.length > 1) {
                alert("Only one file should be uploaded!");
                chooser.value = "";
            } else if (chooser.files[0].size > 1048576) {
                alert("Max file size 1MB!");
                chooser.value = "";
            } else {
                preview.classList.remove("hidden");
                preview.src = URL.createObjectURL(chooser.files[0]);
                preview.onload = function() {
                    URL.revokeObjectURL(preview.src);
                }
            }
        }
    }
}

function clear_intervals() {
    for (let id of intervals) {
        intervals.delete(id);
        clearInterval(id);
    }
}

function close_popup() {
    document.getElementById('popup').classList.toggle('hidden')
}

function show_popup(id) {
    if (document.getElementById(id) == null) {
        document.getElementById('popup').classList.toggle('hidden')
        return;
    }

    for (child of document.getElementById('popup').children) {
        child.classList.add("hidden")
    }

    document.getElementById(id).classList.remove("hidden");
    document.getElementById('popup').classList.toggle('hidden')
}

function edit(id) {
    show_popup("edit-box");
    let par = document.getElementById(`item-${id}`);
    let desc = par.querySelector(".item-text").textContent;

    let date, time;
    [date, time] = par.querySelector(".item-date").textContent.split(" ");
    date = date.split("/");
    dueDate = new Date(date[2], date[1] - 1, date[0], time[0], time[1]);

    let form = document.getElementById("edit-form")
    let descInput = form.elements["description"]
    let dateInput = form.elements["date"]
    let timeInput = form.elements["time"]
    let idInput = form.elements["id"]
    descInput.value = desc;
    dateInput.valueAsDate = new Date(dueDate.getTime() - dueDate.getTimezoneOffset() * 60000);
    timeInput.value = time;
    idInput.value = id;
}

function del_item() {
    let form = document.getElementById("edit-form")
    let id = form.elements["id"].value;

    fetch(`/delete/${id}`, {method: "POST"})
        .then((res) => res.text())
        .then((text) => {
            if (text == "deleted") {
                close_popup();
                document.querySelector(`#item-${id}`).remove();
                clear_intervals();
                add_countdown();
            } else {
                alert("Failed to delete!");
            }
        });
}

function add_countdown() {
    document.querySelectorAll(".item-due").forEach(element => {
        interval = setInterval(() => {
            if (element.parentElement.parentElement.parentElement.id == "done-box") {
                element.innerHTML = "Due: Done";
                return;
            }

            let dueDate = element.dataset.date;
            if (!("date" in element.dataset)) {
                let date, time;
                [date, time] = element.parentElement.querySelector(".item-date").textContent.split(" ");
                date = date.split("/");
                time = time.split(":");
                dueDate = new Date(date[2], date[1] - 1, date[0], time[0], time[1]).getTime();
                element.dataset.date = dueDate;
            }
            let now = new Date().getTime();

            let distance = dueDate - now;
            distance = Math.floor(distance / 1000);

            let days = Math.floor(distance / (60 * 60 * 24));
            let hours = Math.floor((distance % (60 * 60 * 24)) / (60 * 60));
            let minutes = Math.floor((distance % (60 * 60)) / (60));
            let seconds = Math.floor((distance % (60)));

            element.innerHTML = "Due: "
                + (days > 0 ? days + "d " : "")
                + (hours > 0 ? hours + "h " : "")
                + (minutes > 0 ? minutes + "m " : "")
                + (seconds > 0 ? seconds + "s " : "");

            if (distance < 0) {
                element.innerHTML = "OVERDUE!!";
            }
        }, 1000);
        intervals.add(interval);
    });
}
