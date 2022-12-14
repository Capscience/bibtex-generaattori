*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Go To Main Page And Check Title
    Go To Main Page
    Main Page Should Be Open

Go To Send Page And Check Title
    Go To Send Page
    Select From List By Value  name:type  InCollection
    Click Button  submit
    Send Page Should Be Open

Go To Send Page And Send InCollection Reference
    Go To Send Page
    Select From List By Value  name:type  InCollection
    Click Button  submit
    Send InCollection Reference  Mikael Agricola  Abckiria  1543
    Main Page Should Be Open
    Page Should Contain  Mikael Agricola
    Page Should Contain  Abckiria
    Page Should Contain  1543
    Delete Reference

Delete Reference
    Go To Send Page
    Select From List By Value  name:type  InCollection
    Click Button  submit
    Send InCollection Reference  Mika Waltari  Sinuhe Egyptiläinen  1945
    Delete Reference
    Page Should Not Contain  Mika Waltari
    Page Should Not Contain  Sinuhe Egyptiläinen
    Page Should Not Contain  1945
