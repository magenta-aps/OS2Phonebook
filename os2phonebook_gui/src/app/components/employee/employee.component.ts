import { Component, OnInit, OnDestroy } from "@angular/core"
import { Router, ActivatedRoute, ParamMap } from "@angular/router"
import { Observable, Subscription } from "rxjs"
import { EmployeeService } from "@app/services/employee/employee.service"
import { faAt, faMapMarked, faMobileAlt, faBarcode, faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons"
import { EmployeeDetails } from "@app/models/app.models"


@Component({
  selector: "app-employee",
  templateUrl: "./employee.component.html"
})
/**
 * The EmployeeComponent is a view component
 * displaying the details of an employee in the main view area.
 * 
 */
export class EmployeeComponent implements OnInit, OnDestroy {

    // Fontawesome Icons
    private faAtIcon = faAt
    private faMapMarkedIcon = faMapMarked
    private faMobileAltIcon = faMobileAlt
    private faBarcodeIcon = faBarcode
    private faExternalLinkAltIcon = faExternalLinkAlt

    // Subscription to the route param changes
    private subscription$: Subscription

    // Currently loaded employee with details
    private employee: EmployeeDetails

    constructor(private router: Router, private route: ActivatedRoute, private service: EmployeeService) { }

    /**
     * Navigate to the org unit view
     *
     * @private
     * @param   {string}  uuid  The identifier (uuid) of the org unit
     *
     * @return  {void}  Calls the underlying router method to change view. 
     */
    private navigateToOrgunit(uuid: string): void {
        this.router.navigate(["/orgunit", uuid])
    }

    ngOnInit(): void {
        /**
         * Listen for changes in the active route params.
         * 
         * If the current `uuid` changes,
         * load the corresponding employee from the backend webapi.
         */
        this.subscription$ = this.route.paramMap.subscribe(
            (event: ParamMap) => {
                
                // Fetch current `uuid` from the active route
                let uuid: string = event.get("uuid")

                this.service.getEmployee(uuid).subscribe(
                    (response: EmployeeDetails) => {
                        this.employee = response
                    }
                )
            }
        )
    }

    ngOnDestroy(): void {
        /**
         * Unsubscribe from the route changes
         * if this component is removed from the DOM. 
         */
        this.subscription$.unsubscribe()
    }

}
