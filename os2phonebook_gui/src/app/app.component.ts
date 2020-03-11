import { Component, OnInit } from "@angular/core"
import { Router } from "@angular/router"
import { OrgUnitService } from "@app/services/org-unit/org-unit.service"
import { StatusService } from "@app/services/status/status.service"
import { Metadata, StatusCode, TreeOrgUnit } from "@app/models/app.models"
import { Observable } from "rxjs"
import { faSpinner, faTimes } from "@fortawesome/free-solid-svg-icons"
import { Meta } from '@angular/platform-browser'


@Component({
  selector: "app-root",
  templateUrl: "./app.component.html"
})
export class AppComponent implements OnInit {

    // Fontawesome icons
    private spinner = faSpinner
    private error = faTimes

    // Backend Webapi status
    private statusCode: StatusCode

    // Navigation metadata
    private metadata: Metadata

    // Organisation Unit tree
    private organisationUnits$: Observable<TreeOrgUnit[]>

    constructor(
        private router: Router,
        private service: OrgUnitService,
        private status: StatusService
    ) {}

    /**
     * Go Home!
     * Navigate back to the `Home` view.
     *
     * See the `app-routing.module` for current routings
     *
     * @return {Void}
     */
    private goHome(): void {
        this.router.navigate(["/"])
    }

    ngOnInit(): void {

        // Listen for connection status changes
        this.status.getConnectionStatus().subscribe(
            (statusCode: StatusCode) => {
                this.statusCode = statusCode
            }
        )

        // Set the metadata (e.g. organisation name and application version)
        this.status.getMetaData().subscribe(
            (metadata: Metadata) => {
                this.metadata = metadata
            }
        )

        // Get all org units as an observable
        this.organisationUnits$ = this.service.getOrgUnits()
    }
}
