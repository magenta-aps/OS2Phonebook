import { Input, Component } from "@angular/core"
import { Router } from "@angular/router"

import { faArrowAltCircleRight } from "@fortawesome/free-regular-svg-icons"

@Component({
  selector: "app-searchnav",
  templateUrl: "./searchnav.component.html"
})
/**
 * The SearchnavComponent is a widget
 * displaying an underlined title and a `BACK` button to return to the main view.
 * 
 * This is currently used as a header element in the EmployeeComponent and the OrgUnitComponent.
 */
export class SearchnavComponent {

    // Font awesome icon
    private back = faArrowAltCircleRight

    /**
     * This is an angular `Input` property
     * It is used to pass in data from a parent component.
     * 
     * In this case the component diplays a title:
     * 
     *  <h3 class="title">{{ title }}</h3>
     * 
     * The title is passed in via the org unit view or the employee view.
     */
    @Input() title: string;

    constructor(private router: Router) { }

    /**
     * This navigates back to the search view
     *
     * @return  {Void}  Call the underlying router service
     */
    private goToSearch(): void {
        this.router.navigate(["/"])
    }
}
