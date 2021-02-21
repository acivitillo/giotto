// src/controllers/hello_controller.js
import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["levelone", "leveltwo"];

    unhide() {
        var bgColor = "bg-cgrey_200"
        if (this.leveloneTarget.classList.contains(bgColor)) {
            this.leveloneTarget.classList.remove("bg-cgrey_200")
        } else {
            this.leveloneTarget.classList.add("bg-cgrey_200")
        }
        this.leveltwoTargets.forEach(element => {
            if (element.classList.contains("hidden")) {
                element.classList.remove("hidden")
            } else {
                element.classList.add("hidden")
            }
        });
    };
}