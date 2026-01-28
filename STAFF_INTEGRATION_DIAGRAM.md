# 📊 VISUAL WORKFLOW: How Staff Integration Works in Your HMIS

## 🎯 THE BIG PICTURE

```
┌─────────────────────────────────────────────────────────────────────┐
│           NEUDEBRI HMIS - STAFF INTEGRATION WORKFLOW                 │
└─────────────────────────────────────────────────────────────────────┘

                    ┌────────────────────────┐
                    │   New Staff Arrives    │
                    │   (Doctor/Nurse/etc)   │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  Admin Creates Account  │
                    │  in Django Admin Panel  │
                    │  (Username + Password)  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │ Admin Creates Profile    │
                    │ (Role + Department)      │
                    │ THIS IS CRITICAL!        │
                    └───────────┬──────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │  Staff Gets Credentials  │
                    │  Username & Password     │
                    └───────────┬──────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │  Staff Logs In           │
                    │  https://neudebri...     │
                    └───────────┬──────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │  System Checks Role      │
                    │  Assigns Permissions     │
                    └───────────┬──────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │  Staff Sees Dashboard    │
                    │  With Allowed Features   │
                    └───────────┬──────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │  Staff Can Now:          │
                    │  - View Patients         │
                    │  - Create Records        │
                    │  - Access Assigned       │
                    │    Modules               │
                    └──────────────────────────┘
```

---

## 🔄 DETAILED FLOW: STEP BY STEP

### **PHASE 1: USER CREATION**

```
┌─────────────────────────┐
│   Django Admin Panel    │
│  /admin/auth/user/      │
└──────────┬──────────────┘
           │
    ┌──────▼──────┐
    │ Add User    │
    └──────┬──────┘
           │
    ┌──────▼──────────────────────┐
    │ Enter:                       │
    │ • Username: dr_kipchoge      │
    │ • Password: SecurePass123!   │
    │ • Email: dr@hospital.com     │
    │ • First Name: Samuel         │
    │ • Last Name: Kipchoge        │
    └──────┬──────────────────────┘
           │
    ┌──────▼──────┐
    │  Save       │
    │  ✅ User Created
    └─────────────┘
```

### **PHASE 2: PROFILE CREATION (CRITICAL!)**

```
┌──────────────────────────┐
│   Django Admin Panel     │
│  /admin/core/userprofile/│
└──────┬───────────────────┘
       │
┌──────▼──────┐
│ Add Profile │
└──────┬──────┘
       │
┌──────▼────────────────────────────┐
│ Select User:                       │
│ ┌──────────────────────────────┐  │
│ │ dr_kipchoge          ▼       │  │
│ └──────────────────────────────┘  │
│                                    │
│ Select Department:                 │
│ ┌──────────────────────────────┐  │
│ │ Internal Medicine    ▼       │  │
│ └──────────────────────────────┘  │
│                                    │
│ Select Role:                       │
│ ┌──────────────────────────────┐  │
│ │ doctor               ▼       │  │
│ └──────────────────────────────┘  │
│                                    │
│ Enter:                             │
│ • Employee ID: DOC001              │
│ • Phone: 0701234567                │
│ • Specialization: Surgery          │
│ • License Number: LIC123456        │
└──────┬──────────────────────────────┘
       │
┌──────▼──────┐
│  Save       │
│  ✅ Profile Created
└─────────────┘
```

### **PHASE 3: LOGIN & AUTHENTICATION**

```
┌─────────────────────────────┐
│   Staff Goes to Login       │
│   https://neudebri...       │
│   /accounts/login/          │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│ Enters:                      │
│ • Username: dr_kipchoge      │
│ • Password: SecurePass123!   │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────────┐
│ System Checks:                   │
│ 1. Is username correct? ✓        │
│ 2. Is password correct? ✓        │
│ 3. Is account active? ✓          │
│ 4. Does UserProfile exist? ✓     │
│ 5. What is their role? doctor    │
└──────────┬──────────────────────┘
           │
┌──────────▼──────────────────────┐
│ Session Created                  │
│ Browser Cookie Set               │
│ User Logged In                   │
└──────────┬──────────────────────┘
           │
┌──────────▼──────────────────────┐
│ Dashboard Loads                  │
│ Shows Doctor-Allowed Features    │
│ • Patient List                   │
│ • Appointments                   │
│ • Lab Requests                   │
│ • Prescriptions                  │
│ • Vital Signs                    │
└──────────────────────────────────┘
```

### **PHASE 4: USING THE SYSTEM**

```
┌──────────────────────────┐
│   Doctor Logged In       │
│   Sees Dashboard         │
└──────────┬───────────────┘
           │
    ┌──────┴────────┬───────────┬──────────┬──────────┐
    │               │           │          │          │
    ▼               ▼           ▼          ▼          ▼
┌────────┐    ┌─────────┐  ┌────────┐ ┌─────────┐ ┌──────┐
│Patient │    │Appt.    │  │Lab Req │ │Prescription│Vitals│
│List    │    │Mgmt     │  │Mgmt    │ │Creation   │Record│
└────────┘    └─────────┘  └────────┘ └─────────┘ └──────┘
    │               │           │          │          │
    └───────┬───────┴───────────┴──────────┴──────────┘
            │
    ┌───────▼──────────────┐
    │ System Checks        │
    │ User Role: doctor    │
    │ Can access? Yes ✓    │
    └───────┬──────────────┘
            │
    ┌───────▼──────────────┐
    │ Feature Loads        │
    │ Staff Works          │
    │ Data Saved           │
    └──────────────────────┘
```

---

## 🧑‍⚕️ ROLE-BASED ACCESS CONTROL (RBAC)

```
┌────────────────────────────────────────────────────────┐
│              ROLE → PERMISSIONS MAPPING                 │
└────────────────────────────────────────────────────────┘

DOCTOR
│
├─ ✅ Can View Patients
├─ ✅ Can Create Appointments
├─ ✅ Can Request Lab Tests
├─ ✅ Can Create Prescriptions
├─ ✅ Can Record Vitals
├─ ✅ Can Write Doctor Notes
├─ ❌ Cannot Manage Users
├─ ❌ Cannot Access Billing
└─ ❌ Cannot Manage Inventory

NURSE
│
├─ ✅ Can View Patients
├─ ✅ Can Record Vital Signs
├─ ✅ Can Write Nursing Notes
├─ ✅ Can View Medical Records
├─ ✅ Can See Appointments
├─ ❌ Cannot Create Prescriptions
├─ ❌ Cannot Manage Finances
└─ ❌ Cannot Access Admin Functions

PHARMACIST
│
├─ ✅ Can View Prescriptions
├─ ✅ Can Dispense Drugs
├─ ✅ Can Track Inventory
├─ ✅ Can View Patient Records
├─ ❌ Cannot Create Prescriptions
├─ ❌ Cannot Manage Finances
└─ ❌ Cannot Access Admin Functions

ADMIN
│
├─ ✅ Full System Access
├─ ✅ Can Manage All Users
├─ ✅ Can Configure System
├─ ✅ Can View All Data
├─ ✅ Can Generate Reports
└─ ✅ Can Access Everything
```

---

## 🔐 AUTHENTICATION & SESSION FLOW

```
┌─────────────────────────────────────────────────────┐
│         AUTHENTICATION PROCESS                       │
└─────────────────────────────────────────────────────┘

Step 1: Staff Submits Credentials
├─ Username: dr_kipchoge
├─ Password: SecurePass123!
└─ Source: /accounts/login/

Step 2: Django Checks Credentials
├─ Query: User.objects.get(username=...)
├─ Check: user.password match?
├─ Result: ✅ VALID

Step 3: Check UserProfile
├─ Query: UserProfile.objects.get(user=...)
├─ Check: Profile exists?
├─ Result: ✅ EXISTS
├─ Extract: Role = "doctor"
└─ Extract: Department = "Surgery"

Step 4: Create Session
├─ Generate: Session ID
├─ Store: In database
├─ Set: Browser cookie
└─ Duration: 2 weeks (configurable)

Step 5: Redirect to Dashboard
├─ Load: /core/dashboard/
├─ Check: User logged in? ✅
├─ Check: Role? doctor
├─ Load: Doctor-specific views
└─ Display: Doctor dashboard

Step 6: Every Subsequent Request
├─ Check: Session cookie valid?
├─ Check: User logged in?
├─ Check: Is feature allowed for role?
├─ Load: Feature (if allowed)
└─ Deny: Feature (if not allowed)
```

---

## 👥 DEPARTMENT STRUCTURE

```
┌─────────────────────────────────────────┐
│         DEPARTMENTS                     │
└─────────────────────────────────────────┘

Department 1: Surgery
├─ Dr. Kipchoge (doctor) ✓
├─ Nurse Mary (nurse) ✓
├─ Nurse Joyce (nurse) ✓
└─ Surgical Tech (nurse) ✓

Department 2: Internal Medicine
├─ Dr. Ngugi (doctor) ✓
├─ Dr. Kipchoge (doctor) ✓
├─ Nurse Moses (nurse) ✓
└─ Clinical Officer (nurse) ✓

Department 3: Pharmacy
├─ Peter (pharmacist) ✓
├─ Linda (pharmacist) ✓
└─ Tech (receptionist) ✓

Department 4: Laboratory
├─ Tech 1 (lab_tech) ✓
├─ Tech 2 (lab_tech) ✓
└─ Manager (admin) ✓

Department 5: Administration
├─ Hospital Director (admin) ✓
├─ Finance Manager (accountant) ✓
└─ HR Manager (hr_manager) ✓
```

---

## 🔄 STAFF LIFECYCLE IN SYSTEM

```
┌──────────────────────────────────────────────────────┐
│          STAFF LIFECYCLE                              │
└──────────────────────────────────────────────────────┘

PHASE 1: HIRE (First Day)
├─ Create User account
├─ Create UserProfile
├─ Assign role & department
└─ Provide credentials

PHASE 2: ONBOARD (Week 1)
├─ Staff logs in
├─ Changes password
├─ Reviews dashboard
├─ Gets trained
└─ Starts using system

PHASE 3: WORK (Ongoing)
├─ Staff accesses system daily
├─ Creates patient records
├─ Views assignments
├─ System tracks activities
└─ Data stored in database

PHASE 4: MANAGE (Ongoing)
├─ Admin monitors usage
├─ Can change department
├─ Can change role
├─ Can reset password
└─ Can view activity logs

PHASE 5: LEAVE (Last Day)
├─ Admin goes to Users
├─ Unchecks "Active"
├─ Staff can't login anymore
├─ Records stay in system
└─ Audit trail preserved
```

---

## 🔄 COMMON MODIFICATIONS

```
┌─────────────────────────────────────────────────┐
│  HOW TO MAKE CHANGES AFTER STAFF IS ADDED       │
└─────────────────────────────────────────────────┘

CHANGE DEPARTMENT
1. Go to: Django Admin → Users
2. Find: dr_kipchoge → UserProfile
3. Change: Department field
4. Save
5. ✓ Done! Takes effect immediately

CHANGE ROLE
1. Go to: Django Admin → Users
2. Find: dr_kipchoge → UserProfile
3. Change: Role field (e.g., doctor → admin)
4. Save
5. ✓ Done! Staff has new permissions on next login

RESET PASSWORD
1. Go to: /accounts/ (if staff requests)
2. Click: Forgot Password
3. Enter: Email
4. Follow: Reset link in email
5. ✓ Done! They create new password

OR (Admin can reset)
1. Go to: Django Admin → Users
2. Find: dr_kipchoge
3. Click: Reset Password
4. Enter: New password
5. ✓ Done! Send new password to staff

DEACTIVATE STAFF
1. Go to: Django Admin → Users
2. Find: dr_kipchoge
3. Uncheck: Active checkbox
4. Save
5. ✓ Done! They can't login anymore

REACTIVATE STAFF
1. Go to: Django Admin → Users
2. Find: dr_kipchoge
3. Check: Active checkbox
4. Save
5. ✓ Done! They can login again
```

---

## 📱 MULTI-DEVICE ACCESS

```
Same credentials work everywhere:

DESKTOP
│
├─ Hospital Computer
│  └─ Username: dr_kipchoge
│     Password: SecurePass123!
│
├─ Doctor's Home Computer
│  └─ Username: dr_kipchoge
│     Password: SecurePass123!
│
MOBILE
│
├─ Tablet
│  └─ Username: dr_kipchoge
│     Password: SecurePass123!
│
├─ Smartphone
│  └─ Username: dr_kipchoge
│     Password: SecurePass123!

All use same credentials!
All access same patient data!
All see same medical records!
System tracks who logged in from where!
```

---

## ✅ VERIFICATION CHECKLIST

```
After adding staff member:

□ User created in Django Admin
□ UserProfile created
□ Role assigned
□ Department assigned
□ Employee ID set
□ Phone number added

Then:

□ Staff can login with username
□ Staff can login with password
□ Dashboard loads without errors
□ Appropriate features visible
□ Appropriate features hidden
□ No 404 errors on dashboard

If any ❌, check:
□ Is UserProfile created? (most common issue)
□ Is Active checkbox checked?
□ Is Department correct?
□ Is Role correct?
```

---

## 🚀 READY TO ADD STAFF!

**Your system is fully integrated and ready for:**
- ✅ Adding doctors
- ✅ Adding nurses
- ✅ Adding pharmacists
- ✅ Adding lab technicians
- ✅ Adding administrators
- ✅ Managing roles & permissions
- ✅ Handling staff changes
- ✅ Real hospital operations

**Start adding your real staff today!**
