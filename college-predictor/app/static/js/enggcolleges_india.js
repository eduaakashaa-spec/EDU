
// State data — total = realistic unique engg institutions (used by "all")
// TN private fixed to 540 (was 0 in v1) — these are real institutions even though TNEA also covers them.
const STATE_DATA = {
  "Andhra Pradesh":     { total: 320, iit: 1, nit: 1, tnea: 0,   deemed: 6,  private: 312, ioe: 0, nirf: 5,  naac: 2 },
  "Arunachal Pradesh":  { total: 3,   iit: 0, nit: 1, tnea: 0,   deemed: 0,  private: 2,   ioe: 0, nirf: 0,  naac: 0 },
  "Assam":              { total: 25,  iit: 1, nit: 1, tnea: 0,   deemed: 0,  private: 21,  ioe: 1, nirf: 2,  naac: 1 },
  "Bihar":              { total: 45,  iit: 1, nit: 1, tnea: 0,   deemed: 0,  private: 42,  ioe: 0, nirf: 2,  naac: 0 },
  "Chhattisgarh":       { total: 50,  iit: 1, nit: 1, tnea: 0,   deemed: 0,  private: 47,  ioe: 0, nirf: 2,  naac: 0 },
  "Delhi":              { total: 32,  iit: 1, nit: 1, tnea: 0,   deemed: 7,  private: 26,  ioe: 2, nirf: 6,  naac: 2 },
  "Goa":                { total: 7,   iit: 1, nit: 1, tnea: 0,   deemed: 0,  private: 5,   ioe: 0, nirf: 2,  naac: 1 },
  "Gujarat":            { total: 125, iit: 1, nit: 1, tnea: 0,   deemed: 3,  private: 122, ioe: 0, nirf: 4,  naac: 1 },
  "Haryana":            { total: 145, iit: 0, nit: 1, tnea: 0,   deemed: 2,  private: 142, ioe: 1, nirf: 3,  naac: 1 },
  "Himachal Pradesh":   { total: 22,  iit: 1, nit: 1, tnea: 0,   deemed: 0,  private: 19,  ioe: 0, nirf: 2,  naac: 0 },
  "Jammu and Kashmir":  { total: 17,  iit: 1, nit: 1, tnea: 0,   deemed: 0,  private: 14,  ioe: 0, nirf: 2,  naac: 0 },
  "Jharkhand":          { total: 35,  iit: 1, nit: 1, tnea: 0,   deemed: 0,  private: 32,  ioe: 0, nirf: 3,  naac: 0 },
  "Karnataka":          { total: 225, iit: 1, nit: 1, tnea: 0,   deemed: 15, private: 205, ioe: 2, nirf: 8,  naac: 5 },
  "Kerala":             { total: 155, iit: 1, nit: 1, tnea: 0,   deemed: 3,  private: 143, ioe: 0, nirf: 6,  naac: 3 },
  "Madhya Pradesh":     { total: 140, iit: 1, nit: 1, tnea: 0,   deemed: 3,  private: 134, ioe: 0, nirf: 5,  naac: 1 },
  "Maharashtra":        { total: 370, iit: 1, nit: 1, tnea: 0,   deemed: 21, private: 352, ioe: 1, nirf: 11, naac: 5 },
  "Manipur":            { total: 4,   iit: 0, nit: 1, tnea: 0,   deemed: 0,  private: 3,   ioe: 0, nirf: 0,  naac: 0 },
  "Meghalaya":          { total: 3,   iit: 0, nit: 1, tnea: 0,   deemed: 0,  private: 2,   ioe: 0, nirf: 0,  naac: 0 },
  "Mizoram":            { total: 2,   iit: 0, nit: 1, tnea: 0,   deemed: 0,  private: 1,   ioe: 0, nirf: 0,  naac: 0 },
  "Nagaland":           { total: 3,   iit: 0, nit: 1, tnea: 0,   deemed: 0,  private: 2,   ioe: 0, nirf: 0,  naac: 0 },
  "Odisha":             { total: 95,  iit: 1, nit: 1, tnea: 0,   deemed: 3,  private: 92,  ioe: 1, nirf: 4,  naac: 1 },
  "Puducherry":         { total: 10,  iit: 0, nit: 1, tnea: 0,   deemed: 0,  private: 9,   ioe: 0, nirf: 1,  naac: 0 },
  "Punjab":             { total: 110, iit: 1, nit: 1, tnea: 0,   deemed: 3,  private: 105, ioe: 0, nirf: 5,  naac: 2 },
  "Rajasthan":          { total: 135, iit: 1, nit: 1, tnea: 0,   deemed: 5,  private: 128, ioe: 1, nirf: 5,  naac: 2 },
  "Sikkim":             { total: 2,   iit: 0, nit: 1, tnea: 0,   deemed: 0,  private: 1,   ioe: 0, nirf: 0,  naac: 0 },
  "Tamil Nadu":         { total: 600, iit: 1, nit: 1, tnea: 571, deemed: 28, private: 540, ioe: 1, nirf: 13, naac: 8 },
  "Telangana":          { total: 260, iit: 1, nit: 1, tnea: 0,   deemed: 3,  private: 252, ioe: 1, nirf: 7,  naac: 2 },
  "Tripura":            { total: 3,   iit: 0, nit: 1, tnea: 0,   deemed: 0,  private: 2,   ioe: 0, nirf: 0,  naac: 0 },
  "Uttar Pradesh":      { total: 320, iit: 2, nit: 1, tnea: 0,   deemed: 7,  private: 311, ioe: 1, nirf: 9,  naac: 3 },
  "Uttarakhand":        { total: 38,  iit: 1, nit: 1, tnea: 0,   deemed: 0,  private: 36,  ioe: 0, nirf: 2,  naac: 0 },
  "West Bengal":        { total: 110, iit: 1, nit: 1, tnea: 0,   deemed: 3,  private: 102, ioe: 1, nirf: 5,  naac: 2 },
  "Ladakh":             { total: 1,   iit: 0, nit: 0, tnea: 0,   deemed: 0,  private: 1,   ioe: 0, nirf: 0,  naac: 0 },
  "Andaman and Nicobar Islands": { total: 1, iit: 0, nit: 0, tnea: 0, deemed: 0, private: 1, ioe: 0, nirf: 0, naac: 0 },
  "Chandigarh":         { total: 5,   iit: 0, nit: 0, tnea: 0,   deemed: 0,  private: 5,   ioe: 0, nirf: 1,  naac: 1 },
  "Dadra and Nagar Haveli and Daman and Diu": { total: 2, iit: 0, nit: 0, tnea: 0, deemed: 0, private: 2, ioe: 0, nirf: 0, naac: 0 }
};
for (const s in STATE_DATA) STATE_DATA[s].all = STATE_DATA[s].total;

const INSTITUTION_PINS = {
  iit: [
    { name: "IIT Madras", state: "Tamil Nadu", city: "Chennai", lat: 12.99, lng: 80.23 },
    { name: "IIT Bombay", state: "Maharashtra", city: "Mumbai", lat: 19.13, lng: 72.92 },
    { name: "IIT Delhi", state: "Delhi", city: "New Delhi", lat: 28.55, lng: 77.19 },
    { name: "IIT Kanpur", state: "Uttar Pradesh", city: "Kanpur", lat: 26.51, lng: 80.23 },
    { name: "IIT Kharagpur", state: "West Bengal", city: "Kharagpur", lat: 22.32, lng: 87.31 },
    { name: "IIT Roorkee", state: "Uttarakhand", city: "Roorkee", lat: 29.86, lng: 77.89 },
    { name: "IIT Guwahati", state: "Assam", city: "Guwahati", lat: 26.19, lng: 91.69 },
    { name: "IIT BHU Varanasi", state: "Uttar Pradesh", city: "Varanasi", lat: 25.26, lng: 82.99 },
    { name: "IIT Hyderabad", state: "Telangana", city: "Sangareddy", lat: 17.59, lng: 78.12 },
    { name: "IIT Indore", state: "Madhya Pradesh", city: "Indore", lat: 22.52, lng: 75.92 },
    { name: "IIT Bhubaneswar", state: "Odisha", city: "Bhubaneswar", lat: 20.15, lng: 85.67 },
    { name: "IIT Gandhinagar", state: "Gujarat", city: "Gandhinagar", lat: 23.21, lng: 72.68 },
    { name: "IIT Mandi", state: "Himachal Pradesh", city: "Mandi", lat: 31.71, lng: 76.99 },
    { name: "IIT Jodhpur", state: "Rajasthan", city: "Jodhpur", lat: 26.47, lng: 73.11 },
    { name: "IIT Patna", state: "Bihar", city: "Patna", lat: 25.53, lng: 84.85 },
    { name: "IIT Ropar", state: "Punjab", city: "Rupnagar", lat: 30.97, lng: 76.47 },
    { name: "IIT (ISM) Dhanbad", state: "Jharkhand", city: "Dhanbad", lat: 23.81, lng: 86.44 },
    { name: "IIT Tirupati", state: "Andhra Pradesh", city: "Tirupati", lat: 13.63, lng: 79.41 },
    { name: "IIT Palakkad", state: "Kerala", city: "Palakkad", lat: 10.79, lng: 76.65 },
    { name: "IIT Bhilai", state: "Chhattisgarh", city: "Bhilai", lat: 21.21, lng: 81.43 },
    { name: "IIT Goa", state: "Goa", city: "Ponda", lat: 15.40, lng: 74.01 },
    { name: "IIT Jammu", state: "Jammu and Kashmir", city: "Jammu", lat: 32.95, lng: 74.95 },
    { name: "IIT Dharwad", state: "Karnataka", city: "Dharwad", lat: 15.39, lng: 75.02 }
  ],
  nit: [
    { name: "NIT Trichy", state: "Tamil Nadu", city: "Tiruchirappalli", lat: 10.76, lng: 78.81 },
    { name: "NIT Surathkal", state: "Karnataka", city: "Mangalore", lat: 13.01, lng: 74.79 },
    { name: "NIT Rourkela", state: "Odisha", city: "Rourkela", lat: 22.25, lng: 84.90 },
    { name: "NIT Warangal", state: "Telangana", city: "Warangal", lat: 17.98, lng: 79.53 },
    { name: "NIT Calicut", state: "Kerala", city: "Kozhikode", lat: 11.32, lng: 75.93 },
    { name: "MNIT Jaipur", state: "Rajasthan", city: "Jaipur", lat: 26.86, lng: 75.81 },
    { name: "VNIT Nagpur", state: "Maharashtra", city: "Nagpur", lat: 21.13, lng: 79.05 },
    { name: "MANIT Bhopal", state: "Madhya Pradesh", city: "Bhopal", lat: 23.21, lng: 77.41 },
    { name: "NIT Kurukshetra", state: "Haryana", city: "Kurukshetra", lat: 29.95, lng: 76.81 },
    { name: "SVNIT Surat", state: "Gujarat", city: "Surat", lat: 21.16, lng: 72.79 },
    { name: "MNNIT Allahabad", state: "Uttar Pradesh", city: "Prayagraj", lat: 25.49, lng: 81.86 },
    { name: "NIT Jalandhar", state: "Punjab", city: "Jalandhar", lat: 31.40, lng: 75.53 },
    { name: "NIT Patna", state: "Bihar", city: "Patna", lat: 25.62, lng: 85.17 },
    { name: "NIT Silchar", state: "Assam", city: "Silchar", lat: 24.76, lng: 92.78 },
    { name: "NIT Durgapur", state: "West Bengal", city: "Durgapur", lat: 23.55, lng: 87.29 },
    { name: "NIT Jamshedpur", state: "Jharkhand", city: "Jamshedpur", lat: 22.78, lng: 86.14 },
    { name: "NIT Raipur", state: "Chhattisgarh", city: "Raipur", lat: 21.25, lng: 81.60 },
    { name: "NIT Agartala", state: "Tripura", city: "Agartala", lat: 23.83, lng: 91.34 },
    { name: "NIT Hamirpur", state: "Himachal Pradesh", city: "Hamirpur", lat: 31.71, lng: 76.52 },
    { name: "NIT Srinagar", state: "Jammu and Kashmir", city: "Srinagar", lat: 34.13, lng: 74.84 },
    { name: "NIT Uttarakhand", state: "Uttarakhand", city: "Srinagar (UK)", lat: 30.22, lng: 78.78 },
    { name: "NIT Goa", state: "Goa", city: "Cuncolim", lat: 15.18, lng: 74.00 },
    { name: "NIT Sikkim", state: "Sikkim", city: "Ravangla", lat: 27.31, lng: 88.36 },
    { name: "NIT Manipur", state: "Manipur", city: "Imphal", lat: 24.81, lng: 93.94 },
    { name: "NIT Meghalaya", state: "Meghalaya", city: "Shillong", lat: 25.61, lng: 91.91 },
    { name: "NIT Mizoram", state: "Mizoram", city: "Aizawl", lat: 23.73, lng: 92.72 },
    { name: "NIT Nagaland", state: "Nagaland", city: "Dimapur", lat: 25.91, lng: 93.72 },
    { name: "NIT Andhra Pradesh", state: "Andhra Pradesh", city: "Tadepalligudem", lat: 16.81, lng: 81.52 },
    { name: "NIT Arunachal Pradesh", state: "Arunachal Pradesh", city: "Jote", lat: 27.09, lng: 93.72 },
    { name: "NIT Delhi", state: "Delhi", city: "New Delhi", lat: 28.61, lng: 77.04 },
    { name: "NIT Puducherry", state: "Puducherry", city: "Karaikal", lat: 10.92, lng: 79.83 }
  ],
  ioe: [
    { name: "IIT Bombay", state: "Maharashtra", city: "Mumbai", lat: 19.13, lng: 72.92, type: "Public IoE" },
    { name: "IIT Delhi", state: "Delhi", city: "New Delhi", lat: 28.55, lng: 77.19, type: "Public IoE" },
    { name: "IIT Madras", state: "Tamil Nadu", city: "Chennai", lat: 12.99, lng: 80.23, type: "Public IoE" },
    { name: "IISc Bangalore", state: "Karnataka", city: "Bengaluru", lat: 13.02, lng: 77.57, type: "Public IoE" },
    { name: "Univ of Hyderabad", state: "Telangana", city: "Hyderabad", lat: 17.46, lng: 78.33, type: "Public IoE" },
    { name: "BHU Varanasi", state: "Uttar Pradesh", city: "Varanasi", lat: 25.27, lng: 82.99, type: "Public IoE" },
    { name: "Jadavpur University", state: "West Bengal", city: "Kolkata", lat: 22.50, lng: 88.37, type: "Public IoE" },
    { name: "Delhi University", state: "Delhi", city: "New Delhi", lat: 28.69, lng: 77.21, type: "Public IoE" },
    { name: "BITS Pilani", state: "Rajasthan", city: "Pilani", lat: 28.36, lng: 75.59, type: "Private IoE" },
    { name: "MAHE Manipal", state: "Karnataka", city: "Manipal", lat: 13.34, lng: 74.79, type: "Private IoE" },
    { name: "O.P. Jindal Global Univ", state: "Haryana", city: "Sonipat", lat: 28.99, lng: 77.02, type: "Private IoE" },
    { name: "KIIT Bhubaneswar", state: "Odisha", city: "Bhubaneswar", lat: 20.35, lng: 85.81, type: "Private IoE" }
  ],
  nirf: [
    { name: "IIT Madras", rank: 1, state: "Tamil Nadu", city: "Chennai", lat: 12.99, lng: 80.23 },
    { name: "IIT Delhi", rank: 2, state: "Delhi", city: "New Delhi", lat: 28.55, lng: 77.19 },
    { name: "IIT Bombay", rank: 3, state: "Maharashtra", city: "Mumbai", lat: 19.13, lng: 72.92 },
    { name: "IIT Kanpur", rank: 4, state: "Uttar Pradesh", city: "Kanpur", lat: 26.51, lng: 80.23 },
    { name: "IIT Kharagpur", rank: 5, state: "West Bengal", city: "Kharagpur", lat: 22.32, lng: 87.31 },
    { name: "IIT Roorkee", rank: 6, state: "Uttarakhand", city: "Roorkee", lat: 29.86, lng: 77.89 },
    { name: "IIT Hyderabad", rank: 7, state: "Telangana", city: "Sangareddy", lat: 17.59, lng: 78.12 },
    { name: "IIT Guwahati", rank: 8, state: "Assam", city: "Guwahati", lat: 26.19, lng: 91.69 },
    { name: "NIT Trichy", rank: 9, state: "Tamil Nadu", city: "Tiruchirappalli", lat: 10.76, lng: 78.81 },
    { name: "IIT BHU Varanasi", rank: 10, state: "Uttar Pradesh", city: "Varanasi", lat: 25.26, lng: 82.99 },
    { name: "IIT Indore", rank: 12, state: "Madhya Pradesh", city: "Indore", lat: 22.52, lng: 75.92 },
    { name: "NIT Rourkela", rank: 13, state: "Odisha", city: "Rourkela", lat: 22.25, lng: 84.90 },
    { name: "IIT ISM Dhanbad", rank: 15, state: "Jharkhand", city: "Dhanbad", lat: 23.81, lng: 86.44 },
    { name: "VIT Vellore", rank: 16, state: "Tamil Nadu", city: "Vellore", lat: 12.97, lng: 79.16 },
    { name: "NIT Surathkal", rank: 17, state: "Karnataka", city: "Mangalore", lat: 13.01, lng: 74.79 },
    { name: "Jadavpur University", rank: 18, state: "West Bengal", city: "Kolkata", lat: 22.50, lng: 88.37 },
    { name: "Anna University", rank: 20, state: "Tamil Nadu", city: "Chennai", lat: 13.01, lng: 80.24 },
    { name: "IIT Gandhinagar", rank: 25, state: "Gujarat", city: "Gandhinagar", lat: 23.21, lng: 72.68 },
    { name: "Amrita Vishwa Vidyapeetham", rank: 25, state: "Tamil Nadu", city: "Coimbatore", lat: 10.90, lng: 76.90 },
    { name: "NIT Warangal", rank: 28, state: "Telangana", city: "Warangal", lat: 17.98, lng: 79.53 },
    { name: "Thapar Institute", rank: 29, state: "Punjab", city: "Patiala", lat: 30.35, lng: 76.36 },
    { name: "IIIT Hyderabad", rank: 38, state: "Telangana", city: "Hyderabad", lat: 17.45, lng: 78.35 },
    { name: "IIT Bhubaneswar", rank: 39, state: "Odisha", city: "Bhubaneswar", lat: 20.15, lng: 85.67 },
    { name: "ICT Mumbai", rank: 41, state: "Maharashtra", city: "Mumbai", lat: 19.02, lng: 72.86 },
    { name: "SVNIT Surat", rank: 66, state: "Gujarat", city: "Surat", lat: 21.16, lng: 72.79 },
  ],
  naac: [
    { name: "IIT Madras", state: "Tamil Nadu", city: "Chennai", lat: 12.99, lng: 80.23 },
    { name: "IIT Bombay", state: "Maharashtra", city: "Mumbai", lat: 19.13, lng: 72.92 },
    { name: "IIT Delhi", state: "Delhi", city: "New Delhi", lat: 28.55, lng: 77.19 },
    { name: "IIT Kharagpur", state: "West Bengal", city: "Kharagpur", lat: 22.32, lng: 87.31 },
    { name: "IIT Roorkee", state: "Uttarakhand", city: "Roorkee", lat: 29.86, lng: 77.89 },
    { name: "IISc Bangalore", state: "Karnataka", city: "Bengaluru", lat: 13.02, lng: 77.57 },
    { name: "IIT Kanpur", state: "Uttar Pradesh", city: "Kanpur", lat: 26.51, lng: 80.23 },
    { name: "BHU Varanasi", state: "Uttar Pradesh", city: "Varanasi", lat: 25.27, lng: 82.99 },
    { name: "BITS Pilani", state: "Rajasthan", city: "Pilani", lat: 28.36, lng: 75.59 },
    { name: "VIT Vellore", state: "Tamil Nadu", city: "Vellore", lat: 12.97, lng: 79.16 },
    { name: "SRM IST", state: "Tamil Nadu", city: "Kanchipuram", lat: 12.82, lng: 80.04 },
    { name: "Jadavpur University", state: "West Bengal", city: "Kolkata", lat: 22.50, lng: 88.37 },
    { name: "Anna University", state: "Tamil Nadu", city: "Chennai", lat: 13.01, lng: 80.24 },
    { name: "NIT Trichy", state: "Tamil Nadu", city: "Tiruchirappalli", lat: 10.76, lng: 78.81 },
    { name: "NIT Rourkela", state: "Odisha", city: "Rourkela", lat: 22.25, lng: 84.90 },
    { name: "NIT Surathkal", state: "Karnataka", city: "Mangalore", lat: 13.01, lng: 74.79 },
    { name: "NIT Warangal", state: "Telangana", city: "Warangal", lat: 17.98, lng: 79.53 },
    { name: "PSG College of Tech", state: "Tamil Nadu", city: "Coimbatore", lat: 11.02, lng: 76.96 },
    { name: "MAHE Manipal", state: "Karnataka", city: "Manipal", lat: 13.34, lng: 74.79 },
    { name: "SASTRA University", state: "Tamil Nadu", city: "Thanjavur", lat: 10.73, lng: 79.02 },
    { name: "Amrita Vishwa Vidyapeetham", state: "Tamil Nadu", city: "Coimbatore", lat: 10.90, lng: 76.90 },
    { name: "Thapar Institute", state: "Punjab", city: "Patiala", lat: 30.35, lng: 76.36 },
    { name: "ICT Mumbai", state: "Maharashtra", city: "Mumbai", lat: 19.02, lng: 72.86 },
    { name: "RV College of Engg", state: "Karnataka", city: "Bengaluru", lat: 12.92, lng: 77.50 },
    { name: "BMS College of Engg", state: "Karnataka", city: "Bengaluru", lat: 12.94, lng: 77.57 },
    { name: "COEP Pune", state: "Maharashtra", city: "Pune", lat: 18.53, lng: 73.85 },
    { name: "MNIT Jaipur", state: "Rajasthan", city: "Jaipur", lat: 26.86, lng: 75.81 },
    { name: "VIT-AP Amaravati", state: "Andhra Pradesh", city: "Amaravati", lat: 16.50, lng: 80.50 }
  ]
};

const DISTRICT_DATA = {
  "Tamil Nadu": [
    { d: "Chennai", n: 120 }, { d: "Coimbatore", n: 85 }, { d: "Kanchipuram", n: 45 },
    { d: "Tiruchirappalli", n: 38 }, { d: "Madurai", n: 32 }, { d: "Salem", n: 30 },
    { d: "Erode", n: 28 }, { d: "Tirunelveli", n: 26 }, { d: "Vellore", n: 24 },
    { d: "Thiruvallur", n: 22 }, { d: "Namakkal", n: 18 }, { d: "Others (20+ districts)", n: 102 }
  ],
  "Maharashtra": [
    { d: "Pune", n: 95 }, { d: "Mumbai", n: 65 }, { d: "Nagpur", n: 32 },
    { d: "Aurangabad", n: 28 }, { d: "Nashik", n: 26 }, { d: "Thane", n: 22 },
    { d: "Kolhapur", n: 20 }, { d: "Solapur", n: 18 }, { d: "Amravati", n: 16 },
    { d: "Ahmednagar", n: 15 }, { d: "Others", n: 33 }
  ],
  "Karnataka": [
    { d: "Bengaluru Urban", n: 92 }, { d: "Dakshina Kannada", n: 22 }, { d: "Mysuru", n: 18 },
    { d: "Belagavi", n: 16 }, { d: "Tumakuru", n: 14 }, { d: "Hubli-Dharwad", n: 12 },
    { d: "Davanagere", n: 10 }, { d: "Kalaburagi", n: 9 }, { d: "Udupi", n: 8 },
    { d: "Bagalkot", n: 6 }, { d: "Others", n: 18 }
  ],
  "Telangana": [
    { d: "Hyderabad", n: 85 }, { d: "Ranga Reddy", n: 65 }, { d: "Medchal-Malkajgiri", n: 35 },
    { d: "Sangareddy", n: 18 }, { d: "Warangal", n: 12 }, { d: "Karimnagar", n: 10 },
    { d: "Nalgonda", n: 9 }, { d: "Khammam", n: 8 }, { d: "Mahabubnagar", n: 7 },
    { d: "Others", n: 11 }
  ],
  "Andhra Pradesh": [
    { d: "Visakhapatnam", n: 38 }, { d: "Guntur", n: 35 }, { d: "Krishna", n: 32 },
    { d: "Chittoor", n: 28 }, { d: "East Godavari", n: 24 }, { d: "Kurnool", n: 22 },
    { d: "Anantapur", n: 22 }, { d: "West Godavari", n: 20 }, { d: "SPSR Nellore", n: 18 },
    { d: "YSR Kadapa", n: 16 }, { d: "Others", n: 65 }
  ],
  "Uttar Pradesh": [
    { d: "Gautam Buddha Nagar (Noida)", n: 78 }, { d: "Ghaziabad", n: 42 },
    { d: "Lucknow", n: 28 }, { d: "Meerut", n: 22 }, { d: "Kanpur Nagar", n: 18 },
    { d: "Mathura", n: 16 }, { d: "Allahabad (Prayagraj)", n: 14 }, { d: "Agra", n: 14 },
    { d: "Varanasi", n: 12 }, { d: "Bareilly", n: 10 }, { d: "Others", n: 66 }
  ],
  "Kerala": [
    { d: "Ernakulam", n: 32 }, { d: "Thiruvananthapuram", n: 24 }, { d: "Thrissur", n: 18 },
    { d: "Kozhikode", n: 16 }, { d: "Palakkad", n: 14 }, { d: "Kollam", n: 12 },
    { d: "Kannur", n: 10 }, { d: "Kottayam", n: 10 }, { d: "Malappuram", n: 9 },
    { d: "Pathanamthitta", n: 6 }, { d: "Others", n: 4 }
  ],
  "Delhi": [
    { d: "South Delhi", n: 8 }, { d: "New Delhi", n: 6 }, { d: "North Delhi", n: 5 },
    { d: "West Delhi", n: 4 }, { d: "South-West Delhi", n: 3 }, { d: "East Delhi", n: 3 },
    { d: "North-East Delhi", n: 2 }, { d: "North-West Delhi", n: 1 }
  ],
  "Gujarat": [
    { d: "Ahmedabad", n: 32 }, { d: "Surat", n: 22 }, { d: "Vadodara", n: 18 },
    { d: "Rajkot", n: 14 }, { d: "Gandhinagar", n: 12 }, { d: "Anand", n: 8 },
    { d: "Bharuch", n: 6 }, { d: "Mehsana", n: 5 }, { d: "Others", n: 8 }
  ],
  "West Bengal": [
    { d: "Kolkata", n: 28 }, { d: "Howrah", n: 16 }, { d: "North 24 Parganas", n: 14 },
    { d: "Hooghly", n: 10 }, { d: "Burdwan (Purba)", n: 8 }, { d: "Nadia", n: 8 },
    { d: "Murshidabad", n: 6 }, { d: "Paschim Medinipur", n: 6 }, { d: "Others", n: 14 }
  ],
  "Madhya Pradesh": [
    { d: "Indore", n: 32 }, { d: "Bhopal", n: 28 }, { d: "Gwalior", n: 14 },
    { d: "Jabalpur", n: 12 }, { d: "Ujjain", n: 8 }, { d: "Sagar", n: 6 },
    { d: "Rewa", n: 5 }, { d: "Satna", n: 5 }, { d: "Others", n: 30 }
  ],
  "Rajasthan": [
    { d: "Jaipur", n: 38 }, { d: "Jodhpur", n: 16 }, { d: "Udaipur", n: 14 },
    { d: "Kota", n: 12 }, { d: "Sikar", n: 10 }, { d: "Ajmer", n: 9 },
    { d: "Alwar", n: 9 }, { d: "Bikaner", n: 7 }, { d: "Others", n: 20 }
  ]
};

const NOTABLE_COLLEGES = {
  "Tamil Nadu": [
    { name: "IIT Madras", district: "Chennai", tag: "IIT" },
    { name: "NIT Trichy", district: "Tiruchirappalli", tag: "NIT" },
    { name: "Anna University (CEG)", district: "Chennai", tag: "State Univ" },
    { name: "VIT Vellore", district: "Vellore", tag: "Deemed" },
    { name: "SRM IST", district: "Kanchipuram", tag: "Deemed" },
    { name: "PSG College of Technology", district: "Coimbatore", tag: "Private" },
    { name: "SSN College of Engineering", district: "Kanchipuram", tag: "Private" },
    { name: "SASTRA University", district: "Thanjavur", tag: "Deemed" },
    { name: "Amrita Vishwa Vidyapeetham", district: "Coimbatore", tag: "Deemed" },
    { name: "Thiagarajar College of Engg", district: "Madurai", tag: "Private" },
    { name: "Kumaraguru College of Tech", district: "Coimbatore", tag: "Private" },
    { name: "Coimbatore Inst of Technology", district: "Coimbatore", tag: "Private" },
    { name: "Bannari Amman Inst of Tech", district: "Erode", tag: "Private" },
    { name: "Karunya Institute", district: "Coimbatore", tag: "Deemed" },
    { name: "Velammal Engineering College", district: "Chennai", tag: "Private" }
  ],
  "Maharashtra": [
    { name: "IIT Bombay", district: "Mumbai", tag: "IIT" },
    { name: "VNIT Nagpur", district: "Nagpur", tag: "NIT" },
    { name: "ICT Mumbai", district: "Mumbai", tag: "Deemed" },
    { name: "COEP Pune", district: "Pune", tag: "State Univ" },
    { name: "VJTI Mumbai", district: "Mumbai", tag: "State Univ" },
    { name: "PICT Pune", district: "Pune", tag: "Private" },
    { name: "MIT WPU", district: "Pune", tag: "Deemed" },
    { name: "Symbiosis Inst of Tech", district: "Pune", tag: "Deemed" },
    { name: "K J Somaiya Inst", district: "Mumbai", tag: "Private" }
  ],
  "Karnataka": [
    { name: "IISc Bangalore", district: "Bengaluru Urban", tag: "IoE" },
    { name: "NIT Surathkal", district: "Dakshina Kannada", tag: "NIT" },
    { name: "IIT Dharwad", district: "Dharwad", tag: "IIT" },
    { name: "RV College of Engineering", district: "Bengaluru Urban", tag: "Private" },
    { name: "BMS College of Engineering", district: "Bengaluru Urban", tag: "Private" },
    { name: "MS Ramaiah Inst of Tech", district: "Bengaluru Urban", tag: "Private" },
    { name: "PES University", district: "Bengaluru Urban", tag: "Private" },
    { name: "MAHE Manipal", district: "Udupi", tag: "IoE" },
    { name: "Dayananda Sagar Univ", district: "Bengaluru Urban", tag: "Private" },
    { name: "KLE Tech University", district: "Hubli-Dharwad", tag: "Deemed" }
  ],
  "Telangana": [
    { name: "IIT Hyderabad", district: "Sangareddy", tag: "IIT" },
    { name: "NIT Warangal", district: "Warangal", tag: "NIT" },
    { name: "IIIT Hyderabad", district: "Hyderabad", tag: "Deemed" },
    { name: "BITS Pilani Hyderabad", district: "Hyderabad", tag: "Deemed" },
    { name: "JNTU Hyderabad (UCE)", district: "Hyderabad", tag: "State Univ" },
    { name: "Osmania Univ College of Engg", district: "Hyderabad", tag: "State Univ" },
    { name: "VNR VJIET", district: "Hyderabad", tag: "Private" },
    { name: "Vasavi College of Engg", district: "Hyderabad", tag: "Private" },
    { name: "CBIT Hyderabad", district: "Hyderabad", tag: "Private" },
    { name: "MGIT Hyderabad", district: "Ranga Reddy", tag: "Private" }
  ],
  "Andhra Pradesh": [
    { name: "IIT Tirupati", district: "Chittoor", tag: "IIT" },
    { name: "NIT Andhra Pradesh", district: "West Godavari", tag: "NIT" },
    { name: "IIIT Sri City", district: "Chittoor", tag: "Deemed" },
    { name: "GITAM Visakhapatnam", district: "Visakhapatnam", tag: "Deemed" },
    { name: "Andhra Univ College of Engg", district: "Visakhapatnam", tag: "State Univ" },
    { name: "JNTU Kakinada", district: "East Godavari", tag: "State Univ" },
    { name: "VIT-AP Amaravati", district: "Guntur", tag: "Deemed" },
    { name: "K L University", district: "Guntur", tag: "Deemed" },
    { name: "SRM University AP", district: "Guntur", tag: "Private" }
  ],
  "Uttar Pradesh": [
    { name: "IIT Kanpur", district: "Kanpur Nagar", tag: "IIT" },
    { name: "IIT BHU Varanasi", district: "Varanasi", tag: "IIT" },
    { name: "MNNIT Allahabad", district: "Prayagraj", tag: "NIT" },
    { name: "IIIT Allahabad", district: "Prayagraj", tag: "Deemed" },
    { name: "MMMUT Gorakhpur", district: "Gorakhpur", tag: "State Univ" },
    { name: "HBTU Kanpur", district: "Kanpur Nagar", tag: "State Univ" },
    { name: "JSS Academy of Tech", district: "Gautam Buddha Nagar", tag: "Private" },
    { name: "Amity University Noida", district: "Gautam Buddha Nagar", tag: "Private" },
    { name: "Bennett University", district: "Gautam Buddha Nagar", tag: "Private" },
    { name: "AKGEC Ghaziabad", district: "Ghaziabad", tag: "Private" }
  ],
  "Kerala": [
    { name: "IIT Palakkad", district: "Palakkad", tag: "IIT" },
    { name: "NIT Calicut", district: "Kozhikode", tag: "NIT" },
    { name: "IIIT Kottayam", district: "Kottayam", tag: "Deemed" },
    { name: "College of Engg Trivandrum", district: "Thiruvananthapuram", tag: "State Univ" },
    { name: "GEC Thrissur", district: "Thrissur", tag: "State Univ" },
    { name: "Amrita Amritapuri", district: "Kollam", tag: "Deemed" },
    { name: "TKM College of Engg", district: "Kollam", tag: "Private" },
    { name: "MA College of Engg", district: "Kottayam", tag: "Private" },
    { name: "Rajagiri School of Engg", district: "Ernakulam", tag: "Private" }
  ],
  "Delhi": [
    { name: "IIT Delhi", district: "South Delhi", tag: "IIT" },
    { name: "NIT Delhi", district: "North-West Delhi", tag: "NIT" },
    { name: "Delhi University Engg", district: "North Delhi", tag: "IoE" },
    { name: "DTU (Delhi Tech Univ)", district: "North-West Delhi", tag: "State Univ" },
    { name: "NSUT Dwarka", district: "South-West Delhi", tag: "State Univ" },
    { name: "IIIT Delhi", district: "South Delhi", tag: "State Univ" },
    { name: "Jamia Millia Islamia", district: "South-East Delhi", tag: "Central" },
    { name: "IGDTUW (women)", district: "Central Delhi", tag: "State Univ" }
  ],
  "Gujarat": [
    { name: "IIT Gandhinagar", district: "Gandhinagar", tag: "IIT" },
    { name: "SVNIT Surat", district: "Surat", tag: "NIT" },
    { name: "DAIICT", district: "Gandhinagar", tag: "Deemed" },
    { name: "Nirma University", district: "Ahmedabad", tag: "Deemed" },
    { name: "PDPU", district: "Gandhinagar", tag: "State Univ" },
    { name: "L.D. College of Engg", district: "Ahmedabad", tag: "State Univ" },
    { name: "M.S. University Baroda", district: "Vadodara", tag: "State Univ" },
    { name: "CHARUSAT", district: "Anand", tag: "Deemed" }
  ],
  "West Bengal": [
    { name: "IIT Kharagpur", district: "Paschim Medinipur", tag: "IIT" },
    { name: "NIT Durgapur", district: "Burdwan (Purba)", tag: "NIT" },
    { name: "Jadavpur University", district: "Kolkata", tag: "IoE" },
    { name: "IIEST Shibpur", district: "Howrah", tag: "Central" },
    { name: "IIIT Kalyani", district: "Nadia", tag: "Deemed" },
    { name: "Heritage Inst of Tech", district: "Kolkata", tag: "Private" },
    { name: "Techno India University", district: "Kolkata", tag: "Private" }
  ],
  "Madhya Pradesh": [
    { name: "IIT Indore", district: "Indore", tag: "IIT" },
    { name: "MANIT Bhopal", district: "Bhopal", tag: "NIT" },
    { name: "IIIT-DM Jabalpur", district: "Jabalpur", tag: "Deemed" },
    { name: "SGSITS Indore", district: "Indore", tag: "State Univ" },
    { name: "MITS Gwalior", district: "Gwalior", tag: "State Univ" },
    { name: "IPS Academy Indore", district: "Indore", tag: "Private" }
  ],
  "Rajasthan": [
    { name: "IIT Jodhpur", district: "Jodhpur", tag: "IIT" },
    { name: "MNIT Jaipur", district: "Jaipur", tag: "NIT" },
    { name: "BITS Pilani", district: "Jhunjhunu", tag: "IoE" },
    { name: "Manipal University Jaipur", district: "Jaipur", tag: "Deemed" },
    { name: "LNMIIT Jaipur", district: "Jaipur", tag: "Private" },
    { name: "JECRC Jaipur", district: "Jaipur", tag: "Private" },
    { name: "Poornima University", district: "Jaipur", tag: "Private" }
  ]
};

const FILTERS = {
  all: {
    title: "All engineering colleges", sub: "Total AICTE-approved institutions by state · 2023-24 (approximate)",
    mode: "choropleth", pinKey: null,
    panelMeta: "Includes · IITs · NITs · TNEA · Deemed · Private",
    panelTitle: "Total engineering institutions",
    panelBody: "Combined count of unique AICTE-approved engineering institutions. Tamil Nadu, Maharashtra, Andhra Pradesh, Telangana and Karnataka together host nearly 60% of all colleges in India."
  },
  iit: {
    title: "Indian Institutes of Technology (IITs)", sub: "23 IITs · pins show exact locations",
    mode: "pins", pinKey: "iit",
    panelMeta: "Tier-1 · centrally funded · JEE Advanced",
    panelTitle: "IITs across India",
    panelBody: "23 IITs spread across 22 states. Uttar Pradesh holds two (IIT Kanpur and IIT BHU Varanasi). Combined intake ~17,000 BTech seats. The newest six (Tirupati, Palakkad, Bhilai, Jammu, Dharwad, Goa) were established in 2015–16."
  },
  nit: {
    title: "National Institutes of Technology (NITs)", sub: "31 NITs · pins show exact locations",
    mode: "pins", pinKey: "nit",
    panelMeta: "Tier-1.5 · centrally funded · JEE Main + JoSAA",
    panelTitle: "NITs across India",
    panelBody: "Every state and major UT has exactly one NIT — a deliberate policy when the Regional Engineering Colleges were upgraded in 2002. Total intake ~24,000 BTech seats. NIT Trichy, NIT Surathkal and NIT Warangal consistently rank in the top 5."
  },
  tnea: {
    title: "TNEA colleges (Tamil Nadu only)", sub: "571 colleges admit through Anna University TNEA",
    mode: "choropleth", pinKey: null,
    panelMeta: "Tamil Nadu only · Class 12 cut-off based",
    panelTitle: "Tamil Nadu Engineering Admissions (TNEA)",
    panelBody: "TNEA is a state counselling process run by Anna University covering government, aided and self-financing engineering colleges in TN. It uses Class 12 PCM cut-off (out of 200) instead of JEE Main — which is why TN's engineering ecosystem looks structurally different."
  },
  deemed: {
    title: "Deemed-to-be Universities", sub: "~125 deemed universities with engineering programmes",
    mode: "choropleth", pinKey: null,
    panelMeta: "UGC designation · autonomous · independent admission",
    panelTitle: "Deemed universities",
    panelBody: "Autonomous institutions granted university-equivalent status by the UGC. They set their own curriculum, admission process (VITEEE, SRMJEE, BITSAT, KIITEE, MET) and fees. Tamil Nadu, Maharashtra and Karnataka host the largest concentrations."
  },
  private: {
    title: "Private engineering colleges", sub: "Self-financed colleges affiliated to state universities",
    mode: "choropleth", pinKey: null,
    panelMeta: "State counselling · self-financed · affiliated",
    panelTitle: "Private engineering colleges",
    panelBody: "Self-financed colleges affiliated to a state technical university. Admission via state counselling — TNEA, AP-EAPCET, TS-EAMCET, KEAM, KCET, COMEDK, MHT-CET, WBJEE, UP-JEE — or management/NRI quota. Tamil Nadu leads at ~540 (which overlaps with TNEA)."
  },
  ioe: {
    title: "Institutions of Eminence (IoE)", sub: "12 institutions · pins show exact locations",
    mode: "pins", pinKey: "ioe",
    panelMeta: "MoE designation · 8 public + 4 private",
    panelTitle: "Institutions of Eminence",
    panelBody: "Special MoE designation conferring exceptional autonomy and ₹1,000 cr in central support over 5 years. 8 public (IIT Bombay, IIT Madras, IIT Delhi, IISc, BHU, Jadavpur, Delhi University, Univ of Hyderabad) + 4 private (BITS Pilani, MAHE Manipal, O.P. Jindal, KIIT)."
  },
  nirf: {
    title: "NIRF top-ranked institutions", sub: "MoE NIRF 2026 · map pins show 25 leading institutes",
    mode: "pins", pinKey: "nirf",
    panelMeta: "NIRF 2026 · MoE annual ranking",
    panelTitle: "NIRF top-ranked — Engineering",
    panelBody: "The MoE's National Institutional Ranking Framework ranks institutes annually on teaching, research, graduation outcomes, outreach and perception. The map pins show 25 leading NIRF 2026 institutes by location — see the NIRF section below for all 120 ranked colleges in this directory, with exact ranks and branch-portfolio waffles."
  },
  naac: {
    title: "NAAC A++ accredited (engineering)", sub: "~28 colleges with CGPA 3.51–4.00 · pins show locations",
    mode: "pins", pinKey: "naac",
    panelMeta: "NAAC A++ · CGPA 3.51 – 4.00",
    panelTitle: "NAAC A++ — Engineering institutions",
    panelBody: "The National Assessment and Accreditation Council's A++ grade (highest band) is awarded to institutions scoring CGPA 3.51–4.00 across 7 criteria including teaching, research, infrastructure, governance and student support."
  }
};

let currentFilter = "all";
let selectedState = null;

function totalForFilter(key) {
  if (key === 'all') return Object.values(STATE_DATA).reduce((s, r) => s + (r.total || 0), 0);
  return Object.values(STATE_DATA).reduce((s, r) => s + (r[key] || 0), 0);
}
['all','iit','nit','tnea','deemed','private','ioe','nirf','naac'].forEach(k => {
  const el = document.getElementById('badge-' + k);
  if (el) el.textContent = totalForFilter(k).toLocaleString('en-IN');
});

const svg = d3.select("#india-map");
const tooltip = d3.select("#mapTooltip");
const mapLoading = document.getElementById('mapLoading');
let mapPaths = null;
let projection = null;
const mapWidth = 720, mapHeight = 720;

function normaliseName(raw) {
  if (!raw) return raw;
  let n = raw.trim();
  const map = {
    "Orissa": "Odisha", "Pondicherry": "Puducherry", "Uttaranchal": "Uttarakhand",
    "Telengana": "Telangana", "NCT of Delhi": "Delhi", "Delhi (NCT)": "Delhi",
    "Jammu & Kashmir": "Jammu and Kashmir", "Jammu And Kashmir": "Jammu and Kashmir",
    "Andaman & Nicobar Islands": "Andaman and Nicobar Islands",
    "Andaman & Nicobar Island": "Andaman and Nicobar Islands",
    "Dadra and Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "Daman and Diu": "Dadra and Nagar Haveli and Daman and Diu",
    "Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu"
  };
  return map[n] || n;
}

const GEO_SOURCES = [
  "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@ef25ebc/geojson/india.geojson",
  "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@main/geojson/india.geojson",
  "https://cdn.jsdelivr.net/gh/Anuj-Gupta4/india-states-and-uts-geojson@main/india_state.geojson",
  "https://cdn.jsdelivr.net/gh/geohacker/india@master/state/india_telengana.geojson"
];

function loadGeo() {
  return GEO_SOURCES.reduce((p, url) => p.catch(() => d3.json(url)), Promise.reject());
}

loadGeo().then(geo => {
  mapLoading.style.display = "none";
  renderMap(geo);
  render(currentFilter);
}).catch(err => {
  console.warn("Map load failed:", err);
  mapLoading.innerHTML = "<strong style='color:var(--navy-ink);font-family:Fraunces,serif;font-size:16px;'>Map couldn't load</strong><br>The ranked list and stats below still work. Refresh to retry.";
  render(currentFilter);
});

function renderMap(geo) {
  projection = d3.geoMercator().center([82.5, 22.5]).scale(950).translate([mapWidth / 2, mapHeight / 2]);
  const pathGen = d3.geoPath().projection(projection);

  svg.append("g").attr("class", "states-layer");
  svg.append("g").attr("class", "pins-layer");

  mapPaths = svg.select(".states-layer").selectAll("path.state")
    .data(geo.features).enter().append("path")
    .attr("class", "state").attr("d", pathGen).attr("fill", "var(--cream-2)")
    .on("mousemove", function(event, d) {
      const props = d.properties || {};
      const rawName = props.st_nm || props.NAME_1 || props.STATE || props.name || props.State_Name;
      const name = normaliseName(rawName);
      const data = STATE_DATA[name];
      const val = data ? (data[currentFilter] || 0) : 0;
      const cfg = FILTERS[currentFilter];
      const wrap = svg.node().getBoundingClientRect();
      const x = event.clientX - wrap.left + 14;
      const y = event.clientY - wrap.top + 14;
      tooltip.html(
        "<strong>" + (name || "Unknown") + "</strong>" +
        "<div class='tip-num'>" + val.toLocaleString('en-IN') + "</div>" +
        "<div class='tip-label'>" + (currentFilter === 'all' ? 'engineering colleges' : cfg.title) + "</div>" +
        (data && DISTRICT_DATA[name] ? "<div class='tip-sub'>Click to drill down →</div>" : (data ? "<div class='tip-sub'>Click for state detail →</div>" : ""))
      ).style("left", x + "px").style("top", y + "px").style("opacity", 1);
    })
    .on("mouseleave", () => tooltip.style("opacity", 0))
    .on("click", function(event, d) {
      const props = d.properties || {};
      const rawName = props.st_nm || props.NAME_1 || props.STATE || props.name || props.State_Name;
      const name = normaliseName(rawName);
      if (STATE_DATA[name]) {
        selectedState = name;
        d3.selectAll("#india-map path.state").classed("selected", false);
        d3.select(this).classed("selected", true);
        renderStateDetail(name);
      }
    });
}

function renderPins(pinKey) {
  const pinsLayer = svg.select(".pins-layer");
  pinsLayer.selectAll("*").remove();
  if (!pinKey || !projection) return;
  const pins = INSTITUTION_PINS[pinKey] || [];

  pinsLayer.selectAll("circle.pin")
    .data(pins).enter().append("circle")
    .attr("class", "pin")
    .attr("cx", d => projection([d.lng, d.lat])[0])
    .attr("cy", d => projection([d.lng, d.lat])[1])
    .attr("r", 0)
    .on("mousemove", function(event, d) {
      const wrap = svg.node().getBoundingClientRect();
      const x = event.clientX - wrap.left + 14;
      const y = event.clientY - wrap.top + 14;
      tooltip.html(
        "<strong>" + d.name + (d.rank ? " · #" + d.rank : "") + "</strong>" +
        "<div class='tip-label' style='margin-top:6px;'>" + d.city + ", " + d.state + "</div>" +
        (d.type ? "<div class='tip-sub'>" + d.type + "</div>" : "")
      ).style("left", x + "px").style("top", y + "px").style("opacity", 1);
      d3.select(this).attr("r", 9);
    })
    .on("mouseleave", function() { tooltip.style("opacity", 0); d3.select(this).attr("r", 5.5); })
    .transition().duration(450).delay((d, i) => i * 25).attr("r", 5.5);
}

const RAMP = ["#FBF7EE", "#E8DFC8", "#B7C2DC", "#7B91C2", "#3D5DA3", "#0E3A8A"];

(function buildLegend() {
  const c = document.getElementById('legendScale');
  c.innerHTML = "";
  RAMP.forEach(col => { const d = document.createElement('div'); d.style.background = col; c.appendChild(d); });
})();

function colorFor(value, max) {
  if (!value || max === 0) return RAMP[0];
  const ratio = value / max;
  if (ratio === 0) return RAMP[0];
  if (ratio < 0.04)  return RAMP[1];
  if (ratio < 0.12)  return RAMP[2];
  if (ratio < 0.28)  return RAMP[3];
  if (ratio < 0.60)  return RAMP[4];
  return RAMP[5];
}

function render(filterKey) {
  currentFilter = filterKey;
  const cfg = FILTERS[filterKey];

  document.getElementById('mapTitle').textContent = cfg.title;
  document.getElementById('mapSub').textContent = cfg.sub;
  document.getElementById('panelMeta').textContent = cfg.panelMeta;
  document.getElementById('panelTitle').textContent = cfg.panelTitle;
  document.getElementById('panelBody').textContent = cfg.panelBody;

  document.querySelectorAll('.filter-pill').forEach(b => {
    b.setAttribute('aria-pressed', b.dataset.filter === filterKey ? 'true' : 'false');
  });

  document.getElementById('pinNote').classList.toggle('visible', cfg.mode === 'pins');

  const values = Object.values(STATE_DATA).map(r => r[filterKey] || 0);
  const max = Math.max(...values, 1);

  if (mapPaths) {
    mapPaths.transition().duration(450).attr("fill", function(d) {
      const props = d.properties || {};
      const rawName = props.st_nm || props.NAME_1 || props.STATE || props.name || props.State_Name;
      const name = normaliseName(rawName);
      const data = STATE_DATA[name];
      const val = data ? (data[filterKey] || 0) : 0;
      if (cfg.mode === 'pins') return val > 0 ? "#F0E5D0" : RAMP[0];
      return colorFor(val, max);
    });
  }
  renderPins(cfg.mode === 'pins' ? cfg.pinKey : null);

  if (selectedState) renderStateDetail(selectedState); else renderTopStates();

  const total = filterKey === 'all'
    ? Object.values(STATE_DATA).reduce((s, r) => s + r.total, 0)
    : Object.values(STATE_DATA).reduce((s, r) => s + (r[filterKey] || 0), 0);
  document.getElementById('statTotal').textContent = total.toLocaleString('en-IN');

  const withData = Object.entries(STATE_DATA).filter(([_, r]) => (r[filterKey] || 0) > 0);
  document.getElementById('statStates').textContent = withData.length;

  const topState = withData.sort((a, b) => b[1][filterKey] - a[1][filterKey])[0];
  const topEl = document.getElementById('statTop');
  if (topState) {
    topEl.textContent = topState[0];
    topEl.style.fontSize = topState[0].length > 10 ? "clamp(18px, 2.2vw, 26px)" : "";
  } else topEl.textContent = "—";

  const south = ["Tamil Nadu", "Andhra Pradesh", "Telangana", "Karnataka", "Kerala", "Puducherry"];
  const southTotal = south.reduce((s, st) => s + ((STATE_DATA[st] || {})[filterKey] || 0), 0);
  const sharePct = total ? Math.round((southTotal / total) * 100) : 0;
  document.getElementById('statSouth').innerHTML = sharePct + "<span>%</span>";
}

function renderTopStates() {
  const cfg = FILTERS[currentFilter];
  const filterKey = currentFilter;

  const ranked = Object.entries(STATE_DATA)
    .map(([state, r]) => ({ state, val: r[filterKey] || 0 }))
    .filter(r => r.val > 0).sort((a, b) => b.val - a.val);

  const showCount = Math.min(ranked.length, 10);
  const top = ranked.slice(0, showCount);
  const topMax = top.length ? top[0].val : 1;

  const titleLabel = filterKey === "all" ? "all categories" : cfg.title.split(" ")[0];
  const subLabel = "Click any state for district-wise detail";

  let html = "<h3>Top states · " + titleLabel + "</h3>"
           + "<div class='sub'>" + subLabel + "</div>"
           + "<ol class='ranked-list'>";

  if (top.length === 0) {
    html += "<li style='padding:24px 0;color:var(--muted);font-size:14px;list-style:none;'>No data for this filter.</li>";
  } else {
    top.forEach((r, i) => {
      const pct = Math.max(2, Math.round((r.val / topMax) * 100));
      html += "<li class='ranked-item' data-state='" + r.state + "'>"
            + "<div class='ranked-num'>" + String(i + 1).padStart(2, '0') + "</div>"
            + "<div class='ranked-bar-wrap'>"
              + "<div class='ranked-bar-name'>" + r.state + "</div>"
              + "<div class='ranked-bar-track'><div class='ranked-bar-fill' style='width:" + pct + "%'></div></div>"
            + "</div>"
            + "<div class='ranked-val'>" + r.val.toLocaleString('en-IN') + "</div>"
          + "</li>";
    });
  }
  html += "</ol>";

  document.getElementById('rightPanel').innerHTML = html;

  document.querySelectorAll('.ranked-item').forEach(li => {
    li.addEventListener('click', () => {
      const state = li.dataset.state;
      if (state && STATE_DATA[state]) {
        selectedState = state;
        d3.selectAll("#india-map path.state").classed("selected", function(d) {
          const props = (d && d.properties) || {};
          const rawName = props.st_nm || props.NAME_1 || props.STATE || props.name || props.State_Name;
          return normaliseName(rawName) === state;
        });
        renderStateDetail(state);
      }
    });
  });
}

function renderStateDetail(state) {
  const data = STATE_DATA[state];
  if (!data) return;
  const districts = DISTRICT_DATA[state] || [];
  const colleges = NOTABLE_COLLEGES[state] || [];

  let html = "<div class='drill-header'>"
           + "<div class='drill-title'><small>State drill-down</small>" + state + "</div>"
           + "<button class='drill-back' onclick='clearSelection()'>India view</button>"
           + "</div>";

  html += "<div class='drill-stats'>"
        + "<div class='drill-stat'><div class='num'>" + data.total.toLocaleString('en-IN') + "</div><div class='lab'>Total engg colleges</div></div>"
        + "<div class='drill-stat'><div class='num'>" + (data.iit + data.nit) + "<span>•</span></div><div class='lab'>IITs + NITs</div></div>"
        + "<div class='drill-stat'><div class='num'>" + data.deemed + "</div><div class='lab'>Deemed univ.</div></div>"
        + "<div class='drill-stat'><div class='num'>" + (data.nirf || 0) + "<span>•</span></div><div class='lab'>In NIRF Top 100</div></div>"
        + "</div>";

  if (districts.length > 0) {
    html += "<div class='drill-section-title'>Top districts · engg college count</div><ol class='ranked-list'>";
    const maxD = Math.max(...districts.map(d => d.n));
    districts.slice(0, 10).forEach((d, i) => {
      const pct = Math.max(3, Math.round((d.n / maxD) * 100));
      html += "<li class='ranked-item' style='cursor:default;'>"
            + "<div class='ranked-num'>" + String(i + 1).padStart(2, '0') + "</div>"
            + "<div class='ranked-bar-wrap'>"
              + "<div class='ranked-bar-name'>" + d.d + "</div>"
              + "<div class='ranked-bar-track'><div class='ranked-bar-fill' style='width:" + pct + "%'></div></div>"
            + "</div>"
            + "<div class='ranked-val'>" + d.n + "</div>"
          + "</li>";
    });
    html += "</ol>";
  } else {
    html += "<div class='drill-section-title'>District breakdown</div>"
          + "<div style='font-size:13px; color:var(--muted); padding:8px 0;'>District-wise breakdown not curated yet for this state. We're adding more states monthly.</div>";
  }

  if (colleges.length > 0) {
    html += "<div class='drill-section-title'>Notable institutions</div><ul class='college-list'>";
    colleges.forEach(c => {
      const tagClass = (c.tag || "").toLowerCase().replace(/[^a-z]/g, "");
      html += "<li class='college-item'>"
            + "<div><div class='name'>" + c.name + "</div><div class='meta'>" + c.district + "</div></div>"
            + "<span class='tag " + tagClass + "'>" + c.tag + "</span>"
          + "</li>";
    });
    html += "</ul>";
  }

  document.getElementById('rightPanel').innerHTML = html;
}

window.clearSelection = function() {
  selectedState = null;
  d3.selectAll("#india-map path.state").classed("selected", false);
  renderTopStates();
};

document.querySelectorAll('.filter-pill').forEach(btn => {
  btn.addEventListener('click', () => render(btn.dataset.filter));
});

document.getElementById('hamburger').addEventListener('click', () => {
  document.getElementById('navLinks').classList.toggle('open');
});

const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

renderTopStates();
render(currentFilter);

// ════════════════════════════════════════════════════════════════
// COLLEGES DATABASE — comprehensive list with branches offered
// ════════════════════════════════════════════════════════════════
// Branch code legend (short → full label)

// Branch → family index (0=computer,1=circuit,2=mech,3=process) — mirrors data gen
const FAM_LOOKUP = {};
(function(){
  const sets = [
    ["CSE","IT","AIDS","AIML","AI","DS","Cyber","CSBS","CSD","ICT","SE","CompSci"],
    ["ECE","EE","EEE","E&I","EIE","Instru","VLSI","Electronics","ECM","Comm","Electrical"],
    ["Mech","Aero","Auto","Naval","Marine","Mining","Prod","MME","Mechatronics","Robotics","Manufacturing","Industrial","Metal","Production","Aerospace"],
    ["Civil","Chem","Bio","Env","Energy","Textile","Arch","Agri","EarthSci","Food","EngPhy","Math","PulpPaper","Petroleum","Materials","Chemical","Biotech","BioMed","Pharma","Plastics","Polymer","Geo","Petro","EngDes","Nano","Rubber","Print","Leather","WaterRes"]
  ];
  sets.forEach((arr,i)=>arr.forEach(k=>FAM_LOOKUP[k.toLowerCase()]=i));
})();
function branchFamilyIdx(code){
  const c = (code||"").toLowerCase();
  if (c in FAM_LOOKUP) return FAM_LOOKUP[c];
  if (/cs|comp|info|^ai|data|soft/.test(c)) return 0;
  if (/^ec|^ele|eee|vlsi|instru|comm/.test(c)) return 1;
  if (/mech|aero|auto|marine|mining|prod|robot|metal/.test(c)) return 2;
  return 3;
}

const BRANCH_LABELS = {
  CSE: "Computer Science",
  IT: "Information Tech",
  AIML: "AI & ML",
  AIDS: "AI & Data Science",
  ECE: "Electronics & Comm",
  EEE: "Electrical & Electronics",
  EE: "Electrical Engg",
  Mech: "Mechanical",
  Civil: "Civil",
  Chem: "Chemical",
  Aero: "Aerospace",
  Auto: "Automobile",
  Bio: "Biotechnology",
  MME: "Metallurgy & Materials",
  Mining: "Mining",
  Petro: "Petroleum",
  Marine: "Marine",
  Naval: "Naval Architecture",
  Textile: "Textile",
  Prod: "Production / Industrial",
  Robot: "Robotics",
  EngDes: "Engineering Design",
  EngPhy: "Engineering Physics",
  Food: "Food Tech",
  Env: "Environmental",
  Arch: "Architecture",
  Cer: "Ceramic",
  Pharma: "Pharma",
  Math: "Math & Computing",
  ICT: "Info & Comm Tech",
  Agri: "Agricultural",
  PulpPaper: "Pulp & Paper",
  MinMach: "Mineral Machinery",
  Energy: "Energy & Environment",
  Pulp: "Pulp & Paper",
  EarthSci: "Earth Sciences",
  Space: "Space Science",
  Comm: "Communication Engg"
};

// Compact format: n=name, s=state, d=district, t=type, r=NIRF rank (optional), b=branches
// Data now lives in app/data/files/*.csv and is served by /api/data/*.js
const COLLEGES_DB = window.EA_ENGG_COLLEGES || [];

// Collect unique values for filter UIs
const ALL_BRANCHES = Array.from(new Set(COLLEGES_DB.flatMap(c => c.b))).sort();
const ALL_TYPES = ["IIT","NIT","IIIT","IoE","Deemed","Private","State","Central"];
const ALL_STATES_IN_DB = Array.from(new Set(COLLEGES_DB.map(c => c.s))).sort();

// Browse state
const browseState = {
  search: "",
  types: new Set(),       // empty = all types
  state: "",              // empty = all states
  branches: new Set(),    // empty = all branches
  sort: "rank"
};

// Build state dropdown
(function buildStateDropdown() {
  const sel = document.getElementById('stateFilter');
  ALL_STATES_IN_DB.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    sel.appendChild(opt);
  });
})();

// Build type chips
(function buildTypeChips() {
  const wrap = document.getElementById('typeChips');
  ALL_TYPES.forEach(t => {
    const btn = document.createElement('button');
    btn.className = 'chip'; btn.setAttribute('aria-pressed', 'false');
    btn.textContent = t; btn.dataset.type = t;
    btn.addEventListener('click', () => {
      if (browseState.types.has(t)) browseState.types.delete(t); else browseState.types.add(t);
      btn.setAttribute('aria-pressed', browseState.types.has(t) ? 'true' : 'false');
      renderColleges();
    });
    wrap.appendChild(btn);
  });
})();

// Build branch chips — most common first
(function buildBranchChips() {
  const wrap = document.getElementById('branchChips');
  // Show the top ~16 common branches as chips; others reachable via search-style filter is fine
  const commonOrder = ["CSE","IT","ECE","EEE","EE","Mech","Civil","Chem","AIML","AIDS","Bio","Aero","Auto","MME","Mining","Robot","Arch","EngDes"];
  const shown = commonOrder.filter(b => ALL_BRANCHES.includes(b));
  shown.forEach(b => {
    const btn = document.createElement('button');
    btn.className = 'chip'; btn.setAttribute('aria-pressed', 'false');
    btn.textContent = b + (BRANCH_LABELS[b] ? "" : "");
    btn.title = BRANCH_LABELS[b] || b;
    btn.dataset.branch = b;
    btn.addEventListener('click', () => {
      if (browseState.branches.has(b)) browseState.branches.delete(b); else browseState.branches.add(b);
      btn.setAttribute('aria-pressed', browseState.branches.has(b) ? 'true' : 'false');
      renderColleges();
    });
    wrap.appendChild(btn);
  });
})();

document.getElementById('searchInput').addEventListener('input', (e) => {
  browseState.search = e.target.value.toLowerCase().trim();
  renderColleges();
});
document.getElementById('stateFilter').addEventListener('change', (e) => {
  browseState.state = e.target.value;
  renderColleges();
});
document.getElementById('sortBy').addEventListener('change', (e) => {
  browseState.sort = e.target.value;
  renderColleges();
});
document.getElementById('resetFilters').addEventListener('click', () => {
  browseState.search = ""; browseState.types.clear(); browseState.state = "";
  browseState.branches.clear(); browseState.sort = "rank";
  document.getElementById('searchInput').value = "";
  document.getElementById('stateFilter').value = "";
  document.getElementById('sortBy').value = "rank";
  document.querySelectorAll('#typeChips .chip, #branchChips .chip')
    .forEach(c => c.setAttribute('aria-pressed', 'false'));
  renderColleges();
});

function renderColleges() {
  let list = COLLEGES_DB.slice();

  if (browseState.search) {
    const q = browseState.search;
    list = list.filter(c =>
      c.n.toLowerCase().includes(q) ||
      c.d.toLowerCase().includes(q) ||
      c.s.toLowerCase().includes(q)
    );
  }
  if (browseState.types.size > 0) {
    list = list.filter(c => browseState.types.has(c.t));
  }
  if (browseState.state) {
    list = list.filter(c => c.s === browseState.state);
  }
  if (browseState.branches.size > 0) {
    // AND across selected branches — college must offer all selected branches
    list = list.filter(c => Array.from(browseState.branches).every(b => c.b.includes(b)));
  }

  // Sort
  list.sort((a, b) => {
    if (browseState.sort === "name") return a.n.localeCompare(b.n);
    if (browseState.sort === "state") return a.s.localeCompare(b.s) || a.n.localeCompare(b.n);
    if (browseState.sort === "type") {
      const typeOrder = ["IIT","NIT","IIIT","IoE","Deemed","Central","State","Private"];
      return typeOrder.indexOf(a.t) - typeOrder.indexOf(b.t) || a.n.localeCompare(b.n);
    }
    // default: rank — NIRF ranked first, then by name
    const ra = a.r || 9999, rb = b.r || 9999;
    if (ra !== rb) return ra - rb;
    return a.n.localeCompare(b.n);
  });

  document.getElementById('resultsCount').textContent = list.length;

  const grid = document.getElementById('collegesGrid');
  if (list.length === 0) {
    grid.style.gridTemplateColumns = "1fr";
    grid.innerHTML = "<div class='no-results'><strong>No colleges match your filters</strong>Try removing a filter or searching a different term.</div>";
    return;
  }
  grid.style.gridTemplateColumns = "";

  const html = list.map(c => {
    const tagClass = c.t.toLowerCase();
    // branch-mix bar from cp counts [computer, circuit, mech, process]
    const cpArr = c.cp || [0,0,0,0];
    const cpTotal = cpArr.reduce((a,b)=>a+b,0) || 1;
    const famKeys = ["fc","fk","fm","fp"];
    const famNames = ["Computer","Circuit","Mechanical","Civil & Process"];
    const barHtml = famKeys.map((k,i) => cpArr[i] > 0
      ? "<span class='" + k + "' style='width:" + (cpArr[i]/cpTotal*100) + "%' title='" + famNames[i] + ": " + cpArr[i] + " branches'></span>" : "").join("");
    // dominant family caption
    const domIdx = cpArr.indexOf(Math.max(...cpArr));
    const domShare = cpArr[domIdx]/cpTotal;
    const character = domShare >= 0.5 ? famNames[domIdx] + "-focused" : (Math.max(...cpArr) - (cpArr.slice().sort((a,b)=>b-a)[1]||0) <= 1 ? "Broad-base" : famNames[domIdx] + "-leaning");
    // grouped chips by family
    const groups = [[],[],[],[]];
    c.b.forEach(b => { const f = branchFamilyIdx(b); groups[f].push(b); });
    const groupRows = groups.map((arr,i) => arr.length ? (
      "<div class='bg-row'><span class='bg-dot " + famKeys[i] + "'></span><div class='bg-chips'>" +
      arr.map(b => "<span class='bg-chip" + (browseState.branches.has(b) ? " match" : "") + "' title='" + (BRANCH_LABELS[b] || b) + "'>" + b + "</span>").join("") +
      "</div></div>") : "").join("");
    return "<article class='college-card'>"
         + "<div class='cc-head'>"
           + "<div class='cc-name'>" + c.n + "</div>"
           + "<div class='cc-tags'>"
             + (c.r ? "<span class='cc-tag rank'>NIRF #" + c.r + "</span>" : (c.nb ? "<span class='cc-tag rankband'>NIRF " + c.nb + "</span>" : ""))
             + "<span class='cc-tag " + tagClass + "'>" + c.t + "</span>"
           + "</div>"
         + "</div>"
         + "<div class='cc-loc'>" + c.d + " · " + c.s + "</div>"
         + "<div class='cc-sep'></div>"
         + "<div class='fam-bar'>" + barHtml + "</div>"
         + "<div class='fam-caption'><span class='lead'>" + character + "</span> · " + c.b.length + " branches</div>"
         + "<div class='cc-sep' style='margin:14px -22px'></div>"
         + "<div class='branch-group'>" + groupRows + "</div>"
         + "</article>";
  }).join("");

  grid.innerHTML = html;
}

renderColleges();


// ════════════════════════════════════════════════════════════════
// NIRF section — dual view: compare bars (default) + waffle cards
// ════════════════════════════════════════════════════════════════
const WAFFLE_ITEMS = [
  {name:"IIT Madras",state:"Tamil Nadu",type:"IIT",rank:"#1",rsort:1,computer:0.083,circuit:0.167,mech:0.333,other:0.417},
  {name:"IIT Delhi",state:"Delhi",type:"IIT",rank:"#2",rsort:2,computer:0.1,circuit:0.2,mech:0.2,other:0.5},
  {name:"IIT Bombay",state:"Maharashtra",type:"IIT",rank:"#3",rsort:3,computer:0.091,circuit:0.182,mech:0.273,other:0.455},
  {name:"IIT Kanpur",state:"Uttar Pradesh",type:"IIT",rank:"#4",rsort:4,computer:0.1,circuit:0.2,mech:0.3,other:0.4},
  {name:"IIT Kharagpur",state:"West Bengal",type:"IIT",rank:"#5",rsort:5,computer:0.077,circuit:0.154,mech:0.462,other:0.308},
  {name:"IIT Roorkee",state:"Uttarakhand",type:"IIT",rank:"#6",rsort:6,computer:0.083,circuit:0.167,mech:0.25,other:0.5},
  {name:"IIT Hyderabad",state:"Telangana",type:"IIT",rank:"#7",rsort:7,computer:0.2,circuit:0.2,mech:0.2,other:0.4},
  {name:"IIT Guwahati",state:"Assam",type:"IIT",rank:"#8",rsort:8,computer:0.1,circuit:0.2,mech:0.1,other:0.6},
  {name:"NIT Trichy",state:"Tamil Nadu",type:"NIT",rank:"#9",rsort:9,computer:0.182,circuit:0.182,mech:0.273,other:0.364},
  {name:"IIT BHU Varanasi",state:"Uttar Pradesh",type:"IIT",rank:"#10",rsort:10,computer:0.083,circuit:0.167,mech:0.25,other:0.5},
  {name:"BITS Pilani",state:"Rajasthan",type:"IoE",rank:"#11",rsort:11,computer:0.083,circuit:0.167,mech:0.167,other:0.583},
  {name:"IIT Indore",state:"Madhya Pradesh",type:"IIT",rank:"#12",rsort:12,computer:0.1,circuit:0.2,mech:0.2,other:0.5},
  {name:"NIT Rourkela",state:"Odisha",type:"NIT",rank:"#13",rsort:13,computer:0.091,circuit:0.182,mech:0.273,other:0.455},
  {name:"SRM IST Chennai",state:"Tamil Nadu",type:"Deemed",rank:"#14",rsort:14,computer:0.4,circuit:0.133,mech:0.267,other:0.2},
  {name:"IIT ISM Dhanbad",state:"Jharkhand",type:"IIT",rank:"#15",rsort:15,computer:0.091,circuit:0.182,mech:0.273,other:0.455},
  {name:"VIT Vellore",state:"Tamil Nadu",type:"Deemed",rank:"#16",rsort:16,computer:0.357,circuit:0.143,mech:0.286,other:0.214},
  {name:"NIT Surathkal",state:"Karnataka",type:"NIT",rank:"#17",rsort:17,computer:0.273,circuit:0.273,mech:0.273,other:0.182},
  {name:"Jadavpur University",state:"West Bengal",type:"IoE",rank:"#18",rsort:18,computer:0.167,circuit:0.167,mech:0.25,other:0.417},
  {name:"IIT Patna",state:"Bihar",type:"IIT",rank:"#19",rsort:19,computer:0.143,circuit:0.286,mech:0.286,other:0.286},
  {name:"Anna University CEG",state:"Tamil Nadu",type:"State",rank:"#20",rsort:20,computer:0.111,circuit:0.111,mech:0.278,other:0.5},
  {name:"NIT Calicut",state:"Kerala",type:"NIT",rank:"#21",rsort:21,computer:0.1,circuit:0.2,mech:0.3,other:0.4},
  {name:"Amrita Coimbatore",state:"Tamil Nadu",type:"Deemed",rank:"#23",rsort:23,computer:0.333,circuit:0.167,mech:0.25,other:0.25},
  {name:"Jamia Millia Islamia",state:"Delhi",type:"Central",rank:"#24",rsort:24,computer:0.286,circuit:0.286,mech:0.143,other:0.286},
  {name:"IIT Gandhinagar",state:"Gujarat",type:"IIT",rank:"#25",rsort:25,computer:0.125,circuit:0.25,mech:0.25,other:0.375},
  {name:"IIT Mandi",state:"Himachal Pradesh",type:"IIT",rank:"#26",rsort:26,computer:0.286,circuit:0.286,mech:0.143,other:0.286},
  {name:"IIT Jodhpur",state:"Rajasthan",type:"IIT",rank:"#27",rsort:27,computer:0.222,circuit:0.222,mech:0.222,other:0.333},
  {name:"NIT Warangal",state:"Telangana",type:"NIT",rank:"#28",rsort:28,computer:0.125,circuit:0.25,mech:0.25,other:0.375},
  {name:"Thapar Institute",state:"Punjab",type:"Deemed",rank:"#29",rsort:29,computer:0.2,circuit:0.2,mech:0.3,other:0.3},
  {name:"DTU (Delhi Tech Univ)",state:"Delhi",type:"State",rank:"#30",rsort:30,computer:0.214,circuit:0.143,mech:0.143,other:0.5},
  {name:"Chandigarh University",state:"Punjab",type:"Private",rank:"#31",rsort:31,computer:0.3,circuit:0.2,mech:0.3,other:0.2},
  {name:"IIT Ropar",state:"Punjab",type:"IIT",rank:"#32",rsort:32,computer:0.222,circuit:0.222,mech:0.222,other:0.333},
  {name:"K L University (KLU)",state:"Andhra Pradesh",type:"Deemed",rank:"#35",rsort:35,computer:0.444,circuit:0.222,mech:0.111,other:0.222},
  {name:"KIIT Bhubaneswar",state:"Odisha",type:"IoE",rank:"#36",rsort:36,computer:0.364,circuit:0.182,mech:0.273,other:0.182},
  {name:"Amity University Noida",state:"Uttar Pradesh",type:"Private",rank:"#37",rsort:37,computer:0.273,circuit:0.182,mech:0.364,other:0.182},
  {name:"IIIT Hyderabad",state:"Telangana",type:"IIIT",rank:"#38",rsort:38,computer:0.667,circuit:0.167,mech:0.0,other:0.167},
  {name:"IIT Bhubaneswar",state:"Odisha",type:"IIT",rank:"#39",rsort:39,computer:0.125,circuit:0.25,mech:0.375,other:0.25},
  {name:"SASTRA University",state:"Tamil Nadu",type:"Deemed",rank:"#40",rsort:40,computer:0.273,circuit:0.182,mech:0.182,other:0.364},
  {name:"ICT Mumbai",state:"Maharashtra",type:"Deemed",rank:"#41",rsort:41,computer:0.0,circuit:0.0,mech:0.0,other:1.0},
  {name:"MNIT Jaipur",state:"Rajasthan",type:"NIT",rank:"#42",rsort:42,computer:0.125,circuit:0.25,mech:0.25,other:0.375},
  {name:"VNIT Nagpur",state:"Maharashtra",type:"NIT",rank:"#44",rsort:44,computer:0.111,circuit:0.222,mech:0.333,other:0.333},
  {name:"Symbiosis Inst of Tech",state:"Maharashtra",type:"Deemed",rank:"#46",rsort:46,computer:0.286,circuit:0.286,mech:0.286,other:0.143},
  {name:"SSN College of Engg",state:"Tamil Nadu",type:"Private",rank:"#47",rsort:47,computer:0.25,circuit:0.25,mech:0.125,other:0.375},
  {name:"LPU Phagwara",state:"Punjab",type:"Private",rank:"#48",rsort:48,computer:0.25,circuit:0.167,mech:0.25,other:0.333},
  {name:"NIT Durgapur",state:"West Bengal",type:"NIT",rank:"#49",rsort:49,computer:0.222,circuit:0.222,mech:0.222,other:0.333},
  {name:"NIT Silchar",state:"Assam",type:"NIT",rank:"#50",rsort:50,computer:0.167,circuit:0.5,mech:0.167,other:0.167},
  {name:"BIT Mesra",state:"Jharkhand",type:"Deemed",rank:"#51",rsort:51,computer:0.182,circuit:0.182,mech:0.091,other:0.545},
  {name:"NIT Patna",state:"Bihar",type:"NIT",rank:"#53",rsort:53,computer:0.167,circuit:0.333,mech:0.167,other:0.333},
  {name:"IIEST Shibpur",state:"West Bengal",type:"Central",rank:"#54",rsort:54,computer:0.167,circuit:0.167,mech:0.333,other:0.333},
  {name:"NIT Jalandhar",state:"Punjab",type:"NIT",rank:"#55",rsort:55,computer:0.222,circuit:0.222,mech:0.111,other:0.444},
  {name:"IIT Jammu",state:"Jammu and Kashmir",type:"IIT",rank:"#56",rsort:56,computer:0.143,circuit:0.286,mech:0.286,other:0.286},
  {name:"IIT Tirupati",state:"Andhra Pradesh",type:"IIT",rank:"#57",rsort:57,computer:0.167,circuit:0.333,mech:0.167,other:0.333},
  {name:"Manipal Univ Jaipur",state:"Rajasthan",type:"Deemed",rank:"#58",rsort:58,computer:0.273,circuit:0.182,mech:0.273,other:0.273},
  {name:"MAHE Manipal",state:"Karnataka",type:"IoE",rank:"#59",rsort:59,computer:0.25,circuit:0.167,mech:0.333,other:0.25},
  {name:"MMMUT Gorakhpur",state:"Uttar Pradesh",type:"State",rank:"#60",rsort:60,computer:0.25,circuit:0.25,mech:0.25,other:0.25},
  {name:"MNNIT Allahabad",state:"Uttar Pradesh",type:"NIT",rank:"#62",rsort:62,computer:0.125,circuit:0.25,mech:0.25,other:0.375},
  {name:"MNNIT (also listed)",state:"Uttar Pradesh",type:"State",rank:"#62",rsort:62,computer:0.143,circuit:0.286,mech:0.143,other:0.429},
  {name:"IIIT Delhi",state:"Delhi",type:"IIIT",rank:"#63",rsort:63,computer:0.857,circuit:0.143,mech:0.0,other:0.0},
  {name:"IIT Palakkad",state:"Kerala",type:"IIT",rank:"#64",rsort:64,computer:0.333,circuit:0.333,mech:0.167,other:0.167},
  {name:"NIT Delhi",state:"Delhi",type:"NIT",rank:"#65",rsort:65,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"SVNIT Surat",state:"Gujarat",type:"NIT",rank:"#66",rsort:66,computer:0.286,circuit:0.286,mech:0.143,other:0.286},
  {name:"PSG Coimbatore",state:"Tamil Nadu",type:"Private",rank:"#67",rsort:67,computer:0.231,circuit:0.154,mech:0.385,other:0.231},
  {name:"IIIT Bangalore",state:"Karnataka",type:"IIIT",rank:"#69",rsort:69,computer:0.5,circuit:0.5,mech:0.0,other:0.0},
  {name:"IIIT-Bangalore",state:"Karnataka",type:"Deemed",rank:"#69",rsort:69,computer:0.333,circuit:0.667,mech:0.0,other:0.0},
  {name:"NSUT Dwarka",state:"Delhi",type:"State",rank:"#70",rsort:70,computer:0.333,circuit:0.222,mech:0.111,other:0.333},
  {name:"IIT Bhilai",state:"Chhattisgarh",type:"IIT",rank:"#72",rsort:72,computer:0.333,circuit:0.333,mech:0.167,other:0.167},
  {name:"NIT Srinagar",state:"Jammu and Kashmir",type:"NIT",rank:"#73",rsort:73,computer:0.25,circuit:0.25,mech:0.25,other:0.25},
  {name:"MS Ramaiah Inst of Tech",state:"Karnataka",type:"Private",rank:"#75",rsort:75,computer:0.3,circuit:0.2,mech:0.2,other:0.3},
  {name:"IIT Dharwad",state:"Karnataka",type:"IIT",rank:"#77",rsort:77,computer:0.167,circuit:0.333,mech:0.167,other:0.333},
  {name:"MANIT Bhopal",state:"Madhya Pradesh",type:"NIT",rank:"#81",rsort:81,computer:0.125,circuit:0.25,mech:0.25,other:0.375},
  {name:"NIT Jamshedpur",state:"Jharkhand",type:"NIT",rank:"#82",rsort:82,computer:0.125,circuit:0.375,mech:0.375,other:0.125},
  {name:"NIT Meghalaya",state:"Meghalaya",type:"NIT",rank:"#83",rsort:83,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"NIT Kurukshetra",state:"Haryana",type:"NIT",rank:"#85",rsort:85,computer:0.286,circuit:0.286,mech:0.286,other:0.143},
  {name:"NIT Raipur",state:"Chhattisgarh",type:"NIT",rank:"#86",rsort:86,computer:0.182,circuit:0.182,mech:0.273,other:0.364},
  {name:"Andhra Univ CoE",state:"Andhra Pradesh",type:"State",rank:"#88",rsort:88,computer:0.182,circuit:0.182,mech:0.273,other:0.364},
  {name:"Chitkara University",state:"Punjab",type:"Private",rank:"#89",rsort:89,computer:0.333,circuit:0.333,mech:0.167,other:0.167},
  {name:"COEP Pune",state:"Maharashtra",type:"State",rank:"#90",rsort:90,computer:0.2,circuit:0.2,mech:0.3,other:0.3},
  {name:"JNTU Hyderabad (UCE)",state:"Telangana",type:"State",rank:"#94",rsort:94,computer:0.273,circuit:0.182,mech:0.364,other:0.182},
  {name:"NIT Hamirpur",state:"Himachal Pradesh",type:"NIT",rank:"#97",rsort:97,computer:0.125,circuit:0.25,mech:0.25,other:0.375},
  {name:"PDPU Gandhinagar",state:"Gujarat",type:"State",rank:"#98",rsort:98,computer:0.25,circuit:0.25,mech:0.125,other:0.375},
  {name:"NIT Puducherry",state:"Puducherry",type:"NIT",rank:"#99",rsort:99,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"IIT Goa",state:"Goa",type:"IIT",rank:"101-150",rsort:125,computer:0.167,circuit:0.333,mech:0.333,other:0.167},
  {name:"NIT Agartala",state:"Tripura",type:"NIT",rank:"101-150",rsort:125,computer:0.167,circuit:0.333,mech:0.333,other:0.167},
  {name:"NIT Goa",state:"Goa",type:"NIT",rank:"101-150",rsort:125,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"NIT Mizoram",state:"Mizoram",type:"NIT",rank:"101-150",rsort:125,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"NIT Nagaland",state:"Nagaland",type:"NIT",rank:"101-150",rsort:125,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"NIT Arunachal Pradesh",state:"Arunachal Pradesh",type:"NIT",rank:"101-150",rsort:125,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"IIIT Allahabad",state:"Uttar Pradesh",type:"IIIT",rank:"101-150",rsort:125,computer:0.667,circuit:0.0,mech:0.0,other:0.333},
  {name:"IIIT-DM Jabalpur",state:"Madhya Pradesh",type:"IIIT",rank:"101-150",rsort:125,computer:0.25,circuit:0.25,mech:0.25,other:0.25},
  {name:"Nirma University",state:"Gujarat",type:"Deemed",rank:"101-150",rsort:125,computer:0.222,circuit:0.222,mech:0.333,other:0.222},
  {name:"VJTI Mumbai",state:"Maharashtra",type:"State",rank:"101-150",rsort:125,computer:0.222,circuit:0.222,mech:0.222,other:0.333},
  {name:"Osmania Univ CoE",state:"Telangana",type:"State",rank:"101-150",rsort:125,computer:0.333,circuit:0.222,mech:0.111,other:0.333},
  {name:"Univ College of Engg Trivandrum",state:"Kerala",type:"State",rank:"101-150",rsort:125,computer:0.25,circuit:0.25,mech:0.125,other:0.375},
  {name:"Thiagarajar College of Engg",state:"Tamil Nadu",type:"Private",rank:"101-150",rsort:125,computer:0.375,circuit:0.25,mech:0.25,other:0.125},
  {name:"Coimbatore Inst of Technology",state:"Tamil Nadu",type:"Private",rank:"101-150",rsort:125,computer:0.429,circuit:0.286,mech:0.143,other:0.143},
  {name:"Karunya Institute",state:"Tamil Nadu",type:"Deemed",rank:"101-150",rsort:125,computer:0.3,circuit:0.2,mech:0.2,other:0.3},
  {name:"Easwari Engineering College",state:"Tamil Nadu",type:"Private",rank:"101-150",rsort:125,computer:0.5,circuit:0.25,mech:0.125,other:0.125},
  {name:"Rajalakshmi Engineering College",state:"Tamil Nadu",type:"Private",rank:"101-150",rsort:125,computer:0.5,circuit:0.25,mech:0.125,other:0.125},
  {name:"RV College of Engineering",state:"Karnataka",type:"Private",rank:"101-150",rsort:125,computer:0.273,circuit:0.182,mech:0.182,other:0.364},
  {name:"PES University",state:"Karnataka",type:"Private",rank:"101-150",rsort:125,computer:0.286,circuit:0.286,mech:0.143,other:0.286},
  {name:"GITAM Visakhapatnam",state:"Andhra Pradesh",type:"Deemed",rank:"101-150",rsort:125,computer:0.333,circuit:0.222,mech:0.111,other:0.333},
  {name:"MIT WPU Pune",state:"Maharashtra",type:"Deemed",rank:"101-150",rsort:125,computer:0.2,circuit:0.2,mech:0.4,other:0.2},
  {name:"CET Trivandrum",state:"Kerala",type:"State",rank:"101-150",rsort:125,computer:0.25,circuit:0.25,mech:0.125,other:0.375},
  {name:"NIT Uttarakhand",state:"Uttarakhand",type:"NIT",rank:"151-200",rsort:175,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"NIT Sikkim",state:"Sikkim",type:"NIT",rank:"151-200",rsort:175,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"NIT Manipur",state:"Manipur",type:"NIT",rank:"151-200",rsort:175,computer:0.2,circuit:0.4,mech:0.2,other:0.2},
  {name:"Kumaraguru College of Tech",state:"Tamil Nadu",type:"Private",rank:"151-200",rsort:175,computer:0.333,circuit:0.222,mech:0.333,other:0.111},
  {name:"BMS College of Engineering",state:"Karnataka",type:"Private",rank:"151-200",rsort:175,computer:0.333,circuit:0.222,mech:0.222,other:0.222},
  {name:"KLE Tech University",state:"Karnataka",type:"Deemed",rank:"151-200",rsort:175,computer:0.167,circuit:0.333,mech:0.333,other:0.167},
  {name:"VNR VJIET Hyderabad",state:"Telangana",type:"Private",rank:"151-200",rsort:175,computer:0.375,circuit:0.25,mech:0.25,other:0.125},
  {name:"CBIT Hyderabad",state:"Telangana",type:"Private",rank:"151-200",rsort:175,computer:0.375,circuit:0.25,mech:0.125,other:0.25},
  {name:"NIT Andhra Pradesh",state:"Andhra Pradesh",type:"NIT",rank:"201-300",rsort:250,computer:0.143,circuit:0.286,mech:0.286,other:0.286},
  {name:"DAIICT Gandhinagar",state:"Gujarat",type:"Deemed",rank:"201-300",rsort:250,computer:0.75,circuit:0.0,mech:0.0,other:0.25},
  {name:"LNMIIT Jaipur",state:"Rajasthan",type:"Private",rank:"201-300",rsort:250,computer:0.2,circuit:0.2,mech:0.4,other:0.2},
  {name:"Sri Venkateswara CoE",state:"Tamil Nadu",type:"Private",rank:"201-300",rsort:250,computer:0.375,circuit:0.25,mech:0.125,other:0.25},
  {name:"Dayananda Sagar Univ",state:"Karnataka",type:"Private",rank:"201-300",rsort:250,computer:0.333,circuit:0.222,mech:0.222,other:0.222},
  {name:"JSS Tech University",state:"Karnataka",type:"Deemed",rank:"201-300",rsort:250,computer:0.286,circuit:0.286,mech:0.143,other:0.286},
  {name:"GNITS Hyderabad",state:"Telangana",type:"Private",rank:"201-300",rsort:250,computer:0.5,circuit:0.333,mech:0.167,other:0.0},
  {name:"HBTU Kanpur",state:"Uttar Pradesh",type:"State",rank:"201-300",rsort:250,computer:0.154,circuit:0.154,mech:0.077,other:0.615},
  {name:"JSS Academy of Tech",state:"Uttar Pradesh",type:"Private",rank:"201-300",rsort:250,computer:0.286,circuit:0.286,mech:0.143,other:0.286},
  {name:"M.S. University Baroda",state:"Gujarat",type:"State",rank:"201-300",rsort:250,computer:0.182,circuit:0.182,mech:0.182,other:0.455},
];

const FAM = [
  { key:"computer", cls:"fc", label:"Computer" },
  { key:"circuit",  cls:"fk", label:"Circuit" },
  { key:"mech",     cls:"fm", label:"Mechanical" },
  { key:"other",    cls:"fp", label:"Civil & Process" },
];

// attach branch counts to each item (from proportions × an assumed scale is lossy;
// instead recompute counts from COLLEGES_DB by name for accuracy)
const _dbByName = {};
COLLEGES_DB.forEach(c => { _dbByName[c.n] = c; });
WAFFLE_ITEMS.forEach(it => {
  const db = _dbByName[it.name];
  it.counts = db && db.cp ? db.cp.slice() : [
    Math.round(it.computer*10), Math.round(it.circuit*10), Math.round(it.mech*10), Math.round(it.other*10)
  ];
  it.nbranches = it.counts.reduce((a,b)=>a+b,0);
});

let nQuery = "", nSort = "rank", nView = "bars";

function nFilterSort(){
  let list = WAFFLE_ITEMS.filter(it => (it.name + " " + it.state).toLowerCase().includes(nQuery.toLowerCase()));
  list.sort((a,b)=>{
    if(nSort==="computer") return b.computer - a.computer;
    if(nSort==="core") return (b.mech+b.other) - (a.mech+a.other);
    if(nSort==="branches") return b.nbranches - a.nbranches;
    if(nSort==="name") return a.name.localeCompare(b.name);
    return a.rsort - b.rsort;
  });
  return list;
}

// ── Compare-bar row ──
function renderBars(){
  const wrap = document.getElementById('cmpList');
  if(!wrap) return;
  const list = nFilterSort();
  if(!list.length){ wrap.innerHTML = '<div class="waffle-empty">No ranked colleges match your search.</div>'; return; }
  wrap.innerHTML = list.map(it => {
    const total = it.counts.reduce((a,b)=>a+b,0) || 1;
    const segs = FAM.map((f,i) => it.counts[i] > 0
      ? '<span class="'+f.cls+'" style="width:'+(it.counts[i]/total*100)+'%" title="'+f.label+': '+it.counts[i]+'"></span>' : '').join('');
    const isExact = it.rank.charAt(0) === "#";
    const rankHtml = isExact
      ? '<div class="cmp-rank"><span class="star">★</span> '+it.rank.slice(1)+'</div>'
      : '<div class="cmp-rank band">'+it.rank+'</div>';
    return '<div class="cmp-row">'
      + rankHtml
      + '<div class="cmp-name"><span class="nm">'+it.name+'</span><span class="mt">'+it.state+' · '+it.type+'</span></div>'
      + '<div class="cmp-bar" role="img" aria-label="'+it.name+' branch mix">'+segs+'</div>'
      + '<div class="cmp-count">'+it.nbranches+'<span>branches</span></div>'
      + '</div>';
  }).join("");
}

// ── Waffle cards (refined) ──
const W_CELLS = 50;
function wBuild(it){
  const vals = [it.computer, it.circuit, it.mech, it.other];
  let counts = vals.map(v => Math.round(v * W_CELLS));
  let sum = counts.reduce((a,b)=>a+b,0);
  while(sum > W_CELLS){ const i = counts.indexOf(Math.max(...counts)); counts[i]--; sum--; }
  const colors = ["var(--navy)","var(--orange)","var(--green)","var(--amber)"];
  const cells = [];
  counts.forEach((n,i)=>{ for(let k=0;k<n;k++) cells.push(colors[i]); });
  for(let k=0;k<W_CELLS-sum;k++) cells.push("var(--hairline)");
  return cells;
}
function renderWafflesView(){
  const grid = document.getElementById('waffleView');
  if(!grid) return;
  const list = nFilterSort();
  if(!list.length){ grid.innerHTML = '<div class="waffle-empty">No ranked colleges match your search.</div>'; return; }
  grid.innerHTML = list.map(it => {
    const cells = wBuild(it).map(c => '<div class="wcell" style="background:'+c+'"></div>').join("");
    const tip = "Computer "+Math.round(it.computer*100)+"% · Circuit "+Math.round(it.circuit*100)+"% · Mech "+Math.round(it.mech*100)+"% · Civil/Process "+Math.round(it.other*100)+"%";
    const badge = it.rank.charAt(0)==="#"
      ? '<span class="nirf-badge">NIRF '+it.rank+'</span>'
      : '<span class="nirf-badge band">NIRF '+it.rank+'</span>';
    return '<article class="waffle-card">'
      + '<div class="wc-head"><h3>'+it.name+'</h3>'+badge+'</div>'
      + '<div class="wc-sub">'+it.state+' · '+it.type+'</div>'
      + '<div class="waffle" role="img" aria-label="'+it.name+'. '+tip+'" title="'+tip+'">'+cells+'</div>'
      + '<div class="wc-metric"><span>'+it.nbranches+' branches</span><span class="wt">'+it.type+'</span></div>'
      + '</article>';
  }).join("");
}

function renderNirf(){ if(nView==="bars") renderBars(); else renderWafflesView(); }

(function(){
  const s = document.getElementById('nirfSearch'), so = document.getElementById('nirfSort');
  const vb = document.getElementById('viewBars'), vw = document.getElementById('viewWaffle');
  const cmpView = document.getElementById('cmpView'), waffleView = document.getElementById('waffleView');
  if(s) s.addEventListener('input', e=>{ nQuery=e.target.value; renderNirf(); });
  if(so) so.addEventListener('change', e=>{ nSort=e.target.value; renderNirf(); });
  if(vb) vb.addEventListener('click', ()=>{ nView="bars"; vb.setAttribute('aria-pressed','true'); vw.setAttribute('aria-pressed','false'); cmpView.style.display=''; waffleView.style.display='none'; renderNirf(); });
  if(vw) vw.addEventListener('click', ()=>{ nView="waffle"; vw.setAttribute('aria-pressed','true'); vb.setAttribute('aria-pressed','false'); cmpView.style.display='none'; waffleView.style.display='grid'; renderNirf(); });
  renderNirf();
})();


;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z91qpH' }, '*');
	});

	heightObserver.observe(document.documentElement);
