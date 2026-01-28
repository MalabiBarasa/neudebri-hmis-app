# 💼 PRACTICAL REFERENCE: Staff Integration Commands & Procedures

## 🎯 QUICK COMMAND REFERENCE

### **Access Django Admin**
```
URL: https://neudebri-hmis-app.onrender.com/admin/
Username: admin
Password: admin1234
```

---

## 📋 STEP-BY-STEP PROCEDURES

### **PROCEDURE 1: Add Single Doctor**

```
STEP 1: Open Django Admin
└─ Go to: /admin/

STEP 2: Navigate to Users
└─ Click: "Users" in left sidebar

STEP 3: Click "Add User"
└─ Button: "+ Add User" (top right)

STEP 4: Fill User Form
├─ Username:           dr_kipchoge
├─ Password:           SecurePassword123!
├─ Password confirm:   SecurePassword123!
└─ [Save and continue editing]

STEP 5: Complete User Profile (Optional)
├─ Email:              kipchoge@hospital.com
├─ First name:         Samuel
├─ Last name:          Kipchoge
├─ Staff status:       Check if admin
├─ Superuser status:   Only if system admin
└─ [Save]

STEP 6: Navigate to UserProfiles
└─ Click: "UserProfiles" in left sidebar

STEP 7: Click "Add UserProfile"
└─ Button: "+ Add UserProfile" (top right)

STEP 8: Fill UserProfile Form
├─ User:               dr_kipchoge (dropdown)
├─ Department:         Internal Medicine (dropdown)
├─ Role:               doctor (dropdown)
├─ Employee ID:        DOC001 (must be unique)
├─ Phone:              0701234567
├─ Specialization:     Internal Medicine
├─ License Number:     LIC/MOH/2024/001
├─ Date Joined:        (auto-filled today)
└─ [Save]

STEP 9: Verification
├─ Doctor receives credentials
├─ Doctor logs in at: /accounts/login/
├─ Username: dr_kipchoge
├─ Password: SecurePassword123!
└─ Doctor sees dashboard ✓

RESULT: Doctor can now:
├─ View patient list
├─ Create appointments
├─ Request lab tests
├─ Write prescriptions
└─ Record vital signs
```

---

### **PROCEDURE 2: Add Multiple Nurses (Batch)**

```
STEP 1: Prepare Nurses List
├─ Nurse 1: Grace Kipchoge (nurse_grace)
├─ Nurse 2: Faith Ochieng (nurse_faith)
├─ Nurse 3: Hope Kamau (nurse_hope)
└─ Nurse 4: Love Mwangi (nurse_love)

STEP 2: Create Script File
├─ File name: add_nurses.py
├─ Location: /workspaces/codespaces-django/
└─ Content: (See below)

STEP 3: Prepare Script
```

**Create file: `/workspaces/codespaces-django/add_nurses.py`**

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from django.contrib.auth.models import User
from hello_world.core.models import UserProfile, Department

# Get the nursing department
nursing_dept = Department.objects.get(name='General Ward')

# List of nurses to add
nurses = [
    {
        'username': 'nurse_grace',
        'email': 'grace@hospital.com',
        'password': 'NursePass123!',
        'first_name': 'Grace',
        'last_name': 'Kipchoge',
        'employee_id': 'NUR101',
        'phone': '0701111111',
    },
    {
        'username': 'nurse_faith',
        'email': 'faith@hospital.com',
        'password': 'NursePass456!',
        'first_name': 'Faith',
        'last_name': 'Ochieng',
        'employee_id': 'NUR102',
        'phone': '0702222222',
    },
    {
        'username': 'nurse_hope',
        'email': 'hope@hospital.com',
        'password': 'NursePass789!',
        'first_name': 'Hope',
        'last_name': 'Kamau',
        'employee_id': 'NUR103',
        'phone': '0703333333',
    },
    {
        'username': 'nurse_love',
        'email': 'love@hospital.com',
        'password': 'NursePass012!',
        'first_name': 'Love',
        'last_name': 'Mwangi',
        'employee_id': 'NUR104',
        'phone': '0704444444',
    },
]

print("Adding nurses...")
for nurse_data in nurses:
    # Create user
    user, created = User.objects.get_or_create(
        username=nurse_data['username'],
        defaults={
            'email': nurse_data['email'],
            'first_name': nurse_data['first_name'],
            'last_name': nurse_data['last_name'],
        }
    )
    
    if created:
        user.set_password(nurse_data['password'])
        user.save()
        print(f"✅ User created: {nurse_data['first_name']} {nurse_data['last_name']}")
    else:
        print(f"⚠️  User already exists: {nurse_data['username']}")
        continue
    
    # Create profile
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'department': nursing_dept,
            'role': 'nurse',
            'employee_id': nurse_data['employee_id'],
            'phone': nurse_data['phone'],
        }
    )
    
    if created:
        print(f"✅ Profile created: {nurse_data['employee_id']}")
    else:
        print(f"⚠️  Profile already exists: {nurse_data['username']}")

print("\n✅ All nurses added successfully!")
print("\nNurses can now login at: https://neudebri-hmis-app.onrender.com/accounts/login/")
```

```
STEP 4: Run Script
├─ Terminal command: cd /workspaces/codespaces-django
├─ Terminal command: source .venv/bin/activate
├─ Terminal command: python add_nurses.py
└─ Watch output for confirmation

STEP 5: Verification
├─ Go to Django Admin → Users
├─ Verify all 4 nurses created
├─ Go to UserProfiles
├─ Verify all 4 profiles created
└─ All should show role="nurse"

RESULT: All 4 nurses can now login!
```

---

### **PROCEDURE 3: Assign Pharmacist to Pharmacy Department**

```
STEP 1: Go to Django Admin
├─ URL: /admin/

STEP 2: Go to Users
├─ Click: Users

STEP 3: Search for Pharmacist
├─ Use browser search (Ctrl+F)
├─ Find: "pharmacist_peter"

STEP 4: Go to UserProfile
├─ Click: pharmacist_peter
├─ Scroll down
├─ Click: UserProfile (link at bottom)

STEP 5: Check Current Assignment
├─ Current Department: (shows current)
├─ Current Role: pharmacist

STEP 6: Verify Correct Assignment
├─ Department should be: Pharmacy
├─ Role should be: pharmacist
├─ If different, change and save

STEP 7: Verify Next Login
├─ Pharmacist logs in
├─ Should see Pharmacy features
├─ Should NOT see Doctor features
```

---

### **PROCEDURE 4: Change Staff Department/Role**

```
Example: Promote Nurse to Supervisor

STEP 1: Go to Django Admin
└─ URL: /admin/

STEP 2: Go to UserProfiles
├─ Click: "UserProfiles"

STEP 3: Find the Nurse
├─ Search or scroll
├─ Click on nurse's profile

STEP 4: Change Role
├─ Role field: Currently "nurse"
├─ Click dropdown
├─ Select: "hr_manager" (or other role)

STEP 5: Save Changes
├─ Click: [Save]

STEP 6: Test
├─ Nurse logs out
├─ Nurse logs in again
├─ Should see NEW features/permissions
└─ Should NOT see old permissions
```

---

### **PROCEDURE 5: Disable Staff Member (They Leave)**

```
Example: Dr. Kipchoge is leaving

STEP 1: Go to Django Admin
└─ URL: /admin/

STEP 2: Go to Users
├─ Click: "Users"

STEP 3: Find Staff Member
├─ Search or scroll
├─ Click: "dr_kipchoge"

STEP 4: Deactivate
├─ Find: "Active" checkbox
├─ Uncheck it (remove checkmark)
├─ This is CRITICAL - makes them inactive

STEP 5: Save
├─ Click: [Save]

STEP 6: Verify
├─ They try to login
├─ System says: "Invalid credentials"
├─ But their data STAYS in system ✓
├─ Audit trail PRESERVED ✓
└─ Records NOT deleted ✓

IMPORTANT: Never delete users!
Use deactivate instead!
```

---

### **PROCEDURE 6: Reset Staff Password (Forgot Password)**

```
METHOD 1: Staff Resets Themselves
├─ Go to: /accounts/login/
├─ Click: "Forgot Password"
├─ Enter email
├─ Check email for reset link
├─ Click reset link
├─ Create new password
└─ Done!

METHOD 2: Admin Resets
├─ Go to: /admin/auth/user/
├─ Find: username
├─ Click: Change password link (right side)
├─ Enter new password
├─ Click: Save
└─ Give new password to staff

BETTER: Method 1 (staff resets own)
FALLBACK: Method 2 (admin resets)
```

---

## 🔐 EXAMPLE CREDENTIALS SETUP

### **Doctor Setup**
```
USERNAME:       dr_kipchoge
PASSWORD:       (give temporary: Temp@2024)
EMAIL:          kipchoge@neudebri.org
DEPARTMENT:     Internal Medicine
ROLE:           doctor
EMPLOYEE ID:    DOC001
LICENSE:        LIC/MOH/2024/001
PHONE:          +254 701 234 567

First Login:
1. Go to: /accounts/login/
2. Username: dr_kipchoge
3. Password: Temp@2024
4. System says: Change password
5. Doctor creates new password
6. Done! Can now use system
```

### **Nurse Setup**
```
USERNAME:       nurse_joyce
PASSWORD:       (give temporary: Temp@2024)
EMAIL:          joyce@neudebri.org
DEPARTMENT:     General Ward
ROLE:           nurse
EMPLOYEE ID:    NUR002
PHONE:          +254 712 345 678

First Login:
1. Go to: /accounts/login/
2. Username: nurse_joyce
3. Password: Temp@2024
4. System says: Change password
5. Nurse creates new password
6. Done! Can now use system
```

### **Pharmacist Setup**
```
USERNAME:       pharmacist_peter
PASSWORD:       (give temporary: Temp@2024)
EMAIL:          peter@neudebri.org
DEPARTMENT:     Pharmacy
ROLE:           pharmacist
EMPLOYEE ID:    PHARM003
PHONE:          +254 723 456 789

First Login:
1. Go to: /accounts/login/
2. Username: pharmacist_peter
3. Password: Temp@2024
4. System says: Change password
5. Pharmacist creates new password
6. Done! Can now use system
```

---

## 📊 TRACKING STAFF ADDITIONS

### **Keep a Log File: `staff_register.txt`**

```
DATE    | NAME              | USERNAME        | ROLE       | DEPT        | STATUS
--------|-------------------|-----------------|------------|-------------|----------
28-Jan  | Dr. Samuel K.     | dr_kipchoge     | doctor     | Surgery     | Active
28-Jan  | Nurse Joyce       | nurse_joyce     | nurse      | General     | Active
28-Jan  | Peter Omondi      | pharmacist_peter| pharmacist | Pharmacy    | Active
28-Jan  | Grace Kipchoge    | nurse_grace     | nurse      | General     | Active
28-Jan  | Mary Njeri        | dr_mary_njeri   | doctor     | Obs/Gyn     | Active
```

---

## ✅ VERIFICATION CHECKLIST: After Adding Staff

```
For Each New Staff Member:

□ User exists in Django Admin → Users
□ UserProfile exists in Django Admin → UserProfiles
□ Username is unique (no duplicates)
□ Password is set and secure
□ Email is filled in
□ Department is assigned
□ Role is assigned
□ Employee ID is unique
□ Phone number is filled in
□ "Active" checkbox is CHECKED
□ First/Last name are filled in

Testing:

□ Staff can log in with username
□ Staff can log in with password
□ Dashboard loads without errors
□ Sees appropriate features for their role
□ Cannot see features they shouldn't
□ Can create/edit patient records (if allowed by role)
□ Can navigate all allowed views
□ Can logout and login again
```

---

## 🆘 COMMON ISSUES & FIXES

### **Issue: "No UserProfile matches the given query" (404 Error)**

```
Cause: UserProfile not created

Fix:
1. Go to: Django Admin → UserProfiles
2. Click: [+ Add UserProfile]
3. Select: The user
4. Assign: Department & Role
5. Click: Save
6. Staff logs in again
7. Dashboard now works!
```

### **Issue: "User can login but no dashboard features"**

```
Cause: Role not set correctly

Fix:
1. Go to: Django Admin → UserProfiles
2. Find: The user
3. Check: Role field (must be specific)
4. Verify: Not blank
5. Click: Save
6. Staff logs out & in again
7. Features now visible!
```

### **Issue: "Username taken" when adding**

```
Cause: User with that username already exists

Fix:
1. Use different username (add number/suffix)
2. Example: dr_kipchoge2
3. Or: dr_kipchoge_sr
4. Make sure unique
5. Then save
```

### **Issue: "Can't find Django Admin"**

```
Solution:
1. URL: https://neudebri-hmis-app.onrender.com/admin/
2. Login: admin / admin1234
3. If not working:
   - Check login credentials
   - Verify admin account exists
   - Try clearing browser cache
   - Try different browser
```

---

## 📱 STAFF LOGIN GUIDE (To Give Them)

```
Welcome to Neudebri HMIS!

Your Login Details:
├─ URL: https://neudebri-hmis-app.onrender.com
├─ Username: [given by admin]
├─ Temporary Password: [given by admin]
└─ Change password on first login!

How to Log In:
1. Go to URL above
2. Click "Sign In"
3. Enter Username: ___________
4. Enter Password: ___________
5. Click "Sign In"

On First Login:
6. You'll be asked to change password
7. Create a STRONG password:
   - At least 8 characters
   - Mix of letters, numbers, symbols
   - Don't share with anyone
8. You're now logged in!

If You Forget Password:
1. Go to login page
2. Click "Forgot Password"
3. Enter your email
4. Check email for reset link
5. Click link
6. Create new password

Questions? Contact Admin
Email: admin@hospital.com
Phone: [admin phone]
```

---

## 🎯 SUMMARY

**To add new doctors, nurses, pharmacists, etc:**

1. **Option A (Easiest)**: Django Admin → Add User → Add UserProfile
2. **Option B (Batch)**: Create script file → Run Python script
3. **Option C (Web)**: Give signup link → Create profile manually

**Always remember:**
- ✅ Create User first
- ✅ Create UserProfile second (CRITICAL!)
- ✅ Assign role & department
- ✅ Test by logging in
- ✅ Never delete users (deactivate instead)

**You're ready to add your real hospital staff!** 🚀
