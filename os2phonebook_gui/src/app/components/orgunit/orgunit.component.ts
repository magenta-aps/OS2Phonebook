import { Component, OnInit, OnDestroy } from "@angular/core"
import { Router, ActivatedRoute, ParamMap } from "@angular/router"
import { Subscription, Observable } from "rxjs"
import { faAt, faMapMarked, faMobileAlt, faBarcode, faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons"
import { OrgUnitService } from "@app/services/org-unit/org-unit.service"
import { OrgUnitDetails } from "@app/models/app.models"


@Component({
  selector: "app-orgunit",
  templateUrl: "./orgunit.component.html"
})
/**
 * The OrgUnitComponent is a view component
 * which displays the details of an org unit in the main view area.
 */
export class OrgunitComponent implements OnInit, OnDestroy {

    // Fontawesome Icons
    private faAtIcon = faAt
    private faMapMarkedIcon = faMapMarked
    private faMobileAltIcon = faMobileAlt
    private faBarcodeIcon = faBarcode
    private faExternalLinkAltIcon = faExternalLinkAlt

    // Init subscription to route changes
    private subscription$: Subscription;

    // Currently displayed org unit
    private org_unit: OrgUnitDetails

    constructor(private router: Router, private route: ActivatedRoute, public service: OrgUnitService) {}

    /**
     * Change route to the employee view
     *
     * @param   {string}  uuid  The identifier (uuid) of the employee.
     *
     * @return  {Void}  Calls the navigate method to change the route
     */
    private goToEmployee(uuid: string): void {
        this.router.navigate(["/employee", uuid])
    }

    ngOnInit() {
        /**
         * Listen to parameter changes in the current route
         * and load the corresponding org unit.
         * 
         * The current route accepts a org unit identifier as a parameter, e.g.
         * 
         *  `/orgunit/<uuid>` or `/orgunit/535ba446-d618-4e51-8dae-821d63e26560`
         * 
         * We can listen to the `paramMap` property on the active route
         * in order to get the current identifier (uuid).
         * 
         */
        this.subscription$ = this.route.paramMap.subscribe(

            // If the identifier changes...
            (route_params: ParamMap) => {

                // Get current the current identifier (uuid)
                let uuid = route_params.get("uuid")

                // Lazy load the corresponding org unit
                this.service.getOrgUnit(uuid).subscribe(

                    /**
                     * If successful, set the response data to 
                     * to the template variable `org_unit`
                     */
                    (response: OrgUnitDetails) => {
                        this.org_unit = response
                    },

                    /**
                     * TODO: Proper error handler is missing
                     * For now an exception is thrown.
                     * 
                     * A proper way to handle this error would perhaps be
                     * to display an error component instead of the regular section.
                     */
                    (error: any) => {
                        throw new Error(error)
                    }
                )
            }
        )
    }

    ngOnDestroy () {
        // Unsubscribe to the route parameter changes
        this.subscription$.unsubscribe()
    }

}
