import { Input, Component } from "@angular/core"
import { faChevronDown, faChevronRight, faCircle as faCircleSolid } from "@fortawesome/free-solid-svg-icons"
import { faCircle } from "@fortawesome/free-regular-svg-icons"
import { Router } from "@angular/router"
import { TreeOrgUnit } from "@app/models/app.models"


@Component({
  selector: "app-browser",
  templateUrl: "./browser.component.html"
})
/**
 * The BrowserComponent is a tree-like browser (displayed on the right)
 * which lists all the available `ROOT` org units.
 * 
 * If one of the org units is selected,
 * the main view will change to display the selected org unit details, 
 * and the browser will expanded to display the children (if there any).
 */
export class BrowserComponent {
    /**
     * This is an angular `Input` property
     * It is used to pass in data from a parent component.
     * 
     * This input accepts an Array of org unit objects
     * which will recursively displayed as tree elements.
     *
     * @param   {Array<TreeOrgUnit>}  nodes  Array of TreeOrgUnits
     *      For more information on TreeOrgUnit, please
     *      review the TreeOrgUnit interface from the `app.models` module.
     */
    @Input("nodes") nodes: Array<TreeOrgUnit>

    // Font awesome icons
    private right = faChevronRight
    private down = faChevronDown
    private circle = faCircle
    private circleSolid = faCircleSolid

    // The identifier (uuid) of the currently selected org unit
    private identifier: string

    // Current org unit selected node (will be highlighted in the DOM)
    private selectedNode: TreeOrgUnit;

    constructor(private router: Router) { }

    /**
     * Go to the selected org unit
     *
     * @return  {void}  Call the underlying router method
     */
    private goTo(): void {
        this.router.navigate(["/orgunit", this.identifier]);
    }

    /**
     * Navigate to the previously selected parent org unit
     * and set the currently selected Node to undefined
     *
     * (Meaning: before selecting this recursive parent)
     *
     * @return  {Void}  Navigate to the previous view and destory this component
     */
    private remove(): void {
        this.goTo()
        this.selectedNode = undefined
    }

    /**
     * Expand current org unit and to its children
     * 
     * This will change the browser view
     * to displayed the expanded org unit on top of the tree
     * with proper hightlighting to emphasize that it is selected.
     *
     * @param   {TreeOrgUnit}  node  A node is a single TreeOrgUnit item
     *
     * @return  {void}  Calls the underlying router method to change views.
     */
    private expandIt(node: TreeOrgUnit): void {

        // Currently selected (and hightlighted) org unit
        this.selectedNode = node;

        /**
         * Set the `identifier` property to the identifier of the expanded node
         * This facilities easier navigation when deselecting a previously
         * selected org unit in the tree browser.
         */
        this.identifier = node.uuid

        /**
         * The TreeOrgUnit itself has an `expanded` property.
         * We'll need this in the next version of the application
         * in order to traverse through the tree of org units
         * in order to hightlight the currently expanded units.
         */
        node.expanded = true

        // Change view
        this.goTo();
    }
}
