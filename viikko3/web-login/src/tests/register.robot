*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  eetu
    Set Password  eetu1234
    Set password Confirmation  eetu1234
    Submit Credentials
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ee
    Set Password  eetu1234
    Set password Confirmation  eetu1234
    Submit Credentials
    Register Should Fail With Message  Username ee is too short

Register With Valid Username And Too Short Password
    Set Username  eetu2
    Set Password  eetu
    Set password Confirmation  eetu
    Submit Credentials
    Register Should Fail With Message  Password is too short

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Set Username  eetu2
    Set Password  eetueetu
    Set password Confirmation  eetueetu
    Submit Credentials
    Register Should Fail With Message  Password must contain at least one number

Register With Nonmatching Password And Password Confirmation
    Set Username  eetu2
    Set Password  eetu1234
    Set password Confirmation  eetu12345
    Submit Credentials
    Register Should Fail With Message  Password didn't match with the confirmation

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  eetu1234
    Set password Confirmation  eetu1234
    Submit Credentials
    Register Should Fail With Message  User with username kalle already exists

Login After Successful Registration
    Set Username  eetu3
    Set Password  eetu1234
    Set password Confirmation  eetu1234
    Submit Credentials
    Register Should Succeed
    Go to Main Page
    Click Button  Logout
    Set Username  eetu3
    Set Password  eetu1234
    Submit Login Credentials
    Login Should Succeed

Login After Failed Registration
    Set Username  eetu4
    Set Password  eetu
    Set password Confirmation  eetu
    Submit Credentials
    Register Should Fail With Message  Password is too short
    Go To Login Page
    Set Username  eetu4
    Set Password  eetu
    Submit Login Credentials
    Login Should Fail With Message  Invalid username or password

*** Keywords ***
Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Submit Credentials
    Click Button  Register

Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Submit Login Credentials
    Click Button  Login

Login Should Succeed
    Main Page Should Be Open

Login Should Fail With Message
    [Arguments]  ${message}
    Login Page Should Be Open
    Page Should Contain  ${message}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page


