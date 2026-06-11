## 🏗️ System Architecture Blueprint

Below is the live architectural mapping of the framework's multi-layered execution engine, illustrating the decoupling of the configuration layer, the multi-lane validation components, and the automated visual documentation pipeline.

```mermaid
graph TD
    %% Core Styling
    classDef engine fill:#1f2937,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef layers fill:#111827,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef storage fill:#374151,stroke:#f59e0b,stroke-width:2px,color:#fff;
    
    %% Test Runner Configuration Layer
    subgraph Core_Configuration_Layer ["Core Configuration Layer (conftest.py)"]
        A[Pytest Engine] -->|Function Scope Isolation| B[WebDriver Manager]
        B -->|Injects Headless / Window Preferences| C[Chrome Driver Session]
    end
    
    %% Test Execution Suite Layer
    subgraph Test_Execution_Suite ["Test Execution & Automation Suite"]
        C --> D1[test_login.py / test_auth.py]
        C --> D2[test_portfolio.py / test_boundary.py]
        C --> D3[test_security.py / test_dashboard.py]
        C --> D4[test_claims.py]
    end

    %% Internal Framework Verification Layers
    subgraph Multi_Layer_Validation_Engine ["Multi-Layer Validation Engine"]
        %% UI Resiliency
        D1 --> E1[Asynchronous Resiliency Layer]
        E1 -->|Polling Loops| F1[WebDriverWait + Expected Conditions]
        F1 -->|Asserts| G1[Dynamic DOM State]
        
        %% Data Integrity
        D2 --> E2[Data Integrity Layer]
        E2 -->|BVA Input Sanitization| F2[Automated Whitespace Trimming]
        E2 -->|Math Precision| F3[Floating-Point Text Array Sorting]
        
        %% Hybrid API
        D3 --> E3[Hybrid API / Network Layer]
        E3 -->|DOM Scraper| F4[Extract Asset Image / Link Source URLs]
        F4 -->|Programmatic Intercept| F5[Python Requests Library]
        F5 -->|Background Network Ping| G5[Assert 200 OK Status Codes]
        
        %% Environmental
        D3 --> E4[Environmental Scaling Layer]
        E4 -->|Viewport Resize| F6[Mobile Breakpoint Scaling 375x667]
        E4 -->|Window Handles| F7[Cross-Tab Secure Domain Switching]
    end

    %% Documentation and Reporting Pipeline
    subgraph Automated_Reporting_Pipeline ["Automated Reporting Pipeline"]
        D4 --> H[Post-Test Lifecycle Hook]
        G1 --> H
        G5 --> H
        F2 --> H
        
        H -->|Capture Static Browser Viewstate| I[driver.save_screenshot]
        I -->|Sanitize Filename / Strip Timestamps| J[Structured /screenshots Directory]
    end

    %% Apply Component CSS Styling
    class A,B,C engine;
    class D1,D2,D3,D4,E1,E2,E3,E4,F1,F2,F3,F4,F5,F6,F7,G1,G5 layers;
    class H,I,J storage;