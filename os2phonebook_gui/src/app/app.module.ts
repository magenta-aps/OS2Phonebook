import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SearchComponent } from './components/search/search.component';
import { EmployeeComponent } from './components/employee/employee.component';
import { OrgunitComponent } from './components/orgunit/orgunit.component';
import { BrowserComponent } from './components/browser/browser.component';
import { SearchnavComponent } from './components/searchnav/searchnav.component';


@NgModule({
  declarations: [
    AppComponent,
    SearchComponent,
    EmployeeComponent,
    OrgunitComponent,
    BrowserComponent,
    SearchnavComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FontAwesomeModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
