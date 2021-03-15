import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["row", "input", "total"];
    static values = { maxPageRows: Number };

    initialize() {
        this.startIndex = 0;
        this.total = this.rowTargets.length;

        this.showedRows = []; // indexes of rows showed at the page
        this.filteredInRows = []; // indexes of rows that satisfy filter
        for (var i = 0; i < this.maxPageRowsValue; i++) {
            this.showedRows.push(i)
        };

        for (var i = 0; i < this.total; i++) {
            this.filteredInRows.push(i)
        };

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
        if (this.startIndex + this.maxPageRowsValue < this.filteredInRows.length) {
            this.startIndex += this.maxPageRowsValue
            this.showCurrentPage()
        }
    };

    lastPage() {
        console.log(this.filteredInRows.length, this.maxPageRowsValue)
        this.startIndex = this.filteredInRows.length - ((this.filteredInRows.length - 1) % this.maxPageRowsValue) - 1
        this.showCurrentPage()
    }

    filter() {
        if (this.input.length != 1) {
            this.filteredInRows = [];
            this.rowTargets.forEach((element, index) => {
                var includesInput = element.innerText.toLowerCase().includes(this.input)
                if (includesInput) {
                    this.filteredInRows.push(index);
                }
            });

            this.totalTarget.innerText = this.filteredInRows.length;
            this.startIndex = 0;
            this.showCurrentPage()
        }
    }

    showCurrentPage() {
        console.log(this.showedRows)
        // hide showed rows
        this.showedRows.forEach(element => {
            this.rowTargets[element].classList.add("hidden")
        });
        this.showedRows = [];
        // unhide rows that are filtered in and fit in pagination interval
        this.filteredInRows.forEach((realIndex, index) => {
            if (index >= this.startIndex & index < this.startIndex + this.maxPageRowsValue) {
                this.rowTargets[realIndex].classList.remove("hidden")
                this.showedRows.push(realIndex)
            }
        });
    }

    get input() {
        return this.inputTarget.value.toLowerCase()
    };

    get rows() {
        return this.rowTarget.value
    };

};