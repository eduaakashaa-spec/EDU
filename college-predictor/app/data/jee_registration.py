"""Content of the JEE Main 2027 registration page (/jee-main-2027-registration), from the EduAakashaA JEE Main 2027 NRI Registration Guide of 31 October 2026.

Official rules come from NTA's JEE (Main) 2027 Information Bulletin and the Session 1 public notice. Items tagged 'peer' are what other families reported in the EduAakashaA Members Group:
useful, but not NTA rules. 'disputed' means families disagreed; 'open' means unanswered. The page never names a family or a child. Re-check every rule on jeemain.nta.nic.in.
"""
UPDATED = '31 October 2026'
NTA = 'jeemain.nta.nic.in'
HELPLINE = '011-40759000 or 011-69227700'
HELP_EMAIL = 'jeemain@nta.ac.in'

TAGS = {'official': 'Official source', 'peer': 'Reported by families', 'disputed': 'Disputed', 'open': 'Unanswered'}

SESSIONS = [
    {'name': 'Session 1 · January 2027', 'rows': [
        ('24 Oct to 22 Nov', 'Apply and pay, until 11:50 pm IST'), ('23 to 26 Nov', 'Late window, extra ₹500 for all'), ('27 to 29 Nov', 'Correction window'),
        ('30 Dec', 'Exam city slip'), ('13 Jan', 'Admit card download'), ('20 to 24 and 28 Jan', 'Exam days')]},
    {'name': 'Session 2 · April 2027', 'rows': [
        ('5 Jan to 3 Feb', 'Apply and pay, with the same application number'), ('4 to 7 Feb', 'Late window'), ('8 to 10 Feb', 'Correction window'),
        ('12 Mar', 'Exam city slip'), ('25 Mar', 'Admit card download'), ('2 to 7 Apr', 'Exam days')]},
]
TIMING = ('Papers run 3 hours in two shifts: 9:00 am to 12:00 pm and 3:00 pm to 6:00 pm IST. Applying for B.Arch and B.Planning together takes 3 hours 30 minutes. '
          'Candidates who may use a scribe get 4 hours (4 h 40 min for the combined paper). Every NTA time is in IST: work out your own offset before you plan travel or an early shift.')

ELIGIBILITY = [
    ('Class 12 year', 'Passed in 2025 or 2026, or appearing in 2027. Passed in 2024 or earlier: not eligible. No age limit.'),
    ('Boards accepted', 'CBSE, CISCE, state boards, NIOS (five subjects), Cambridge A-levels, IB Diploma and others on NTA\'s list.'),
    ('Board outside India', 'An Association of Indian Universities (AIU) equivalence certificate is required if the board is not on NTA\'s list.'),
    ('State of eligibility', 'The state of the Class 12 institution, not the home address. NIOS: the study centre\'s state.'),
    ('One form only', 'Under no circumstances may a candidate fill more than one form. Strict action can follow, even later.'),
    ('Both sessions', 'The best NTA score across the sessions counts. Session 2 is applied for separately, using the same application number.'),
]

DOCS = [
    ('Photograph', 'JPG, 10 to 200 KB', 'Captured live on the form, by webcam or by phone with the QR code. White background, face about 80% of the frame with both ears visible, good light. Do not edit it: background removers can erase the ears.'),
    ('Signature', 'JPG, 10 to 100 KB', 'Signed on plain white paper, cropped tightly.'),
    ('Class 10 certificate', 'PDF, 50 to 300 KB', 'Name and date of birth must match your identity record exactly.'),
    ('Disability certificate or UDID', 'PDF, 50 to 300 KB', 'Only if you claim PwD.'),
    ('Non-Indian passport', 'PDF, 50 to 300 KB', 'Only for foreign nationals, including OCI.'),
]
IDENTITY = [
    ('Identity verification', 'Sign in through MeriPehchaan using your own DigiLocker, JanParichay or e-Pramaan credentials. eKYC works through Aadhaar, PAN, driving licence or APAAR. Complete DigiLocker Re-KYC before you start.'),
    ('Phone and email', 'One mobile number and one email per application, and they must be the candidate\'s or a parent or guardian\'s. Every OTP and recovery message goes there.'),
    ('Password and medium', 'Password of 8 to 13 characters with upper case, lower case, a digit and one special character (! @ # $ % ^ & * -). The medium is locked once the correction window closes; at centres outside India, English is the only medium.'),
    ('Category certificate', 'EWS and OBC-NCL: issued on or after 1 April 2026. OBC must be on the Central list.'),
]

STEPS = [
    ('Prepare', 'Collect every file in the checklist. Fix name or date mismatches first.'),
    ('DigiLocker', 'Create or open the account, complete Re-KYC, fetch Aadhaar or PAN into issued documents.'),
    ('Official portal', 'Open jeemain.nta.nic.in and follow its link to sign-in. Copycat sites exist.'),
    ('Verify and create account', 'Sign in, enter your own phone and email, verify the OTPs, set the password.'),
    ('Personal details', 'Name, date of birth, parents, state, category, paper, medium, addresses, four cities.'),
    ('Uploads and live photo', 'Signature and certificates, then the live photograph. Preview each file.'),
    ('Review and pay', 'Read every field twice, then pay online and wait for the success message.'),
    ('Save', 'Download the confirmation page. Note the application number and password separately.'),
]
PAYMENT = [
    ('How', 'Net banking, credit card, debit card or UPI. Bank or gateway processing charges and GST are extra.'),
    ('Confirmation', 'The confirmation page appears only after a successful payment. A bank deduction alone proves nothing.'),
    ('If it fails', 'Contact the bank or payment gateway named in the bulletin. Refunds are only for failed or duplicate transactions.'),
    ('Corrections', 'Only certain fields can change in the correction window. Requests by post, messaging apps or email are not accepted.'),
]
PATTERN = ('Paper 1 has 75 questions (25 each in Physics, Chemistry and Mathematics): 20 multiple-choice and 5 numerical per subject. Correct answer +4, wrong answer −1, unattempted 0. '
           'Numerical answers are rounded to the nearest integer.')

FEES_HEAD = ('Centre in India', 'Centre outside India')
FEES = [
    ('General · male', '₹1,000', '₹5,000'), ('General · female', '₹800', '₹4,000'), ('EWS / OBC-NCL · male', '₹900', '₹4,500'),
    ('EWS / OBC-NCL · female', '₹800', '₹4,000'), ('SC / ST / PwD', '₹500', '₹2,500'),
]
FEES_NOTE = ('One paper, per session, before bank charges and GST. Two papers (B.E./B.Tech plus B.Arch or B.Planning): General, EWS and OBC-NCL pay ₹2,000 male or ₹1,600 female in India and ₹10,000 or ₹8,000 abroad. '
             'SC, ST, PwD and third gender pay ₹1,000 in India and ₹5,000 abroad. Late fee: ₹500 for everyone.')
BUDGET = 'A General male candidate at a centre abroad pays ₹5,000 per session, so ₹10,000 for both sessions, plus bank charges and GST each time. Keep the payment method ready before you start.'

CITIES = [
    ('The rule', 'tag-official', 'Choose up to four cities in order of priority. If your present or permanent address is outside India, at least one city in India is compulsory. NTA may allot a different city for administrative reasons, and its decision is final.'),
    ('Cities abroad in the bulletin', 'tag-official', 'Manama, Kuwait City, Muscat, Doha, Riyadh and Kathmandu, plus further cities in the region. Check the live list on the portal. Where a country has one centre, families asked for more; additions this year looked doubtful.'),
    ('What families did', 'tag-peer', 'Present address in the country of residence, permanent address in India, home-country city first and Indian cities for the other choices. The country of the present address decides which foreign cities appear, and it cannot be changed after OTP verification.'),
]

NATIONALITY = [
    ('Nationality field', 'Indian national (this includes NRI), foreign national or OCI. One family chose wrongly and found no fix, so read the options before submitting.', 'official'),
    ('Passport as sign-in', 'Indian citizens sign in through DigiLocker-based identity. Families report that passport sign-in, used last year, was not offered this year; on 29 October it was still open.', 'peer'),
    ('Foreign nationals and OCI', 'Upload a non-Indian passport (PDF, 50 to 300 KB).', 'official'),
    ('OCI who passed Class 12 abroad', 'Eligible for All India quota seats in NITs, IIITs and other centrally funded institutes, but not Home State quota seats.', 'official'),
    ('OCI who passed Class 12 in India', 'Treated like Indian nationals for state of eligibility.', 'official'),
    ('Board from abroad', 'Get an AIU equivalence certificate if the board is not on NTA\'s list.', 'official'),
    ('Birth place', 'Families entered the country of birth for a child born abroad.', 'peer'),
    ('Class 10 passed abroad', 'Selecting the country reveals different fields. Enter the roll number from the Class 10 marksheet.', 'peer'),
]
AADHAAR = [
    ('Mobile', 'The Aadhaar OTP goes to the Indian number linked to Aadhaar. It must be active, with roaming if you are abroad.'),
    ('Photo and biometrics', 'Updates need the child present at an Aadhaar centre in India. Only the address can be changed online.'),
    ('Live photo', 'An old childhood photo may not match the live photo. Families report a declaration email, not automatic rejection.'),
]
AADHAAR_NOTE = 'Plan an India visit early if the Aadhaar mobile is dead or the photo is from before age 15. Do not leave this to the last week of the window.'

AFTER = [
    ('A', 'JEE Main', 'Session 1 in January, Session 2 in April 2027. Best score counts.'),
    ('B', 'Class 12 result', 'Eligibility for admission, with the 75% aggregate families quote.'),
    ('C', 'Counselling', 'DASA, JoSAA or CSAB, around July per families. Rank decides the seat.'),
    ('D', 'Reporting', 'Documents and fees are submitted online at the admission stage.'),
]
GATES = [
    ('JEE Main registration', 'NTA rules above. One form, DigiLocker-based identity, four city choices. A category certificate number is typed, not uploaded.'),
    ('DASA / CIWG', 'Allotment is by JEE Main rank. Class 12 marks (75% aggregate, per families) are an eligibility condition, not the ranking basis. Documents are uploaded later during online reporting.'),
    ('CIWG backup', 'A CIWG-eligible student can also apply for non-CIWG by paying the additional amount. Non-CIWG tuition is higher, and payment does not guarantee a seat.'),
    ('JoSAA / CSAB', 'Category benefits (OBC-NCL, EWS) matter here. Gulf-schooled students are treated as All India or Other State, not Home State, per families.'),
    ('NRI certificate', 'Families concluded it is not needed for registration, DASA allotment, JoSAA or CSAB. Direct NRI-quota seats in private colleges may ask for one.'),
]
AFTER_NOTE = 'These are family summaries, not NTA rules. Read the current DASA, CIWG and JoSAA brochures before you act, because rules move year to year.'

TOPICS = [
    'Identity (DigiLocker, Aadhaar, passport) is the main worry, more than the exam itself.', 'Category and certificates, including OBC-NCL for families in the Gulf.',
    'Eligibility questions: NRI, OCI, CIWG and DASA.', 'Exam cities and centres abroad.', 'Login, OTP and account problems from overseas numbers.',
    'Dates and deadlines, and photo, signature and upload problems.', 'Duplicate forms and corrections.', 'Fees and payment.',
]

# ---- FAQ ---------------------------------------------------------------------------------------------------------------------------------------------
# (id, tag, question, answer)
FAQ = [
    {'key': 'identity', 'title': 'Signing in with DigiLocker and Aadhaar', 'check': [
        'The eKYC options are Aadhaar, PAN, driving licence and APAAR. A non-Indian passport upload applies only to foreign nationals and OCI candidates.',
        'NTA asks for your own DigiLocker, JanParichay or e-Pramaan credentials and DigiLocker Re-KYC in advance.',
        'A PAN route is untested by families, and minors get no photo on PAN. Plan an India visit if you can.'], 'qs': [
        (1, 'peer', 'Can my child still register with a passport, as in earlier years?', 'Families who tried this week saw only DigiLocker-based sign-in with Aadhaar, PAN, driving licence or APAAR. Passport sign-in, available last year, was not offered. Families wrote to the agency, which reportedly said it was working on it.'),
        (2, 'disputed', 'Is a DigiLocker account really compulsory?', 'First replies said no. Families who then tried found sign-in runs through DigiLocker (or JanParichay or e-Pramaan), so an account is needed.'),
        (3, 'peer', 'Whose phone gets the Aadhaar OTP, the child\'s or a parent\'s?', 'The Indian number linked to the child\'s Aadhaar. It must be active, with international roaming if the family is abroad. One parent opened DigiLocker from the Gulf this way.'),
        (4, 'peer', 'Can we change the Aadhaar mobile number or photo from abroad?', 'No, families said. Mobile, photo and biometric updates need the person present at an Aadhaar centre in India. Only the address can be changed online.'),
        (5, 'disputed', 'The Aadhaar-linked mobile is dead. Is there any other way in?', 'Reported routes: update the number in India, or get a PAN card online and sign in with it, with APAAR as another option. One alternative sign-in worked for some families and bounced others back to DigiLocker.'),
        (6, 'peer', 'Does a scanned Aadhaar saved in the DigiLocker drive count?', 'No. Documents must be fetched as issued documents. If the consent step says document not found, log in to DigiLocker, fetch the document first, then give consent.')]},
    {'key': 'portal', 'title': 'Sign-in problems, OTP and the portal', 'check': [
        'Use jeemain.nta.nic.in only. Copycat sites exist.',
        'The mobile number and email must be the candidate\'s or a parent or guardian\'s, and one set per application.',
        'Session 2 is applied for separately with the same application number and a separate fee.'], 'qs': [
        (7, 'peer', 'Do we need the parent\'s DigiLocker as well?', 'Only the candidate\'s own DigiLocker is needed. Parent documents are not required.'),
        (8, 'peer', 'The e-Pramaan page will not open from a link. What now?', 'Start at the official exam site and click through; the sign-in page then opens by itself. Do not use direct links.'),
        (9, 'peer', 'The OTP never arrives by SMS on our overseas number.', 'The same OTP also goes to the registered email. Check the inbox and spam folder. Families said the email OTP verified both the mobile number and the emergency contact.'),
        (10, 'peer', 'My daughter has no phone in her own name. Whose number do I give?', 'A parent or guardian\'s number can be used. An Indian number is advised, because OTPs are needed again at admission.'),
        (11, 'disputed', 'The portal or captcha will not load from abroad. What worked?', 'Zoom the browser out, use the audio captcha, a mobile hotspot, another browser, or fill early in the morning. A VPN helped a few families in one city; others needed none.'),
        (12, 'peer', 'Does one registration cover both January and April?', 'Credentials made now can be reused for the second session. Only Session 1 is open for payment today; Session 2 will be notified later.')]},
    {'key': 'cities', 'title': 'Exam cities abroad', 'check': [
        'If the present or permanent address is outside India, one Indian city is compulsory.',
        'NTA may allot a different city for administrative reasons, and its decision is final.'], 'qs': [
        (13, 'peer', 'After choosing outside India, no city appeared. What should we do?', 'Many families saw an empty list on 26 October and browser changes did not help. A volunteer relayed a reply from the agency that the issue was resolved, and several families saw cities on 27 October.'),
        (14, 'peer', 'Must I pick all four cities abroad?', 'All four must differ, and at least one must be an Indian city. Many families put their home-country city first and Indian cities after.'),
        (15, 'peer', 'If I list several cities, can the student be put in a lower choice?', 'Families said allotment follows the order, with later choices considered only if earlier ones cannot be used.'),
        (16, 'peer', 'Which address is present and which is permanent?', 'Present: the overseas address. Permanent: the Indian address. The country of the present address decides which foreign cities appear, and it cannot be changed after OTP verification. The mobile need not be local.'),
        (17, 'peer', 'Can Session 1 be in India and Session 2 abroad?', 'Families said many did exactly this last cycle. Each session has its own city choices.'),
        (18, 'open', 'Will more centres be added in a country that has only one?', 'Families and volunteers wrote to the authorities asking for more. A volunteer in the EduAakashaA Members Group said additions this year looked doubtful.')]},
    {'key': 'photo', 'title': 'Photo, name and form fields', 'check': [
        'Use good light, a white background, face about 80% of the frame with both ears visible.',
        'We found no official text on the live-photo mismatch. Keep checking your email after you submit.',
        'NTA asks you to match name and date of birth to the Class 10 certificate.'], 'qs': [
        (19, 'peer', 'The live photo keeps being rejected. Any tips?', 'One family said capturing on a phone through the QR code failed on size and dimensions, while a laptop webcam worked.'),
        (20, 'peer', 'The live photo does not match the old Aadhaar photo.', 'After several failed tries, choose the second option and continue. An email may follow asking for a declaration that both photos show the same person. Cancellation is said to be only for fraud.'),
        (21, 'peer', 'The Aadhaar name differs from the Class 10 name.', 'Use the name exactly as on the Class 10 marksheet. The form fills from Aadhaar and can be edited.'),
        (22, 'peer', 'What do we enter for the Class 12 registration number?', 'It is not mandatory for students now in Class 12. Enter the not-available marker shown on the page, a hyphen. Droppers must give the number.'),
        (23, 'peer', 'Which school type for an Indian-curriculum school abroad?', 'Several families repeatedly chose Private Unaided. For the qualifying board, pick the board named on your certificates, which is CBSE for many schools in the region.'),
        (24, 'peer', 'Is the APAAR ID mandatory?', 'No. Select no if you do not have one. It is also one of the identity options if Aadhaar is unavailable.')]},
    {'key': 'category', 'title': 'Nationality, category and certificates', 'check': [
        'Ask the NTA helpline before submitting if you are unsure about nationality.',
        'Confirm the OBC-NCL certificate with the issuing authority in India.',
        'No official figure was cited for how long an NRI certificate stays valid.',
        'The 75% rule is an admission rule, not a JEE Main registration rule. Read the DASA and JoSAA brochures.'], 'qs': [
        (25, 'disputed', 'Which nationality for an Indian-passport NRI child?', 'Families said choose Indian national, which includes NRI, and keep OCI and foreign national for those categories. One family chose wrongly and found no fix.'),
        (26, 'peer', 'Can a state OBC certificate be used?', 'No. Only the Central-list OBC-NCL certificate counts for reservation. At registration only the certificate details are typed, not uploaded.'),
        (27, 'disputed', 'Can Gulf-resident families claim OBC-NCL given the income limit?', 'Earlier replies said no. Later a family said salary is not counted and only other income is assessed. DASA has no reservation; JoSAA and CSAB use it. The families did not fully agree.'),
        (28, 'disputed', 'Do we need an NRI certificate?', 'Families concluded it is not needed for registration, DASA allotment, JoSAA or CSAB. Only direct NRI-quota seats in private colleges may ask. Validity was quoted as six months to one year.'),
        (29, 'peer', 'Which quota applies to Gulf-schooled students?', 'Not Home State. They are treated as All India or Other State.'),
        (30, 'peer', 'Is the 75% rule overall or only in PCM?', 'Overall across the subjects, not PCM alone. A parent said a student with 65% would not qualify.')]},
    {'key': 'forms', 'title': 'Forms, sessions and DASA', 'check': [
        'The bulletin says no candidate may fill more than one form. NTA\'s public notice says a duplicate filled in good faith keeps the paid form. Use the 27 to 29 Nov window for small slips and call the helpline first.',
        'The best NTA score across the sessions counts.'], 'qs': [
        (31, 'disputed', 'We made a mistake. Can we submit a new form?', 'A forwarded notice said a fresh form is allowed, with only the last paid form counting and the earlier fee not refunded. Other families advised registering once only.'),
        (32, 'peer', 'Should we start now or wait until we have everything?', 'Collect documents, read the bulletin, then register once. A volunteer suggested finishing by mid November instead of the last day.'),
        (33, 'peer', 'Should my child appear in both sessions?', 'Several families strongly advised both: the better score counts and the first attempt is practice. Only Session 1 can be paid now.'),
        (34, 'disputed', 'Is non-CIWG decided by Class 12 marks?', 'A claim circulated that it is. It was corrected: both CIWG and non-CIWG are allotted on JEE Main rank. Class 12 marks are an eligibility condition.'),
        (35, 'peer', 'Can a CIWG-eligible student also apply for non-CIWG as a backup?', 'Yes, by paying the additional amount. Non-CIWG tuition is higher and payment does not guarantee a seat. If a CIWG seat is allotted, the extra is refundable; a refund was still awaited by some in early October.'),
        (36, 'peer', 'How does a family start the CIWG route for 2027?', 'Write JEE Main in January and April, meet the Class 12 criterion, follow the bulletin, and join counselling after the results, around July.')]},
]

MYTHS = [
    ('Passport still works for registration', 'Families report DigiLocker-based sign-in only for Indian citizens this year. A non-Indian passport upload is for foreign nationals and OCI.'),
    ('DigiLocker is optional', 'It is the route. Create it, complete Re-KYC and fetch documents as issued documents.'),
    ('Aadhaar must match every document', 'The application name follows the Class 10 marksheet, and the form lets you edit it.'),
    ('An old Aadhaar photo blocks registration', 'It does not block. A live-photo mismatch is flagged, and families report a declaration email.'),
    ('A state OBC certificate is enough', 'Only the Central-list OBC-NCL certificate counts.'),
    ('An NRI certificate is mandatory', 'Not for registration or DASA allotment, per families. Private NRI-quota seats may ask.'),
    ('Non-CIWG is decided by Class 12 marks', 'Both are decided by JEE Main rank. Marks are eligibility.'),
    ('The empty city list is a browser fault', 'It was a site-side fault, fixed after NTA was told.'),
    ('The Class 12 registration number is mandatory', 'Only for droppers. Others enter a hyphen.'),
    ('Both sessions can be paid today', 'Only Session 1 is open. Session 2 comes later.'),
    ('A scanned marksheet in the DigiLocker drive is enough', 'It must be fetched as an issued document.'),
    ('A fresh form is a safe fix for a mistake', 'The bulletin allows one application. Call the helpline first.'),
]
CORRECTIONS = [
    ('Renew the passport any time', 'An embassy statement shared later: renewal is accepted within about one year of expiry unless lost, damaged or particulars change.'),
    ('Students over 16 should renew', 'The rule is a ten-year passport after age 15, with the adult fee.'),
    ('OBC-NCL is not for Gulf-resident families', 'Later: salary income is not counted, only other income. Still not unanimous.'),
    ('An email OTP can replace the Aadhaar OTP', 'It works only after DigiLocker login, not for the first Aadhaar fetch.'),
    ('Align addresses with Aadhaar or passport', 'No proof is needed. Give the real present and permanent addresses.'),
    ('The passport problem is a glitch awaiting a reply', 'Families later noted passport worked last year; the rule is new this cycle.'),
    ('NRI certificate valid one year', 'Quoted later as six months. No official figure was shown.'),
]
OPEN_QS = [
    'Will NTA restore passport sign-in for Indian citizens?', 'What happens to a candidate whose live photo does not match an old Aadhaar photo?', 'How can a wrong nationality choice be corrected?',
    'Is there a route if the Aadhaar-linked mobile is permanently inactive and the family is abroad?', 'Will more centres be added in countries that have only one?',
    'Can an NRI family claim OBC-NCL?', 'Is a fresh form safe after a mistake?', 'What number format should the alternative contact use?',
]

CHECKLIST = [
    ('Aadhaar mobile works', 'Is the Indian number linked to Aadhaar active, and can it receive an OTP abroad with roaming?'),
    ('Aadhaar photo and name', 'Is the photo recent? Does the name match the Class 10 marksheet? If not, plan the India visit now.'),
    ('DigiLocker ready', 'Account created, Re-KYC done, Aadhaar or PAN fetched into issued documents.'),
    ('Email you can open', 'Every OTP and recovery message goes here. Check the spam folder.'),
    ('Addresses ready', 'Present address abroad, permanent address in India, both complete.'),
    ('Four cities chosen', 'All different, at least one in India. Decide the order now.'),
    ('Files prepared', 'Photo, signature and certificates in the right format and size. Laptop webcam for the live photo.'),
    ('Payment method tested', 'Card or UPI that works for an international payer. Know the fee for an outside-India centre.'),
    ('One form only', 'Plan to register once. Save the confirmation page and keep the application number.'),
    ('Both sessions', 'Calendar: Session 1 closes 22 Nov, Session 2 opens 5 Jan.'),
]

GLOSSARY = [
    ('AIU', 'Association of Indian Universities. Issues equivalence certificates for boards outside India.'), ('APAAR', 'A student ID. Optional on the form; also an eKYC option.'),
    ('CIWG', 'Children of Indian Workers in the Gulf. A DASA category for students whose Classes 11 and 12 were in the Gulf; NRI-only.'), ('CSAB', 'Counselling body for seats left after JoSAA.'),
    ('DASA', 'Direct Admission of Students Abroad. A route into NITs and other institutes for NRIs and foreign nationals.'), ('DigiLocker', 'Government document wallet. The route to NTA sign-in.'),
    ('eKYC / Re-KYC', 'Identity check through Aadhaar, PAN, driving licence or APAAR; Re-KYC refreshes the DigiLocker record.'),
    ('e-Pramaan, JanParichay', 'Alternative government sign-in services under MeriPehchaan.'), ('EWS', 'Economically Weaker Section. 10% quota; certificate dated on or after 1 April 2026.'),
    ('IST', 'Indian Standard Time, used for every NTA timing.'), ('JoSAA', 'Joint counselling for IITs, NITs, IIITs and GFTIs.'),
    ('MeriPehchaan', 'NTA sign-in that links to DigiLocker and others.'), ('NCL', 'Non-Creamy Layer. The OBC condition for reservation.'),
    ('NRI', 'Non-Resident Indian. An Indian citizen living abroad.'), ('NTA', 'National Testing Agency. Conducts JEE Main.'),
    ('OCI', 'Overseas Citizen of India. Uses the foreign-national upload and the OCI quota rule.'), ('OTP', 'One-time password sent to your phone or email.'),
    ('PwD', 'Person with Disability. 5% horizontal reservation.'), ('UDID', 'Unique Disability ID card.'), ('UFM', 'Unfair Means. Includes appearing under more than one application number.'),
]
