import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Subject, BehaviorSubject, Observable } from "rxjs";
import { Metadata, StatusCode } from "@app/models/app.models"


@Injectable({
  providedIn: "root"
})
/**
 * StatusService provides application status
 * and metadata from the backend webapi.
 * 
 * GET /api/status
 * 
 *  {
 *      "organisation":"Magenta",
 *      "version":"1.0.0-rc"
 *  }
 * 
 */
export class StatusService {

    private metadata$: Subject<Metadata>
    private connectionStatus$: BehaviorSubject<StatusCode>

    constructor(private http: HttpClient) {
        this.metadata$ = new Subject()
        this.connectionStatus$ = new BehaviorSubject(StatusCode.LOADING)
    }

    /**
     * Get the application metadata from the backend webapi
     * 
     * The metadata does not provide any real functionality
     * and currently consists of only 2 things:
     *   * A configurable organisation name
     *   * The application version
     *
     * @return  {Observable}  Returns an observable for Metadata objects
     */
    public getMetaData(): Observable<Metadata> {
        this.http.get("/api/status").subscribe(
            (metadata: Metadata) => {
                // Push the metadata once it's received
                this.metadata$.next(metadata)

                // Set the connection status to `SUCCESS = 3`
                this.connectionStatus$.next(StatusCode.SUCCESS)
            },
            (error: any) => {
                // The request has failed - Set status code to `ERROR = 2`
                this.connectionStatus$.next(StatusCode.ERROR)

                // Log the error
                console.log(error)
            }
        )

        return this.metadata$.asObservable()
    }

    /**
     * Get the connection status to the backend webapi.
     * 
     * The reason we are not just returning the Subject itself
     * is that we want to allow the subscriber to listen for changes
     * but NOT make any changes. 
     * 
     * We do NOT want to expose the next method!
     *
     * @return  {Observable}  Returns the connection status as an observable
     */
    public getConnectionStatus(): Observable<StatusCode> {
        return this.connectionStatus$.asObservable()
    }
}
