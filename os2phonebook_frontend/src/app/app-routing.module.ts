import { NgModule } from "@angular/core"
import { Routes, RouterModule } from "@angular/router"

import { SearchComponent } from "@app/components/search/search.component"
import { EmployeeComponent } from "@app/components/employee/employee.component"
import { OrgunitComponent } from "@app/components/orgunit/orgunit.component"

/**
 * Application routes
 * Defaults to the search view
 */
const routes: Routes = [
    {
        path: "",
        component: SearchComponent
    },
    {
        path: "employee/:uuid",
        component: EmployeeComponent
    },
    {
        path: "orgunit/:uuid",
        component: OrgunitComponent
    }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
