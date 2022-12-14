*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0.1 seconds
${HOME URL}  http://${SERVER}
${SEND URL}  http://${SERVER}/type

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}

Go To Main Page
    Go To  ${HOME URL}

Go To Send Page
    Go To  ${SEND URL}

Main Page Should Be Open
    Title Should Be  Bibtex generaattori

Send Page Should Be Open
    Title Should Be  Tallenna viite

Send InCollection Reference
    [Arguments]  ${AUTHOR}  ${TITLE}  ${YEAR}
    Input Text  name=author  ${AUTHOR}
    Input Text  name=title  ${TITLE}
    Input Text  name=year  ${YEAR}
    Click Button  submit

Send Book Reference
    [Arguments]  ${AUTHOR}  ${TITLE}  ${BOOK_TITLE}  ${YEAR}  ${PAGES}
    Input Text  name=author  ${AUTHOR}
    Input Text  name=title  ${TITLE}
    Input Text  name=booktitle  ${BOOK_TITLE}
    Input Text  name=year  ${YEAR}
    Input Text  name=pages  ${PAGES}
    Press Keys   xpath=//body  \ue00f
    Click Element  name:submit

Delete Reference
    Click Button  name:delete
    Click Button  name:confirm-delete

Select Reference
    [Arguments]  ${ID}
    Select Checkbox  id:chkbox-${ID}

Download References
    Go To Main Page
    Click Button  download-all
    File Should Exist  ./references.bib

Download Selected References
    Go To Main Page
    Click Button  download-selected
    File Should Exist  ./references.bib
