import { Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { BehaviorSubject, Observable } from "rxjs"
import { OrgUnit, TreeOrgUnit } from "@app/models/app.models"


@Injectable({
  providedIn: "root"
})
/**
 * The OrgUnitService facilites communication
 * with the backend webapi in order to fetch organisation unit data
 * and make it accessible through subscribable subjects.
 */
export class OrgUnitService {

    // This subject with hold an array of `formatted` org units
    private orgUnits$: BehaviorSubject<TreeOrgUnit[]>

    constructor(private http: HttpClient) {
        // Init subject
        this.orgUnits$ = new BehaviorSubject<TreeOrgUnit[]>([])
    }

    /**
     * Get all org units
     * 
     * Query the `/api/org_units` service endpoint
     * to receive a full list of organisation units.
     *
     * @return  {Observable}  Returns a recursive tree of org units.
     */
    public getOrgUnits() {
        this.http.get("/api/org_units")
            .subscribe((response: Array<OrgUnit>) => {
                let treeData: TreeOrgUnit[] = this.buildTree(response)
                this.orgUnits$.next(treeData)
            })

        return this.orgUnits$.asObservable()
    }

    /**
     * Get a single org unit with details
     * 
     * Query the `/api/org_unit/<uuid>` service endpoint
     * for a single org unit by identifier (uuid).
     *
     * @param   {string}  uuid  The internal identifier (uuid) of the org unit.
     *
     * @return  {Observable<object>}  Returns a HTTP response object.
     */
    public getOrgUnit(uuid: string): Observable<object> {
        return this.http.get(`/api/org_unit/${uuid}`)
    }

    /**
     * Build a recursive tree of org units
     * 
     * Creates a hashmap of TreeOrgUnits (formatted org unit items)
     * with parent children relationships.
     * 
     * Example:
     * 
     * $ROOT: {
     *     name: "Main Unit",
     *     children: [
     *         {
     *             name: "Sub Unit",
     *             children: [
     *                 {
     *                     name: "Sub unit of sub unit",
     *                     children: [   ]
     *                 }
     *             ]
     *         }
     *     ]
     * }
     *
     * @private
     * @param   {Array<OrgUnit>} data  Response data: list of org units received.
     *
     * @return  {Array<TreeOrgUnit>}}  Returns an array of (formatted) TreeOrgUnits.
     */
    private buildTree(data: Array<OrgUnit>): Array<TreeOrgUnit> {
        // Declare hash map with structure
        let hashMap: {[key: string]: TreeOrgUnit} = {}

        // Iterate over the array of received org units
        for (let unit of data) {

            // (Re)format org units
            let treeUnit: TreeOrgUnit = {
                name: unit.name,
                parent: unit.parent,
                uuid: unit.uuid,
                expanded: false,
                selected: false,
                children: []
            }

            // Add the re-formatted unit to the hashmap
            hashMap[unit.uuid] = treeUnit
        }

        /**
         * For each TreeOrgUnit who does NOT have a parent...
         * Append the TreeOrgUnit to its parent unit childrens array.
         */
        Object.values(hashMap)
            .filter((unit: TreeOrgUnit) => unit.parent != null)
            .forEach((unit: TreeOrgUnit) => {
                hashMap[unit.parent].children.push(unit)
            })

        /**
         * Return only the `ROOT` org units (which do NOT have parents).
         * These will include all the other org units as `children`.
         */
        return Object.values(hashMap)
            .filter((unit: TreeOrgUnit) => unit.parent == null)
    }
}
