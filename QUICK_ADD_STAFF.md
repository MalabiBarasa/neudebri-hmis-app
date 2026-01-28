# ⚡ QUICK START: Adding New Staff (5 Minutes)

## 🎯 THE FASTEST WAY TO ADD A DOCTOR, NURSE, OR ADMIN

### **OPTION 1: Through Django Admin (Easiest)**

#### **STEP 1: Open Admin**
```
Go to: https://neudebri-hmis-app.onrender.com/admin/
Login: admin / admin1234
```

#### **STEP 2: Add User**
```
Click: Users (in left menu)
Click: [+ Add User] (top right)
Enter:
  Username: dr_kipchoge
  Password: YourSecurePass123!
  Confirm Password: YourSecurePass123!
Click: Save
```

#### **STEP 3: Add UserProfile**
```
Click: UserProfiles (in left menu)
Click: [+ Add UserProfile] (top right)
Select:
  User: dr_kipchoge
  Department: Internal Medicine
  Role: doctor
Enter:
  Employee ID: DOC001
  Phone: 0701234567
  License Number: LIC123456
Click: Save
```

#### **DONE!** 
```
Dr. Kipchoge can now log in:
  URL: https://neudebri-hmis-app.onrender.com/accounts/login/
  Username: dr_kipchoge
  Password: YourSecurePass123!
```

---

### **OPTION 2: Through Web Sign-Up**

#### **STEP 1: Give Sign-Up Link to Staff**
```
Send this URL to new staff:
https://neudebri-hmis-app.onrender.com/accounts/signup/
```

#### **STEP 2: Staff Registers**
```
They fill in:
  Email: doctor@hospital.com
  Username: dr_new
  Password: CreatePass123!
  Confirm: CreatePass123!
Click: Sign Up
```

#### **STEP 3: Admin Creates Profile**
```
Go to Admin:
  Django Admin → Users → Find "dr_new"
  Then: UserProfiles → Add UserProfile
  Select: dr_new
  Role: doctor
  Department: Surgery
Click: Save
```

#### **DONE!**
```
They can now log in with their credentials
```

---

### **OPTION 3: Batch Add Multiple Staff (Advanced)**

#### **Create file: add_staff.py**

```python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from django.contrib.auth.models import User
from hello_world.core.models import UserProfile, Department

staff = [
    {'username': 'dr_alice', 'email': 'alice@hospital.com', 'password': 'Pass123!', 
     'first_name': 'Alice', 'last_name': 'Kipchoge', 'role': 'doctor', 
     'department': 'Surgery', 'employee_id': 'DOC010'},
    
    {'username': 'nurse_bob', 'email': 'bob@hospital.com', 'password': 'Pass456!',
     'first_name': 'Bob', 'last_name': 'Mwangi', 'role': 'nurse',
     'department': 'ICU', 'employee_id': 'NUR011'},
]

for s in staff:
    user, _ = User.objects.get_or_create(
        username=s['username'],
        defaults={'email': s['email'], 'first_name': s['first_name'], 
                  'last_name': s['last_name']}
    )
    user.set_password(s['password'])
    user.save()
    
    dept = Department.objects.get(name=s['department'])
    UserProfile.objects.get_or_create(
        user=user,
        defaults={'department': dept, 'role': s['role'], 
                  'employee_id': s['employee_id']}
    )
    print(f"✅ {s['first_name']} {s['last_name']} added!")
```

#### **Run it:**
```bash
python add_staff.py
```

#### **DONE!**
```
Multiple staff added instantly
```

---

## 📋 USER ROLES QUICK REFERENCE

| Role | Can Do | Best For |
|------|--------|----------|
| **doctor** | See patients, diagnose, prescribe, order labs | Physicians, surgeons |
| **nurse** | Record vitals, care notes, patient monitoring | Ward nurses, clinic nurses |
| **pharmacist** | View prescriptions, dispense drugs, manage inventory | Pharmacy staff |
| **lab_tech** | Order tests, enter results, verify | Lab technicians |
| **cashier** | Create invoices, process payments | Billing staff |
| **receptionist** | Register patients, queue management | Front desk |
| **admin** | Full system access, user management | Hospital admin |
| **hr_manager** | Employee management, leave requests | HR staff |
| **radiologist** | Manage imaging requests, reports | Radiology staff |
| **accountant** | Financial management, reports | Finance staff |

---

## ✅ VERIFICATION: Can They Log In?

After adding a staff member:

1. Have them try: `https://neudebri-hmis-app.onrender.com/accounts/login/`
2. Enter username & password
3. Should see **Dashboard**
4. Should see features based on their **role**

**If they see blank page**: UserProfile wasn't created. Go back to Step 3 above.

---

## 🔑 PASSWORDS

### For Staff Members:
```
Your temp password: YourSecurePass123!

On first login:
1. Log in
2. Go to profile settings
3. Change to personal password
```

### For Admins:
```
Keep secure list of:
  - Initial passwords
  - Who has what username
  - Employee IDs
  - Department assignments
```

---

## 🚀 COMMON SCENARIOS

### Scenario 1: Hire a New Doctor

```
Admin: "Welcome Dr. Kipchoge!"
Admin: Creates account (dr_kipchoge) in Django Admin
Admin: Creates profile with role=doctor, dept=Surgery
Admin: Gives Dr. Kipchoge username & temp password
Dr. Kipchoge: Logs in, changes password
Dr. Kipchoge: Starts using system immediately
```

### Scenario 2: Hire Multiple Nurses

```
Admin: Uses batch script to add 5 nurses at once
Script: Creates all accounts and profiles automatically
Admin: Provides login credentials to all nurses
Nurses: All log in and start work same day
```

### Scenario 3: Promote Nurse to Supervisor

```
Admin: Goes to UserProfile for the nurse
Admin: Changes role from 'nurse' to 'hr_manager'
Admin: Saves
Nurse: Now has HR access on next login
```

### Scenario 4: Staff Member Leaves

```
Admin: Goes to Users → Find staff member
Admin: Unchecks "Active" checkbox
Admin: Saves
Result: They can't log in anymore (records stay)
```

---

## 📱 STAFF CAN LOGIN FROM

- **Desktop Computer**: Yes ✅
- **Laptop**: Yes ✅
- **Tablet**: Yes ✅
- **Phone**: Yes ✅
- **Remote Location**: Yes ✅

**Anywhere with internet connection!**

---

## ❓ TROUBLESHOOTING

### Can't find Users menu?
```
Go directly to: /admin/auth/user/
```

### Staff can login but no dashboard?
```
Create UserProfile for that user
(This is required!)
```

### Forgot admin password?
```
Contact Render support or reset via:
python manage.py changepassword admin
```

### Need to add 50 staff members?
```
Use Option 3 (batch script)
Much faster than manual entry
```

---

## ✨ YOU'RE READY!

**Your hospital can now:**
- ✅ Hire new doctors, nurses, staff
- ✅ Give them login credentials
- ✅ Assign them to departments
- ✅ Control what they can do by role
- ✅ Remove access when they leave
- ✅ Track everything in system

**Start adding your real staff today!**

---

## 📞 QUICK HELP

**Need to add staff?** → Use Method 1 (Admin Panel)
**Need to add 10+ staff?** → Use Method 3 (Script)
**Staff forgot password?** → They use Forgot Password on login page
**Need to remove someone?** → Uncheck "Active" (don't delete)
**Role permissions issue?** → Check UserProfile role assignment

---

**Next**: Start adding your real hospital staff and go live! 🚀
