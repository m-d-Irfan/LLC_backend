# LLC Backend - Language Learning API

The backend for the Language Learning Center (LLC) platform, focused on providing a streamlined experience for students to access courses, take quizzes, and manage payments.

## 🚀 Features
- **Student Management:** Custom user models tailored for learners.
- **Course System:** Comprehensive course materials and curriculum management.
- **Enrollment:** Seamless student-to-course registration.
- **Quiz System:** Integrated assessments and automated grading.
- **Payment Integration:** Secure transaction handling for course access.
- **Certificates:** Automated PDF certificate generation upon completion.

## 🛠️ Tech Stack
- **Framework:** Django & Django REST Framework (DRF)
- **Database:** PostgreSQL (Production) / SQLite (Development)
- **Authentication:** JWT (JSON Web Tokens)
- **Deployment:** Render

## 📁 Project Structure
```text
├── llc/            # Core project settings
├── user/           # Student authentication & profiles
├── course/         # Course content management
├── enrollment/     # Registration logic
├── quiz/           # Assessments
├── payment/        # Transactions
└── certificate/    # PDF Generation
