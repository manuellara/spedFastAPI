## Overview

This project intended to: 
* Take in a CSV file from SEIS
  * Entered
  * Exited 
* Clean up the SEIS CSV file
  * Convert data types
  * Filter out inconsistent data
* Compare SEIS data to what's currently in Aeries CSE table
  * Compare each ID's value (Aeries vs SEIS)
* Output a merged CSV file for upload into Aeries with all the changes
* Output a change log (dropped IDs and updated values)

## TODOs

* [ ] Get CSV files from SEIS
  * [x] Entered
  * [x] Exited
* [ ] Read in SEIS files as dataframes
  * [x] Entered 
  * [ ] Exited 
* [x] Filter SEIS District IDs so they are all consistent 
  * [x] Remove blanks
  * [x] Remove non numeric 
* [x] Convert SEIS District ID to integer 
* [x] Convert SEIS Disability Code 1 and Disability Code 2 to integer
* [x] Get list of SEIS District IDs 
* [x] Initialize Aeries CSE dataframe
* [x] Query SQL Server to get Aeries data
  * [x] Get SQL Server connection variables
  * [x] Create SQL statement
  * [x] Execute SQL query
    * [x] Save results for Aeries CSE table in dataframe
* [x] Convert Aeries CSE table date fields to a readable format
* [x] Export Aeries CSE dataframe to CSV **Aeries output.csv** as a snapshot
* [x] Open the attribute mapping JSON file
* [ ] Iterate over Aeries dataframe IDs
  * [ ] Iterate over every mapped attribute 
    * [ ] Check if conversion is needed for the attribute
      * [ ] If yes, process replace value function with conversion
        * [x] School Type
        * [x] Percent IN Regular Class
        * [x] Case Manager
        * [x] Plan Type  (Edu Plan for SpEd Svcs)
      * [x] If no, process regular replace value function
* [x] Export Aeries dataframe as CSV **merged.csv** as the snapshot with changes
* [x] Compare original snapshot CSV against the snapshot with changes CSV
  * [x] Export change log to **compare_data.json**
  * [ ] Set up some analytics on the change log
* [x] Add SQLAlchemy (replace pyODBC)


## Mapping

| SEIS                                                                     | Aeries                  | Mapping Required? | Completed |
| ------------------------------------------------------------------------ | ----------------------- | ----------------- | --------- |
| SEIS ID                                                                  | CSE.SEI                 |                   |           |
| Last Name                                                                |                         |                   |           |
| FirstName                                                                |                         |                   |           |
| Student SSID                                                             | CSE.ID (map to STU.CID) |                   |           |
| Date of Birth                                                            |                         |                   |           |
| District ID                                                              | CSE.ID                  |                   |           |
| Disability 1 Code                                                        | CSE.DI                  |                   |           |
| Disability 1                                                             |                         |                   |           |
| Disability 2 Code                                                        | CSE.DI2                 |                   |           |
| Disability 2                                                             |                         |                   |           |
| Disability 3 Code                                                        | CSE.DI3                 |                   |           |
| Disability 3                                                             |                         |                   |           |
| Student Eligibility Status                                               |                         |                   |           |
| Date of Original SpEd Entry                                              | CSE.ED                  |                   |           |
| Date of Exit from SpEd                                                   | CSE.XD                  |                   |           |
| Exit Reason                                                              | CSE.XR                  |                   |           |
| School CDS Code                                                          | CSE.SS                  |                   |           |
| School of Attendance                                                     |                         |                   |           |
| District of SPED Accountability CDS Code                                 | CSE.DS & CSE.DR         |                   |           |
| School of Residence CDS Code                                             |                         |                   |           |
| School of Residence                                                      |                         |                   |           |
| Case Manager                                                             | CSE.SI                  | True              | Done      |
| Case Manager Email                                                       |                         |                   |           |
| Percent IN Regular Class                                                 | CSE.IRC                 | True              | Done      |
| School Type (Attendance School)                                          | CSE.TY                  | True              | Done      |
| SELPA                                                                    | CSE.SE                  |                   |           |
| Plan Type (Edu Plan for SpEd Svcs)                                       | CSE.PT                  | True              | Done      | 
| Graduation Plan Code                                                     | CSE.GP                  |                   |           |
| Program Setting Code (Ages 0-2)                                          | CSE.FI                  |                   |           |
| Preschool Program Setting (3-5 year-old Preschool and 4 year-old TK/Kgn) | CSE.FP                  |                   |           |
| Program Setting (TK/Kgn or greater, ages 5-22)                           | CSE.FS                  |                   |           |
| Date of Next Annual Plan Review                                          | CSE.AD                  |                   |           |
| Date of Initial Referral                                                 | CSE.RD                  |                   |           |
| Referred By                                                              | CSE.RB                  | True              |           |
| Date of Initial Parent Consent                                           | CSE.PC                  |                   |           |
| Date of Infant Initial Referral                                          | CSE.IRD                 |                   |           |
| Infant Refer By                                                          | CSE.IRB                 |                   |           |
| Date of Infant Parent Consent                                            | CSE.IPC                 |                   |           |
| Date of Initial Evaluation                                               | CSE.IE                  |                   |           |
| Meeting Delay Code                                                       | CSE.EDL                 |                   |           |
| Date of Infant Initial Evaluation                                        | CSE.IIE                 |                   |           |
| Special Transportation                                                   | CSE.ST                  | True              |           |
| Primary Residence                                                        | CSE.RS                  | True              |           |
| Early Intervention Services                                              | CSE.EI                  | True              |           |
| SBAC Participation Code in ELA                                           | CSE.PA2                 |                   |           |
| SBAC Participation Description in ELA                                    |                         |                   |           |
| SBAC Participation Code in Math                                          | CSE.PA3                 |                   |           |
| SBAC Participation Description in Math                                   |                         |                   |           |
| SBAC Participation Code in Science                                       | CSE.PA4                 |                   |           |
| SBAC Participation Description in Science                                |                         |                   |           |


## Utility scripts

### Count changes in compare file

```python
import json

jsonFile = open('compare_data.json')
data = json.load(jsonFile)

print( len(data['changed']) )
```


## Local Development

Use the Makefile or Taskfile included


## Resources

[Containerizing FastAPI application](https://www.youtube.com/watch?v=2a5414BsYqw&list=LL&index=4&ab_channel=incompetent_ian )


[Adding file uploads to FastAPI application](https://www.youtube.com/watch?v=N6bpBkwFdc8&list=LL&index=7&t=241s&ab_channel=FastAPIChannel)