// src/controllers/hello_controller.js
import { Controller } from "stimulus"

export default class extends Controller {
    static values = { name: String }

    connect() {
        console.log("Hello, Stimulus!", this.element)
    };
    swap() {
        var frame = document.getElementById("frametest")
        frame.setAttribute("src", `/someurl?name=${this.nameValue}`);
    };
    reset() {
        var frame = document.getElementById("frametest")
        frame.setAttribute("src", "/someurl");
    };
}