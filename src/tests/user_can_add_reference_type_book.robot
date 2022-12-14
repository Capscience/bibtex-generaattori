*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Go To Send Page And Send Book Reference
    Go To Send Page
    Select From List By Value  name:type  Book
    Click Button  submit
    Send Book Reference  Charles Bukowski  Postitoimisto  Postitoimisto  1971  100-110
    Main Page Should Be Open
    Page Should Contain  Charles Bukowski
    Page Should Contain  Postitoimisto
    Page Should Contain  1971
    Page Should Contain  100-110
    Delete Reference
