function toggle_dark() {
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        document.body.classList.toggle("light-mode");
    } else {
        document.body.classList.toggle("dark-mode");
    }
}

function move_right(e) {
    let item = e.parentElement.parentElement;
    let list = item.parentElement;
    let parent;

    switch (list.id) {
        case "todo-box":
            parent = document.getElementById("doing-box");
            break;
        case "doing-box":
            parent = document.getElementById("done-box");
            break;
        default:
            return;
    }
    fetch(`/move/${item.id.split("-")[1]}/right`, {method: "POST"})
        .then((res) => {
            if (res.ok) {
                parent.appendChild(item);
            }
        });
}

function move_left(e) {
    let item = e.parentElement.parentElement;
    let list = item.parentElement;
    let parent;

    switch (list.id) {
        case "doing-box":
            parent = document.getElementById("todo-box");
            break;
        case "done-box":
            parent = document.getElementById("doing-box");
            break;
        default:
            return;
    }
    fetch("/move/1/left", {method: "POST"})
        .then((res) => {
            if (res.ok) {
                parent.appendChild(item);
            }
        });
}

intervals = new Set();
window.onload = () => {
    document.querySelectorAll(".item-due").forEach(element => {
        interval = setInterval(() => {
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
            console.log(distance);

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

function clear_intervals() {
    for (let id of intervals) {
        intervals.delete(id);
        clearInterval(id);
    }
}
