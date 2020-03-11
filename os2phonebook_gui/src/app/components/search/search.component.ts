import { Component, OnInit } from "@angular/core"
import { FormControl } from "@angular/forms"
import { Router } from "@angular/router"
import { debounceTime, distinctUntilChanged } from "rxjs/operators"
import { Observable } from "rxjs"
import { faSearch, faIdCard, faAt, faMapMarked, faMobileAlt, faSpinner } from "@fortawesome/free-solid-svg-icons"

import { SearchService } from "@app/services/search/search.service"
import { SearchType } from "@app/models/app.models"


@Component({
  selector: "app-search",
  templateUrl: "./search.component.html"
})
/**
 * The SearchComponent is a view component
 * displaying the available search types and a search bar in the main view area.
 */
export class SearchComponent implements OnInit {

    // Font awesome icons
    private search = faSearch
    private sync = faSpinner
    private idCard = faIdCard
    private phone = faMobileAlt
    private email = faAt
    private map = faMapMarked

    /**
     * Array of available search types.
     * Radio buttons will be generated accordingly via
     * the template, e.g.
     * 
     * <div class="search-types">
     *   <div *ngFor="let type of searchTypes">
     *      {{ type.name }}
     *  </div>
     * <div>
     *
     * TODO:
     * This should be replaced by a data driven approach
     * The backend must instead make the search types 
     * available via a GET endpoint
     */
    private searchTypes: Array<SearchType> = [
        {
            name: "Navn",
            type: "employee_by_name",
        },
        {
            name: "Tlf nr.",
            type: "employee_by_phone",
        },
        {
            name: "Email",
            type: "employee_by_email",
        },
        {
            name: "Stilling",
            type: "employee_by_engagement",
        },
        {
            name: "Enhed",
            type: "org_unit_by_name",
        }
    ]

    /**
     * Search input field (form)
     * The FormControl object provides a listener
     * which allows us to react to keystrokes.
     */
    private searchField = new FormControl("");

    // Current selected search type
    private selectedType: string = "employee_by_name";

    // Determine if `spinner should be visible`
    private loading: boolean = false;

    // Search results are piped via this oberservable
    private searchResults: Observable<any>;

    constructor(private router: Router, private service: SearchService) { }

    /**
     * Select a search type invokes the value to change
     * 
     * Causes the search field to reset
     * and the calls the underlying API service
     *
     * @param {string} searchtype Search type value, e.g. employee_by_name
     */
    private select(searchtype: string): void {
        // Empty the input field
        this.searchField.reset()

        // Set the new current search type
        this.service.setSearchType(searchtype)
    }

    /**
     * Navigate to either the selected org unit or employee
     *
     * @param   {string}  uuid  The identifier of the org unit or employee
     *
     * @return  {void}          Changes the view to either the org unit or employee view
     */
    private goTo(uuid: string): void {

        let url: string;

        /**
         * Set the url to either /org_unit or /employee
         * based on which is the selectedType
        */
        if (this.selectedType == "org_unit_by_name") {
            url = "/orgunit"
        } else {
            url = "/employee"
        }

        // Navigate to the corresponding view
        this.router.navigate([url, uuid])
    }

    /**
     * Perform a search request in the backed webapi.
     * For more information on this resource, 
     * please see the `/api/search` endpoint description
     * in the backend service. 
     *
     * @param   {string}  search_type   The canonical value of the search type
     * @param   {string}  search_value  Freetext search value
     *
     * @return  {Void}  Call the underlying search method
     */
    private callSearch(search_type: string, search_value: string): void {
        this.service.search(search_type, search_value)
    }

    ngOnInit() {
        // Listen to chances in the search type
        this.service.getSearchType().subscribe(
            (changedSearchType: string) => {
                this.selectedType = changedSearchType
            }
        )

        // Listen to search results - this may be triggered from a seperate component
        this.searchResults = this.service.getSearchResults()

        /**
         * Listen to changes to the input field
         * (Meaning: what the user is typing in the field)
         */
        this.searchField.valueChanges
            /**
             * If the user stops typing for 300 ms (`debouncetime in ms`)
             * evalute the input field value and whether it has changed,
             * if no changes have occured, do nothing.
             */
            .pipe(debounceTime(300), distinctUntilChanged())

            /**
             * If the user has stopped typing and the input field value has changed
             * trigger the `callSearch` method with the changed value.
             */
            .subscribe(changed_value => this.callSearch(this.selectedType, changed_value))
    }
}
