import { Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { BehaviorSubject, Observable } from "rxjs"
import { SearchRequest } from "@app/models/app.models"


@Injectable({
  providedIn: "root"
})
/**
 * SearchService provides methods perform search queries in the backend webapi
 */
export class SearchService {

    // Observables
    private searchResults$: BehaviorSubject<any[]>
    private search_type$: BehaviorSubject<string>

    constructor(private http: HttpClient) {
        // Init Subjects
        this.searchResults$ = new BehaviorSubject<any[]>([]);
        this.search_type$ = new BehaviorSubject<string>("employee_by_name")
    }

    /**
     * Current search type (state)
     * Defaults to `employee_by_name`
     * 
     * We are persisting the state of the selected search type
     * outside the components displaying the value.
     * This prevents the displayed value from resetting
     * everytime the view changes.
     * 
     * @return  {Observable}  Returns the selected search type as an observable.
     */
    public getSearchType(): Observable<string> {
        return this.search_type$.asObservable()
    }

    /**
     * Sets a new search type value.
     * 
     * The `BehaviorSubject` is not directly exposed to the consumers
     * of this service.
     * As such this method provides the means to change the current
     * value. 
     *
     * @param   {string}  value  Search type, e.g. `employee_by_name`
     *
     * @return  {Void}  Sets the new search type (on the subject).
     */
    public setSearchType(value: string): void {
        this.search_type$.next(value)
    }

    /**
     * Current search results (as an array of results)
     * 
     * Consumers may subscribe to this observable
     * to asynchronously receive new search results
     * as searches are performed in the backend webapi.
     * 
     * By persisting the current search results on this service class,
     * we allow the components to fetch the current results
     * without having to perform the query once more
     * which is preferable when changing views.
     *
     * @return  {Observable}  Returns the current search results as an observable.
     */
    public getSearchResults() {
        return this.searchResults$.asObservable()
    }

    /**
     * Perform a search in the backend webapi
     *
     * @param   {string}  search_type   Search type, e.g. `employee_by_name`
     * @param   {string}  search_value  Search value, e.g. `Jean Luc Picard`
     *
     * @return  {void}  Perform a search and pass the results to the `searchResults$` subject.
     */
    public search(search_type: string, search_value: string): void {

         // Construct the post data payload
         let data: SearchRequest = {
            search_type: search_type,
            search_value: search_value
        }

        // Perform a HTTP POST request
        this.http.post("/api/search", data).subscribe(

                /**
                 * If the POST request is successful,
                 * an array of search results is returned.
                 */
                (search_results: any) => {
                    this.searchResults$.next(search_results)
                },

                /**
                 * If the POST request has failed,
                 * throw an exception - a proper error handler is missing here.
                 */
                (error: any)=> {
                    throw new Error(error)
                }
            )
    }
}
