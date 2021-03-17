// src/controllers/hello_controller.js
import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["levelone", "leveltwo"];

    unhide() {
        if (this.leveloneTarget.classList.contains("border-b-2")) {
            this.leveloneTarget.classList.remove("border-b-2")
            this.leveloneTarget.classList.add("border-r-4")
            this.leveloneTarget.classList.add("hover:bg-cgrey_200")
        } else {
            this.leveloneTarget.classList.remove("hover:bg-cgrey_200")
            this.leveloneTarget.classList.remove("border-r-4")
            this.leveloneTarget.classList.add("border-b-2")
        }
        this.leveltwoTargets.forEach(element => {
            if (element.classList.contains("hidden")) {
                element.classList.remove("hidden")
            } else {
                element.classList.add("hidden")
            }
        });
        var el = document.getElementsByClassName("selected")
        if (el[0] != undefined) {
            el[0].classList.add("hidden")
            el[0].classList.remove("selected")
        }
    };
}