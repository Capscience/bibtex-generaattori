*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Import Reference From DOI
    Go To Doi Page
    Send Doi  10.1037/0000168-000
    Click Button  submit
    Main Page Should Be Open
    Page Should Contain  Lynne M. Jackson
    Page Should Contain  The psychology of prejudice: From attitudes to social action (2nd ed.).
    Page Should Contain  2020
    Delete Reference
