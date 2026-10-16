# Alumni Tracking System - Data Design (CDD)

## Database Schema
- **Users / Graduates Table**: Stores graduate profile information.
  - `id` (Integer, Primary Key)
  - `full_name` (String)
  - `email` (String, Unique)
  - `graduation_year` (Integer)