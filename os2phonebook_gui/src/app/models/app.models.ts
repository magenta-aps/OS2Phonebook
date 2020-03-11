/**
 * ENUMS
 */
export enum StatusCode {
    LOADING = 1,
    SUCCESS = 2,
    ERROR = 3,
}

/**
 * INTERFACES
 */
export interface Metadata {
    organisation: string;
    version: string;
}

export interface SearchType {
    name: string;
    type: string;
}

export interface SearchRequest {
    search_type: string;
    search_value: string;
}

export interface OrgUnit {
    name: string;
    parent: string;
    uuid: string;
}

export interface TreeOrgUnit {
    name: string;
    parent: any;
    uuid: string;
    expanded: boolean;
    selected: boolean;
    children: TreeOrgUnit[]
}

export interface OrgUnitDetails {
    uuid: string;
    parent: string;
    name: string;
    addresses: Array<any>;
    engagements: Array<any>;
    management: Array<any>;
    associations: Array<any>;
}

export interface EmployeeDetails {
    uuid: string;
    givenname: string;
    name: string;
    surname: string;
    addresses: Array<any>;
    engagements: Array<any>;
    management: Array<any>;
    associations: Array<any>;
}
