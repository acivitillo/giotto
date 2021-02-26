import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["row"];

    hide() {
        this.rowTargets.forEach(element => {
            element.classList.add("invisible")
        });
    };

    unhide() {
        this.rowTargets.forEach(element => {
            element.classList.remove("invisible")
        });
    };


    get rows() {
        return this.rowTarget.value
    };
};