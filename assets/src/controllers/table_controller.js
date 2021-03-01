import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["row"];
    static values = { entries: String };

    initialize() {
        this.rowTargets.forEach((element, index) => {
            if (index < this.entry) {
                element.classList.remove("hidden")
            } else {
                element.classList.add("hidden")
            }
        });
    };

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

    next() {
        // get first index of next rows
        var start_index = 0
        var i;
        for (i = 0; i < this.rowTargets.length; i++) {
            if (!this.rowTargets[i].classList.contains("hidden")) {
                var start_index = i + this.entry;
                break;
            }
        }

        if (start_index < this.rowTargets.length) {
            // hide previous rows and unhide next rows
            this.rowTargets.forEach((element, index) => {
                if (index >= start_index & index < start_index + this.entry) {
                    element.classList.remove("hidden")
                } else {
                    element.classList.add("hidden")
                }
            });
        }
    };

    prev() {
        // get first index of prev rows
        var start_index = 0
        var i;
        for (i = 0; i < this.rowTargets.length; i++) {
            if (!this.rowTargets[i].classList.contains("hidden")) {
                var start_index = i - this.entry;
                break;
            }
        }

        if (start_index >= 0) {
            // hide current rows and unhide prev rows
            this.rowTargets.forEach((element, index) => {
                if (index >= start_index & index < start_index + this.entry) {
                    element.classList.remove("hidden")
                } else {
                    element.classList.add("hidden")
                }
            });
        }

    };


    get rows() {
        return this.rowTarget.value
    };

    get entry() {
        return parseInt(this.entriesValue)
    };
};