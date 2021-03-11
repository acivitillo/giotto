import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["row", "input", "total"];
    static values = { maxPageRows: Number };

    initialize() {
        this.startIndex = 0;
        this.rowTargets.forEach(element => { element.filteredIn = true });
        this.showCurrentPage()
    };

    firstPage() {
        this.startIndex = 0;
        this.showCurrentPage()
    }

    previousPage() {
        if (this.startIndex - this.maxPageRowsValue >= 0) {
            this.startIndex -= this.maxPageRowsValue
            this.showCurrentPage()
        }
    };

    nextPage() {
        if (this.startIndex + this.maxPageRowsValue < this.filteredInIndexes.length) {
            this.startIndex += this.maxPageRowsValue
            this.showCurrentPage()
        }
    };

    lastPage() {
        this.startIndex = this.filteredInIndexes.length - ((this.filteredInIndexes.length - 1) % this.maxPageRowsValue) - 1
        this.showCurrentPage()
    }

    filter() {
        this.rowTargets.forEach(element => {
            var includesInput = element.innerText.toLowerCase().includes(this.input)
            if (!includesInput) {
                element.filteredIn = false;
            } else {
                element.filteredIn = true;
            }
        });
        this.totalTarget.innerText = this.filteredInIndexes.length
        this.startIndex = 0;
        this.showCurrentPage()
    }

    showCurrentPage() {
        // hide all rows
        this.rowTargets.forEach(element => {
            element.classList.add("hidden")
        });
        // unhide rows that are filtered in and fit in pagination interval
        this.filteredInIndexes.forEach((realIndex, index) => {
            if (index >= this.startIndex & index < this.startIndex + this.maxPageRowsValue) {
                this.rowTargets[realIndex].classList.remove("hidden")
            }
        });
    }

    get input() {
        return this.inputTarget.value.toLowerCase()
    };

    get rows() {
        return this.rowTarget.value
    };

    get filteredInIndexes() {
        var indexes = [];
        var i;
        for (i = 0; i < this.rowTargets.length; i++) {
            if (this.rowTargets[i].filteredIn) {
                indexes.push(i)
            }
        }
        return indexes
    }

};