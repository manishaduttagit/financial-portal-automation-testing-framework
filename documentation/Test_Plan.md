# Test Automation Plan: Financial Portal Testing Framework

## 1. Objective & Scope
The objective of this framework is to deliver robust, scalable, multi-layered automation testing for a secure digital financial portal. It validates critical end-to-end user journeys across the Web UI, backend APIs, and the database layer to ensure data integrity and security.

* **In Scope:**
    * **Web UI Layer:** User onboarding/registration, dynamic premium calculations, document uploads, and secure session management.
    * **API Layer:** Backend endpoint verification, JSON response data validation, and security token authentication.
    * **Database Layer (Data Integrity):** Executing direct SQL queries to verify UI input matches database state changes.
* **Out of Scope:** Actual credit card/payment gateway processing clearances and external third-party credit score updates.

## 2. Automation Stack & Architecture
* **Language:** Python 3.9+
* **Framework:** Pytest (for test execution and assertions)
* **Design Pattern:** Page Object Model (POM) to ensure clean separation of UI elements and test logic.
* **Reporting:** Built-in Pytest HTML reports.

## 3. Core Test Scenarios

### Phase 1: User Onboarding & Dynamic Pricing (Web UI)
* **TC-001: New Premium Account Registration**
  * *Scenario:* A user registers for a new financial portfolio, enters personal profile data, and uploads a verification ID document.
  * *Validation:* Verify that the application accepts the file upload and advances to the "Account Pending Review" screen.
* **TC-002: Dynamic Premium/Interest Calculator Verification**
  * *Scenario:* On the investment/coverage summary page, the user adjusts their coverage deductible or investment limit slider.
  * *Validation:* Verify that the monthly premium or projected interest rate updates dynamically on the screen without a full page refresh.
* **TC-003: Validation Handling for Underage Applicants (Edge Case)**
  * *Scenario:* A user attempts to open an investment/insurance account but enters a date of birth that makes them under 18.
  * *Validation:* Verify that the UI displays the strict error message: *"Applicant must be 18 years or older to qualify."*

### Phase 2: Transaction Backend & API Validation (API Layer)
* **TC-004: Secure Financial Profile API Retrieval**
  * *Scenario:* Execute a background API `GET` request using an authenticated user token to fetch account status.
  * *Validation:* Verify the API returns a `200 OK` status code and a JSON response body confirming the account state is `"PENDING"`.
* **TC-005: API Security Token Enforcement**
  * *Scenario:* Attempt to query the backend account endpoints without passing a valid security bearer token.
  * *Validation:* Verify the system rejects the request with a `401 Unauthorized` status code to prove API security.

### Phase 3: Financial Records & Data Integrity (Database Layer)
* **TC-006: UI-to-Database Data Integrity Sync**
  * *Scenario:* Immediately after a user updates their profile address or beneficiary details on the Web UI, trigger a backend backend script.
  * *Validation:* Connect directly to the database via Python and run a SQL query (`SELECT * FROM users WHERE...`) to verify the database matches the UI input exactly.
* **TC-007: Administrative Status Approval Workflow**
  * *Scenario:* Log into the back-office manager dashboard, search for the pending account, and click "Approve Account".
  * *Validation:* Verify the UI status updates to `"ACTIVE"`.
* **TC-008: Database State Update Verification**
  * *Scenario:* Run a post-approval backend SQL query on the accounts table.
  * *Validation:* Verify the `status_code` column in the database has updated from `0` (Pending) to `1` (Active).

### Phase 4: Account Security & Session Management
* **TC-009: Secure Session Timeout/Logout Validation**
  * *Scenario:* Click the "Logout" button from the main banking/insurance dashboard and attempt to click the browser's "Back" button.
  * *Validation:* Verify that the user is securely redirected to the public login screen and cannot view cached financial information.
* **TC-010: Invalid Login Authentication Lockout**
  * *Scenario:* Attempt to log into the application using an unverified or incorrect password multiple times.
  * *Validation:* Verify the UI captures and displays a clear authorization warning: *"Invalid username or password."*