# PART 1: STATIC AND DYNAMIC TESTING

## 1.1 Overview
This part involved performing static and dynamic testing on the Mobile Food Delivery App in an Agile/Scrum environment. The aim was to identify code issues early, improve code quality, and ensure all major components are functionally reliable before deployment.

## 1.2 Static Testing

### 1. Manual Code Review
We reviewed the following files:
- `main.py`
- `Order_Placement.py`
- `Payment_Processing.py`
- `Restaurant_Browsing.py`
- `User_Registration.py`

### 2. Findings Summary

| Issue                        | Description                                              | Priority | Suggestion                                      |
|------------------------------|----------------------------------------------------------|----------|-------------------------------------------------|
| Plaintext password storage   | Password saved as-is in users.json.                      | High     | Use bcrypt for password hashing.               |
| Quantity input not validated | In AddItemPopup, `int(qty_entry.get())` may raise `ValueError`. | High     | Use try-except and validate positive integers. |
| No JSONDecodeError handling  | `load_users()` doesn’t handle mal-formed JSON file.      | Medium   | Add try-except for `json.JSONDecodeError`.     |
| Unnecessary class dependencies | `PaymentMethod` used instead of the already imported `PaymentProcessing`. | Low | Use consistent class for clarity. |

### 3. Automated Static Analysis
**Tools Used:**
- Pylint

**Sample Output Summary:**
