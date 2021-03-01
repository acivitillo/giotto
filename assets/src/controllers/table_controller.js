import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["row"];
    static values = { maxPageRows: Number };

    initialize() {
        this.startIndex = 0;
        this.showCurrentPage()
    };

    firstPage() {
        this.initialize()
    }

    previousPage() {
        if (this.startIndex - this.maxPageRowsValue >= 0) {
            this.startIndex -= this.maxPageRowsValue
            this.showCurrentPage()
        }
    };

    nextPage() {
        if (this.startIndex + this.maxPageRowsValue < this.rowTargets.length) {
            this.startIndex += this.maxPageRowsValue
            this.showCurrentPage()
        }
    };

    lastPage() {
        this.startIndex = this.rowTargets.length - ((this.rowTargets.length - 1) % this.maxPageRowsValue) - 1
        this.showCurrentPage()
    }

    showCurrentPage() {
        this.rowTargets.forEach((element, index) => {
            if (index >= this.startIndex & index < this.startIndex + this.maxPageRowsValue) {
                element.classList.remove("hidden")
            } else {
                element.classList.add("hidden")
            }
        });
    }


    get rows() {
        return this.rowTarget.value
    };

};