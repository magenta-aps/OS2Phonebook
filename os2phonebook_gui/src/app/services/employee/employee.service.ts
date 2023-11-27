import { Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { EmployeeDetails } from "@app/models/app.models"
import { Observable } from 'rxjs'


@Injectable({
    providedIn: "root"
})
/**
 * The EmployeeService facilitates communication
 * with the backend webapi for fetching employee data.
 * 
 * Actually this is the ONLY thing this services does right now...
 */
export class EmployeeService {

    constructor(private http: HttpClient) { }

    /**
     * Fetch employee with details
     * 
     * Call HTTP GET on `/api/employee/<uuid>` with identifier (uuid)
     * in order to receive an employee object with details. 
     *
     * @param   {string}  uuid  The identifier (uuid) of the employee
     *
     * @return  {Observable<object>}  Returns a HTTP response object with employee data.
     */
    public getEmployee(uuid: string): Observable<object> {
        return this.http.get(`/api/employee/${uuid}`)
    }
}
