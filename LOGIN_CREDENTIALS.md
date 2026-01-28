# Login Credentials for Neudebri HMIS

## For Your Deployed Render App

### Admin Account (Full Access)
- **Username**: `admin`
- **Email**: `admin@neudebri.com`
- **Password**: `admin1234` (default - CHANGE THIS IN PRODUCTION!)
- **Role**: System Administrator
- **Access**: Dashboard, Admin Panel, All Modules

### Available Test Accounts by Role

#### 🏥 Doctors
1. **Username**: `doctor1`
   - Email: `doctor1@neudebri.com`
   - Password: `doctor1` (Django default pattern)
   - Name: James Kipchoge

2. **Username**: `doctor2`
   - Email: `doctor2@neudebri.com`
   - Password: `doctor2`
   - Name: Mary Wanjiru

3. **Username**: `doctor3`
   - Email: `doctor3@neudebri.com`
   - Password: `doctor3`
   - Name: Peter Mutunga

#### 👩‍⚕️ Nurses
1. **Username**: `nurse4`
   - Email: `nurse4@neudebri.com`
   - Password: `nurse4`
   - Name: Alice Ochieng

2. **Username**: `nurse5`
   - Email: `nurse5@neudebri.com`
   - Password: `nurse5`
   - Name: Carol Mwangi

#### 🧪 Laboratory Technician
- **Username**: `lab_tech6`
- Email: `lab_tech6@neudebri.com`
- Password: `lab_tech6`
- Name: David Kiplagat

#### 💊 Pharmacist
- **Username**: `pharmacist7`
- Email: `pharmacist7@neudebri.com`
- Password: `pharmacist7`
- Name: Ruth Kipchoge

#### 💰 Cashier
- **Username**: `cashier8`
- Email: `cashier8@neudebri.com`
- Password: `cashier8`
- Name: Rose Chepkurui

---

## How to Access Your App

### Local Development
```
URL: http://localhost:8000
Login: http://localhost:8000/accounts/login/
Admin: http://localhost:8000/admin/
```

### Deployed on Render
```
URL: https://neudebri-hmis-app.onrender.com
Login: https://neudebri-hmis-app.onrender.com/accounts/login/
Admin: https://neudebri-hmis-app.onrender.com/admin/
```

---

## Feature Access by Role

### Administrator Account
- View all dashboards
- Manage all users and departments
- Access admin panel
- All CRUD operations
- System configuration

### Doctor Account
- View patient information
- Create/manage appointments
- Create prescriptions
- View lab results
- Record vital signs
- Create outpatient visits

### Nurse Account
- Record vital signs
- View patient information
- View appointments
- Create outpatient visits

### Lab Technician Account
- View lab requests
- Manage lab tests
- Update test results

### Pharmacist Account
- View prescriptions
- Manage pharmacy inventory
- Process prescriptions

### Cashier Account
- View appointments
- Process payments
- View billing

---

## First Login Steps

1. **Go to login page**: https://neudebri-hmis-app.onrender.com/accounts/login/
2. **Enter credentials** (e.g., `admin` / `admin1234`)
3. **Click login**
4. **You'll see the Dashboard** with:
   - Welcome message
   - Quick links to modules
   - Department information

---

## Available Features to Test

### 👥 Patient Management
- View patient list
- Create new patient
- Edit patient information
- Patient medical records

### 📅 Appointments
- View all appointments
- Schedule new appointment
- Track appointment status

### 🧪 Laboratory
- Submit lab requests
- View lab results
- Track test status

### 💊 Pharmacy
- Create prescriptions
- View pharmacy inventory
- Dispense medications

### 👤 Vital Signs
- Record patient vitals
- Track BP, Temperature, Pulse
- Vital signs history

### 🏥 Outpatient Visits
- Record outpatient visits
- Track visit notes
- Visit documentation

---

## Changing Passwords

### On the App
- Login with your account
- Click your profile name (top right)
- Change password section
- Enter old and new password

### Via Admin Panel
- Login as admin
- Go to `/admin/auth/user/`
- Click user
- Set new password
- Save

---

## Important Notes for Production

⚠️ **SECURITY**: Before going live with real hospital data:

1. **Change admin password**
   ```
   Old: admin1234
   New: [Choose a strong password]
   ```

2. **Reset all test user passwords**
   - Each user should set their own password

3. **Enable HTTPS** (should be automatic on Render)

4. **Configure email notifications** (optional but recommended)

5. **Backup database regularly**

---

## Troubleshooting Login Issues

### Error: "Login Failed"
- ✅ Check username/email spelling
- ✅ Verify database is connected
- ✅ Check if migrations ran

### Error: "Page not found"
- ✅ Check URL is correct
- ✅ Verify Django is running
- ✅ Check ALLOWED_HOSTS setting

### Can't access admin panel
- ✅ Must be logged in as admin
- ✅ URL: `/admin/`
- ✅ Only admin account has access

---

## Database with Test Data

Your app comes with sample data:
- ✅ 9 user accounts (as listed above)
- ✅ 5 sample patients
- ✅ 6 appointments
- ✅ 4 insurance providers
- ✅ 8 departments
- ✅ 16 clinic units

This data is loaded in both:
- Local database (`db.sqlite3`)
- Production database (PostgreSQL on Render)

---

## Next Steps

1. ✅ Use these credentials to test the app
2. ✅ Verify all features work correctly
3. ✅ Create any additional user accounts
4. ✅ Change admin password before production use
5. ✅ Share feedback with team

**Happy testing!** 🎉
