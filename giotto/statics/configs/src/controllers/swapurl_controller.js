// src/controllers/hello_controller.js
import { Controller } from "stimulus"

export default class extends Controller {
    static values = { name: String, frame: String }

    swap() {
        console.log("here", this.frameValue)
        var frame = document.getElementById(this.frameValue)
        frame.setAttribute("src", `/frameurl?name=${this.nameValue}`);
    };
    reset() {
        var frame = document.getElementById(this.frameValue)
        frame.setAttribute("src", "/frameurl");
    };
}