import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["row"];

    hide() {
        this.rowTargets.forEach(element => {
            element.classList.add("hidden")
        });
    };

    unhide() {
        this.rowTargets.forEach(element => {
            element.classList.remove("hidden")
        });
    };


    get rows() {
        return this.rowTarget.value
    };
};