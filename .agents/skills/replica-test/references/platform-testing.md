# Platform Test Harnesses and Automation

Reference material for `replica-test`. Load this document when configuring automated
end-to-end and UI regression tests for your specific target platform.

## 1. Web Automation (Playwright)

Install test harness and browser binaries:
```bash
npm i -D @playwright/test @axe-core/playwright && npx playwright install chromium
npx playwright test
```

Best practices:
- Query elements by role and user-facing accessibility name (`getByRole('button', { name: 'Submit' })`).
- Never rely on ephemeral CSS utility classes.
- Run `@axe-core/playwright` accessibility scans on key rendered views.
- Isolate test state by seeding clean database records per test suite.

## 2. Windows Desktop Automation (FlaUI / WinApp CLI)

For WinUI 3 and WPF desktop applications:
- Use FlaUI (`FlaUI.UIA3`) or `winapp ui` test harness.
- Locate UI elements via `AutomationId` or accessibility control type.
- Run test suites locally or in Windows Sandbox for reproducible clean-state runs.

## 3. Android Mobile Automation (Jetpack Compose / ADB)

For Android applications:
- Compose UI tests using `createComposeRule()` and semantic finders (`onNodeWithText`, `onNodeWithContentDescription`).
- ADB automation via input commands (`adb shell input tap x y`, `adb shell uiautomator dump`).
- Verify edge cases: screen rotation, system dark theme toggle, network offline mode.
