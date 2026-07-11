"""Email template registry for /admin/templates.

Each template card has one or more "versions" (a version selector shows when
there is more than one). `subject` / `text` / `html` carry {placeholders}
filled client-side from that version's fields. The `html` is the email body
only — it is wrapped in the branded shell (logo header + footer) client-side,
so every email looks identical without repeating the chrome here.

Nothing is auto-sent: the admin opens a ready draft (Gmail compose / mailto)
or copies the formatted email and pastes it into Gmail.
"""

SENDER_EMAIL = 'eduaakashaa@gmail.com'
WHATSAPP_NUMBER = '+91 80157 22706'
PHONE_UAE = '+971 50 516 8081'
SITE = 'https://eduaakashaa.onrender.com'
LOGO_URL = SITE + '/static/images/logo.png'


def _f(key, label, default=''):
    return {'key': key, 'label': label, 'default': default}


def _btn(url, label):
    """Inline-styled CTA button that survives Gmail's CSS sanitiser."""
    return ('<p style="margin:24px 0 8px"><a href="' + url + '" '
            'style="background:#0E3A8A;color:#ffffff;text-decoration:none;'
            'padding:12px 28px;border-radius:999px;font-weight:700;font-size:14px;'
            'display:inline-block">' + label + '</a></p>')


# --------------------------------------------------------------------------- #
# The registry. Grouped by `category` for the admin UI.
# --------------------------------------------------------------------------- #
EMAIL_TEMPLATES = [

    # ===================== Members & Onboarding ============================ #
    {'key': 'welcome', 'icon': '👋', 'label': 'Welcome message',
     'category': 'Members & Onboarding',
     'desc': 'Welcome a new user, a premium member who just paid, or a new College Guide.',
     'versions': [
        {'key': 'user', 'label': 'New user', 'fields': [_f('name', 'First name', 'there')],
         'subject': 'Welcome to EduAakashaa 🎓',
         'text': ("Hi {name},\n\nWelcome to EduAakashaa! You now have free access to our "
                  "college predictors (JOSAA, TNEA, DASA), NIRF rankings and career-planning "
                  "tools.\n\nWhenever you're deciding on a college, we're here to help you "
                  "choose right.\n\nStart exploring: " + SITE + "\nQuestions? WhatsApp us at "
                  + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Welcome to <strong>EduAakashaa</strong>! You now have "
                  "free access to our college predictors (JOSAA, TNEA, DASA), NIRF rankings "
                  "and career-planning tools.</p><p>Whenever you're deciding on a college, "
                  "we're here to help you choose right.</p>"
                  + _btn(SITE, 'Start exploring')
                  + "<p>Questions? WhatsApp us at <strong>" + WHATSAPP_NUMBER + "</strong>.</p>")},
        {'key': 'premium', 'label': 'Premium — just paid',
         'fields': [_f('name', 'First name', 'there'), _f('plan', 'Plan', 'Premium')],
         'subject': 'Your EduAakashaa Premium is active, {name}! 🎉',
         'text': ("Hi {name},\n\nThank you for your payment — your {plan} membership is now "
                  "active! You've unlocked every premium tool: expert predictors, member "
                  "reports and 1-on-1 counsellor support.\n\nCounselling season moves fast — "
                  "let's build your perfect choice list together. Head to your dashboard to "
                  "get started: " + SITE + "/dashboard\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thank you for your payment — your <strong>{plan}</strong> "
                  "membership is now active! 🎉 You've unlocked every premium tool: expert "
                  "predictors, member reports and 1-on-1 counsellor support.</p>"
                  "<p>Counselling season moves fast — let's build your perfect choice list "
                  "together.</p>" + _btn(SITE + '/dashboard', 'Go to your dashboard'))},
        {'key': 'guide', 'label': 'New College Guide',
         'fields': [_f('name', 'First name', 'there'), _f('college', 'College', 'your college')],
         'subject': "You're a College Guide now, {name}! 🙌",
         'text': ("Hi {name},\n\nWelcome aboard as an EduAakashaa College Guide! Whenever a "
                  "parent has questions about {college}, we'll reach out — hop on a quick call "
                  "or drop a short video, and get paid ₹500–1000 for it. No lock-in, no spam, "
                  "fully on your schedule.\n\nMeanwhile, share your invite link to earn ₹1000 "
                  "referral bonuses. We'll be in touch when a parent wants your take.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Welcome aboard as an <strong>EduAakashaa College Guide</strong>! "
                  "Whenever a parent has questions about <strong>{college}</strong>, we'll reach "
                  "out — hop on a quick call or drop a short video, and <strong>get paid ₹500–1000</strong> "
                  "for it. No lock-in, no spam, fully on your schedule.</p>"
                  "<p>Meanwhile, share your invite link to earn ₹1000 referral bonuses. We'll be "
                  "in touch when a parent wants your take.</p>")},
     ]},

    {'key': 'assessment_invite', 'icon': '🧭', 'label': 'Onboarding assessment invite',
     'category': 'Members & Onboarding',
     'desc': 'Ask the student (or parent) to complete the profiling assessment before the first 1-on-1.',
     'versions': [
        {'key': 'student', 'label': 'Student', 'fields': [
            _f('name', 'First name', 'there'),
            _f('link', 'Assessment link', SITE + '/onboarding-assessment/student'),
            _f('days', 'Complete within', '2 days')],
         'subject': 'Before your first session — a 20-minute head start, {name}',
         'text': ("Hi {name},\n\nBefore your first 1-on-1, we'd like to understand you properly "
                  "— your interests, strengths and what you actually want from engineering. "
                  "Please complete your onboarding assessment (about 20 minutes, on your "
                  "phone):\n\n{link}\n\nAnswer honestly — there are no right answers, and "
                  "nothing you say is shared without your OK. Your counsellor uses this to "
                  "make the session about YOU, not generic advice.\n\nPlease finish it within "
                  "{days} so we can prepare.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Before your first 1-on-1, we'd like to understand you "
                  "properly — your interests, strengths and what you actually want from "
                  "engineering. Please complete your onboarding assessment "
                  "(about <strong>20 minutes</strong>, on your phone).</p>"
                  + _btn('{link}', 'Start my assessment')
                  + "<p>Answer honestly — there are no right answers, and nothing you say is "
                  "shared without your OK. Your counsellor uses this to make the session about "
                  "<strong>you</strong>, not generic advice.</p>"
                  "<p>Please finish it within <strong>{days}</strong> so we can prepare.</p>")},
        {'key': 'parent', 'label': 'Parent', 'fields': [
            _f('name', 'Parent name', 'there'), _f('student', 'Student name', 'your child'),
            _f('link', 'Assessment link', SITE + '/onboarding-assessment/parent'),
            _f('days', 'Complete within', '2 days')],
         'subject': 'Your side of the picture — 10 minutes before our session',
         'text': ("Dear {name},\n\nThank you for trusting EduAakashaa with {student}'s "
                  "engineering admissions. Before the first counselling session, we ask "
                  "parents to fill a short questionnaire (about 10 minutes) — your "
                  "expectations, budget planning and questions about the admissions "
                  "process:\n\n{link}\n\nPlease fill it independently — don't compare answers "
                  "with {student}. Seeing where you both agree (and differ) is exactly what "
                  "makes the first session useful.\n\nPlease finish it within {days}.\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Dear {name},</p><p>Thank you for trusting EduAakashaa with "
                  "<strong>{student}</strong>'s engineering admissions. Before the first "
                  "counselling session, we ask parents to fill a short questionnaire "
                  "(about <strong>10 minutes</strong>) — your expectations, budget planning "
                  "and questions about the admissions process.</p>"
                  + _btn('{link}', 'Fill the parent questionnaire')
                  + "<p>Please fill it independently — don't compare answers with {student}. "
                  "Seeing where you both agree (and differ) is exactly what makes the first "
                  "session useful.</p><p>Please finish it within <strong>{days}</strong>.</p>")},
     ]},

    {'key': 'session_booked', 'icon': '📅', 'label': 'Session confirmed',
     'category': 'Members & Onboarding',
     'desc': 'Confirm a booked 1-on-1 counselling session with date, time and how to join.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('date', 'Date', '15 Jul 2026'),
            _f('time', 'Time (IST)', '6:00 PM'), _f('mode', 'Mode', 'Google Meet'),
            _f('counsellor', 'Counsellor', 'our senior counsellor')],
         'subject': 'Confirmed: your 1-on-1 on {date} at {time} IST',
         'text': ("Hi {name},\n\nYour 1-on-1 counselling session is confirmed:\n\n"
                  "Date: {date}\nTime: {time} IST\nMode: {mode}\nWith: {counsellor}\n\n"
                  "Keep your recent marks handy, and bring every question you have — no "
                  "question is too small. If the time doesn't work anymore, reply here or "
                  "WhatsApp us at " + WHATSAPP_NUMBER + " and we'll reschedule.\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Your 1-on-1 counselling session is confirmed:</p>"
                  "<table style=\"border-collapse:collapse;margin:16px 0;font-size:15px\">"
                  "<tr><td style=\"padding:6px 18px 6px 0;color:#5A6278\">Date</td>"
                  "<td style=\"padding:6px 0;font-weight:700\">{date}</td></tr>"
                  "<tr><td style=\"padding:6px 18px 6px 0;color:#5A6278\">Time</td>"
                  "<td style=\"padding:6px 0;font-weight:700\">{time} IST</td></tr>"
                  "<tr><td style=\"padding:6px 18px 6px 0;color:#5A6278\">Mode</td>"
                  "<td style=\"padding:6px 0;font-weight:700\">{mode}</td></tr>"
                  "<tr><td style=\"padding:6px 18px 6px 0;color:#5A6278\">With</td>"
                  "<td style=\"padding:6px 0;font-weight:700\">{counsellor}</td></tr></table>"
                  "<p>Keep your recent marks handy, and bring every question you have — no "
                  "question is too small.</p><p>If the time doesn't work anymore, reply here "
                  "or WhatsApp us at <strong>" + WHATSAPP_NUMBER + "</strong> and we'll "
                  "reschedule.</p>")},
     ]},

    {'key': 'session_recap', 'icon': '🗒️', 'label': 'Session recap & next steps',
     'category': 'Members & Onboarding',
     'desc': 'After a 1-on-1: thank them and put the agreed next steps in writing.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'),
            _f('steps', 'Agreed next steps', 'finalise your college list by Friday')],
         'subject': 'Your session recap & next steps, {name}',
         'text': ("Hi {name},\n\nGreat talking with you today! Putting what we agreed in "
                  "writing so nothing slips:\n\nNext steps: {steps}\n\nYour dashboard has "
                  "every tool we used in the session: " + SITE + "/dashboard\n\nStuck on "
                  "anything before the next check-in? Reply here or WhatsApp us at "
                  + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Great talking with you today! Putting what we agreed "
                  "in writing so nothing slips:</p>"
                  "<div style=\"background:#FBF7EE;border-left:4px solid #FF6B0A;padding:14px 18px;"
                  "border-radius:0 10px 10px 0;margin:16px 0\"><strong>Next steps:</strong> "
                  "{steps}</div>"
                  + _btn(SITE + '/dashboard', 'Open your dashboard')
                  + "<p>Stuck on anything before the next check-in? Reply here or WhatsApp us "
                  "at <strong>" + WHATSAPP_NUMBER + "</strong>.</p>")},
     ]},

    {'key': 'report_ready', 'icon': '📊', 'label': 'Report delivered',
     'category': 'Members & Onboarding',
     'desc': 'Tell a member their personalised report is ready to view/download.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'),
            _f('report', 'Report name', 'College Fit Report')],
         'subject': 'Your {report} is ready, {name} 📊',
         'text': ("Hi {name},\n\nYour personalised {report} is ready! It covers our analysis "
                  "and clear recommendations for your next steps.\n\nView it on your "
                  "dashboard: " + SITE + "/dashboard\n\nRead it once, note your questions, "
                  "and bring them to your next session — that's where the report really "
                  "pays off.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Your personalised <strong>{report}</strong> is ready! "
                  "It covers our analysis and clear recommendations for your next steps.</p>"
                  + _btn(SITE + '/dashboard', 'View my report')
                  + "<p>Read it once, note your questions, and bring them to your next "
                  "session — that's where the report really pays off.</p>")},
     ]},

    {'key': 'docs', 'icon': '📄', 'label': 'Documents',
     'category': 'Members & Onboarding',
     'desc': 'Chase missing documents, or confirm everything has been received.',
     'versions': [
        {'key': 'pending', 'label': 'Missing documents', 'fields': [
            _f('name', 'First name', 'there'),
            _f('docs', 'Documents needed', 'Class 12 marksheet, JEE scorecard')],
         'subject': 'Documents pending: {docs}',
         'text': ("Hi {name},\n\nTo move ahead with your counselling file we still need:\n\n"
                  "{docs}\n\nPlease send them as photos or PDFs — reply to this email or "
                  "WhatsApp them to " + WHATSAPP_NUMBER + ". Clear photos are fine; nothing "
                  "needs to be attested at this stage.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>To move ahead with your counselling file we still "
                  "need:</p><div style=\"background:#FBF7EE;border-left:4px solid #E89A1C;"
                  "padding:14px 18px;border-radius:0 10px 10px 0;margin:16px 0\">"
                  "<strong>{docs}</strong></div>"
                  "<p>Please send them as photos or PDFs — reply to this email or WhatsApp "
                  "them to <strong>" + WHATSAPP_NUMBER + "</strong>. Clear photos are fine; "
                  "nothing needs to be attested at this stage.</p>")},
        {'key': 'received', 'label': 'All received', 'fields': [_f('name', 'First name', 'there')],
         'subject': 'Got everything — your documents are in ✅',
         'text': ("Hi {name},\n\nQuick confirmation: we've received all your documents and "
                  "your counselling file is complete. Nothing more needed from you right "
                  "now.\n\nWe'll flag it immediately if anything else comes up during "
                  "registration or choice filling.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Quick confirmation: we've received all your documents "
                  "and your counselling file is <strong>complete</strong>. ✅ Nothing more "
                  "needed from you right now.</p><p>We'll flag it immediately if anything "
                  "else comes up during registration or choice filling.</p>")},
     ]},

    {'key': 'renewal', 'icon': '🔔', 'label': 'Premium renewal reminder',
     'category': 'Members & Onboarding',
     'desc': 'Remind a premium member their membership is expiring.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('plan', 'Plan', 'Premium'),
            _f('validity', 'Valid until', '31 Mar 2026')],
         'subject': 'Your EduAakashaa membership is expiring soon, {name}',
         'text': ("Hi {name},\n\nA quick heads-up — your {plan} membership is valid until "
                  "{validity}. Renew in time to keep uninterrupted access to the premium "
                  "predictors, expert reports and counsellor support during counselling "
                  "season.\n\nRenew: " + SITE + "/members-registration\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>A quick heads-up — your <strong>{plan}</strong> membership "
                  "is valid until <strong>{validity}</strong>. Renew in time to keep "
                  "uninterrupted access to the premium predictors, expert reports and "
                  "counsellor support during counselling season.</p>"
                  + _btn(SITE + '/members-registration', 'Renew now'))},
     ]},

    # ===================== Admissions & Payments =========================== #
    {'key': 'application', 'icon': '📥', 'label': 'Application received',
     'category': 'Admissions & Payments',
     'desc': 'Acknowledge a new membership application with its reference number.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('reference', 'Reference', 'EA-PREM-0001')],
         'subject': "We've got your application, {name} (ref {reference})",
         'text': ("Hi {name},\n\nThanks for applying for EduAakashaa membership — your reference "
                  "number is {reference}. Our team will review it and reach out within 2 working "
                  "days to confirm your plan and next steps.\n\nQuestions in the meantime? "
                  "WhatsApp us at " + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thanks for applying for EduAakashaa membership — your "
                  "reference number is <strong>{reference}</strong>. Our team will review it and "
                  "reach out within 2 working days to confirm your plan and next steps.</p>"
                  "<p>Questions in the meantime? WhatsApp us at <strong>" + WHATSAPP_NUMBER
                  + "</strong>.</p>")},
     ]},

    {'key': 'app_approved', 'icon': '✅', 'label': 'Application approved',
     'category': 'Admissions & Payments',
     'desc': 'Confirm the plan and share the amount so the family can pay and get started.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('reference', 'Reference', 'EA-PREM-0001'),
            _f('plan', 'Plan', 'Premium'), _f('amount', 'Amount ₹', '15,000')],
         'subject': 'Approved! Your {plan} membership awaits, {name} ✅',
         'text': ("Hi {name},\n\nGood news — your application ({reference}) is approved for the "
                  "{plan} plan. The membership fee is ₹{amount} (inclusive of GST).\n\nWe'll "
                  "send the invoice and payment details separately. Once the payment is in, "
                  "your membership activates the same day and we schedule your first 1-on-1."
                  "\n\nAny questions about the plan or payment? WhatsApp us at "
                  + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Good news — your application (<strong>{reference}</strong>) "
                  "is approved for the <strong>{plan}</strong> plan. The membership fee is "
                  "<strong>₹{amount}</strong> (inclusive of GST).</p>"
                  "<p>We'll send the invoice and payment details separately. Once the payment "
                  "is in, your membership activates the same day and we schedule your first "
                  "1-on-1.</p><p>Any questions about the plan or payment? WhatsApp us at "
                  "<strong>" + WHATSAPP_NUMBER + "</strong>.</p>")},
     ]},

    {'key': 'payment_reminder', 'icon': '⏳', 'label': 'Payment reminder',
     'category': 'Admissions & Payments',
     'desc': 'Gently chase a pending invoice / balance due.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('reference', 'Invoice / reference', 'EA/0001'),
            _f('amount', 'Balance due ₹', '7,500'), _f('due', 'Due by', '20 Jul 2026')],
         'subject': 'Gentle reminder: ₹{amount} pending on {reference}',
         'text': ("Hi {name},\n\nA gentle reminder that ₹{amount} is pending on your "
                  "EduAakashaa invoice {reference}, due by {due}.\n\nOnce it's cleared, your "
                  "membership continues uninterrupted — especially important with counselling "
                  "deadlines coming up.\n\nAlready paid? Please ignore this and accept our "
                  "thanks — or reply with the reference so we can match it quickly.\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>A gentle reminder that <strong>₹{amount}</strong> is "
                  "pending on your EduAakashaa invoice <strong>{reference}</strong>, due by "
                  "<strong>{due}</strong>.</p><p>Once it's cleared, your membership continues "
                  "uninterrupted — especially important with counselling deadlines coming "
                  "up.</p><p>Already paid? Please ignore this and accept our thanks — or reply "
                  "with the reference so we can match it quickly.</p>")},
     ]},

    {'key': 'payment_received', 'icon': '🧾', 'label': 'Payment received',
     'category': 'Admissions & Payments',
     'desc': 'Acknowledge a full or partial payment with the receipt details.',
     'versions': [
        {'key': 'full', 'label': 'Paid in full', 'fields': [
            _f('name', 'First name', 'there'), _f('amount', 'Amount ₹', '15,000'),
            _f('receipt', 'Receipt no', 'RCPT/0001')],
         'subject': 'Payment received — receipt {receipt} 🧾',
         'text': ("Hi {name},\n\nWe've received your payment of ₹{amount} — thank you! Your "
                  "receipt number is {receipt} and your membership is fully paid.\n\nNext: "
                  "we'll schedule your onboarding and first 1-on-1. See you inside!\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>We've received your payment of <strong>₹{amount}</strong> "
                  "— thank you! Your receipt number is <strong>{receipt}</strong> and your "
                  "membership is <strong>fully paid</strong>.</p><p>Next: we'll schedule your "
                  "onboarding and first 1-on-1. See you inside!</p>")},
        {'key': 'partial', 'label': 'Partial payment', 'fields': [
            _f('name', 'First name', 'there'), _f('amount', 'Amount received ₹', '7,500'),
            _f('balance', 'Balance due ₹', '7,500'), _f('due', 'Balance due by', '31 Jul 2026')],
         'subject': 'Received ₹{amount} — ₹{balance} remaining',
         'text': ("Hi {name},\n\nThank you — we've received your payment of ₹{amount}. The "
                  "remaining balance is ₹{balance}, due by {due}.\n\nYour membership benefits "
                  "are already active, so don't wait to use the tools and book your "
                  "sessions.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thank you — we've received your payment of "
                  "<strong>₹{amount}</strong>. The remaining balance is "
                  "<strong>₹{balance}</strong>, due by <strong>{due}</strong>.</p>"
                  "<p>Your membership benefits are already active, so don't wait to use the "
                  "tools and book your sessions.</p>")},
     ]},

    # ========================= College Guides ============================== #
    {'key': 'guide_match', 'icon': '🎯', 'label': 'Guide — matched with a parent',
     'category': 'College Guides',
     'desc': 'Ask a College Guide if they’re free to talk to a matched parent.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('parent', 'Parent / who', 'A parent'),
            _f('college', 'College', 'your college')],
         'subject': 'A parent wants to talk to you, {name} 🎓',
         'text': ("Hi {name},\n\n{parent} is looking at {college} and would love to hear from "
                  "someone who's actually been there — you! It's a short, paid session "
                  "(₹500–1000): a quick call or a short video answering their questions.\n\n"
                  "Are you free in the next few days? Reply and we'll set it up. Totally your "
                  "call — no pressure.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p><strong>{parent}</strong> is looking at "
                  "<strong>{college}</strong> and would love to hear from someone who's actually "
                  "been there — you! It's a short, paid session (<strong>₹500–1000</strong>): a "
                  "quick call or a short video answering their questions.</p><p>Are you free in "
                  "the next few days? Reply and we'll set it up. Totally your call — no pressure.</p>")},
     ]},

    {'key': 'ty_session', 'icon': '🙏', 'label': 'Thank you — Guide session',
     'category': 'College Guides',
     'desc': 'Thank a College Guide after they answer a parent’s questions.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('college', 'College', 'your college'),
            _f('amount', 'Payout ₹', '1000')],
         'subject': 'Thanks for guiding a parent, {name} 🙏',
         'text': ("Hi {name},\n\nThank you for taking the time to answer a parent's questions "
                  "about {college} — your honest, first-hand take genuinely helps a family "
                  "choose right.\n\nYour payout of ₹{amount} is being processed and will "
                  "reflect in your College Guide dashboard. We'll reach out again when another "
                  "parent needs your perspective.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thank you for taking the time to answer a parent's "
                  "questions about <strong>{college}</strong> — your honest, first-hand take "
                  "genuinely helps a family choose right.</p><p>Your payout of "
                  "<strong>₹{amount}</strong> is being processed and will reflect in your "
                  "College Guide dashboard. We'll reach out again when another parent needs "
                  "your perspective.</p>")},
     ]},

    {'key': 'payment', 'icon': '💸', 'label': 'Payout credited — Guide',
     'category': 'College Guides',
     'desc': 'Tell a College Guide their payout has been credited.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('amount', 'Amount ₹', '1000')],
         'subject': '₹{amount} credited to you, {name} 💸',
         'text': ("Hi {name},\n\nGood news — your payout of ₹{amount} has been credited. Thank "
                  "you for being an EduAakashaa College Guide and helping parents with your "
                  "real college experience.\n\nKeep an eye on your dashboard for your next "
                  "session. Questions about a payout? Just reply here.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Good news — your payout of <strong>₹{amount}</strong> "
                  "has been credited. 💸 Thank you for being an EduAakashaa College Guide and "
                  "helping parents with your real college experience.</p><p>Keep an eye on your "
                  "dashboard for your next session. Questions about a payout? Just reply here.</p>")},
     ]},

    {'key': 'ty_survey', 'icon': '📝', 'label': 'Thank you — Survey',
     'category': 'College Guides',
     'desc': 'Thank someone for filling the college experience survey (and nudge them to guide).',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('college', 'College', 'your college')],
         'subject': 'Thanks for the honest review, {name}! 🙌',
         'text': ("Hi {name},\n\nThank you for filling out the EduAakashaa college survey about "
                  "{college}. Your real, no-filter feedback helps NRI parents make better "
                  "decisions for their kids.\n\nWant to earn from what you know? Become a "
                  "College Guide and get paid ₹500–1000 to answer parents' questions: "
                  + SITE + "/alumni-network\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thank you for filling out the EduAakashaa college survey "
                  "about <strong>{college}</strong>. Your real, no-filter feedback helps NRI "
                  "parents make better decisions for their kids.</p><p>Want to earn from what "
                  "you know? Become a College Guide and get paid <strong>₹500–1000</strong> to "
                  "answer parents' questions.</p>"
                  + _btn(SITE + '/alumni-network', 'Become a College Guide'))},
     ]},

    # ======================= Engagement & Season =========================== #
    {'key': 'deadline_alert', 'icon': '⏰', 'label': 'Counselling deadline alert',
     'category': 'Engagement & Season',
     'desc': 'Warn a family about an approaching JoSAA / TNEA / other counselling deadline.',
     'versions': [
        {'key': 'josaa', 'label': 'JoSAA', 'fields': [
            _f('name', 'First name', 'there'), _f('round', 'Round / event', 'JoSAA Round 2 choice locking'),
            _f('date', 'Deadline', '18 Jul 2026, 5 PM')],
         'subject': '⏰ {round} closes {date}',
         'text': ("Hi {name},\n\nHeads-up: {round} closes on {date}. After that the portal "
                  "locks and choices can't be changed.\n\nIf you want a second pair of eyes on "
                  "your choice list before you lock, reply here or WhatsApp us at "
                  + WHATSAPP_NUMBER + " — we'll review it with you before the deadline.\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Heads-up: <strong>{round}</strong> closes on "
                  "<strong>{date}</strong>. After that the portal locks and choices can't be "
                  "changed.</p><p>If you want a second pair of eyes on your choice list before "
                  "you lock, reply here or WhatsApp us at <strong>" + WHATSAPP_NUMBER
                  + "</strong> — we'll review it with you before the deadline.</p>")},
        {'key': 'tnea', 'label': 'TNEA', 'fields': [
            _f('name', 'First name', 'there'), _f('round', 'Round / event', 'TNEA Round 1 choice filling'),
            _f('date', 'Deadline', '22 Jul 2026')],
         'subject': '⏰ {round} — deadline {date}',
         'text': ("Hi {name},\n\nReminder: {round} must be completed by {date}. TNEA rounds "
                  "move quickly and missed windows can't be reopened.\n\nUnsure about your "
                  "order of choices? Our TNEA tools and counsellors can pressure-test your "
                  "list before you submit: " + SITE + "\n\nWhatsApp us any time: "
                  + WHATSAPP_NUMBER + "\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Reminder: <strong>{round}</strong> must be completed by "
                  "<strong>{date}</strong>. TNEA rounds move quickly and missed windows can't "
                  "be reopened.</p><p>Unsure about your order of choices? Our TNEA tools and "
                  "counsellors can pressure-test your list before you submit.</p>"
                  + _btn(SITE, 'Open the TNEA tools')
                  + "<p>WhatsApp us any time: <strong>" + WHATSAPP_NUMBER + "</strong></p>")},
        {'key': 'generic', 'label': 'Other', 'fields': [
            _f('name', 'First name', 'there'), _f('round', 'Event', 'BITSAT application window'),
            _f('date', 'Deadline', '25 Jul 2026')],
         'subject': '⏰ Don\'t miss it: {round} — {date}',
         'text': ("Hi {name},\n\nQuick reminder: {round} closes on {date}.\n\nIf this applies "
                  "to you, block 30 minutes this week to finish it — last-day server rushes "
                  "are real. Need help deciding whether it's worth applying? Reply here or "
                  "WhatsApp " + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Quick reminder: <strong>{round}</strong> closes on "
                  "<strong>{date}</strong>.</p><p>If this applies to you, block 30 minutes "
                  "this week to finish it — last-day server rushes are real. Need help "
                  "deciding whether it's worth applying? Reply here or WhatsApp <strong>"
                  + WHATSAPP_NUMBER + "</strong>.</p>")},
     ]},

    {'key': 'winback', 'icon': '🌱', 'label': 'Win-back — expired member',
     'category': 'Engagement & Season',
     'desc': 'Re-engage a member whose premium membership lapsed.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there')],
         'subject': 'We kept your seat warm, {name}',
         'text': ("Hi {name},\n\nYour EduAakashaa Premium has lapsed — but your data, saved "
                  "predictions and reports are all still here.\n\nIf this admissions season "
                  "still matters for your family, rejoin and pick up exactly where you left "
                  "off — predictors, reports and 1-on-1 counselling included.\n\nRejoin: "
                  + SITE + "/members-registration\n\nNot the right time? No hard feelings — "
                  "the free tools remain yours forever.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Your EduAakashaa Premium has lapsed — but your data, "
                  "saved predictions and reports are all still here.</p><p>If this admissions "
                  "season still matters for your family, rejoin and pick up exactly where you "
                  "left off — predictors, reports and 1-on-1 counselling included.</p>"
                  + _btn(SITE + '/members-registration', 'Rejoin Premium')
                  + "<p>Not the right time? No hard feelings — the free tools remain yours "
                  "forever.</p>")},
     ]},

    {'key': 'feedback', 'icon': '💬', 'label': 'Feedback / testimonial request',
     'category': 'Engagement & Season',
     'desc': 'Ask a member how it went and (optionally) for a short testimonial.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there')],
         'subject': 'How did we do, {name}?',
         'text': ("Hi {name},\n\nNow that the dust has settled, we'd love two minutes of "
                  "honest feedback: what helped, and what we should do better?\n\nJust reply "
                  "to this email — we read every response personally.\n\nAnd if EduAakashaa "
                  "made a real difference for your family, a short line we can share with "
                  "other parents would mean a lot. 🙏\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Now that the dust has settled, we'd love two minutes "
                  "of honest feedback: what helped, and what we should do better?</p>"
                  "<p>Just reply to this email — we read every response personally.</p>"
                  "<p>And if EduAakashaa made a real difference for your family, a short line "
                  "we can share with other parents would mean a lot. 🙏</p>")},
     ]},

    {'key': 'inquiry_reply', 'icon': '📮', 'label': 'Inquiry response',
     'category': 'Engagement & Season',
     'desc': 'First response to a contact-form inquiry — acknowledge and offer a call.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('topic', 'They asked about', 'engineering admissions')],
         'subject': 'Re: your question about {topic}',
         'text': ("Hi {name},\n\nThanks for reaching out to EduAakashaa about {topic} — happy "
                  "to help.\n\nThe quickest way forward is a short call so we understand your "
                  "situation properly. WhatsApp us at " + WHATSAPP_NUMBER + " (India) or "
                  + PHONE_UAE + " (UAE) with a good time, or simply reply to this email with "
                  "your questions.\n\nMeanwhile, our free predictors and guides are at "
                  + SITE + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thanks for reaching out to EduAakashaa about "
                  "<strong>{topic}</strong> — happy to help.</p><p>The quickest way forward is "
                  "a short call so we understand your situation properly. WhatsApp us at "
                  "<strong>" + WHATSAPP_NUMBER + "</strong> (India) or <strong>" + PHONE_UAE
                  + "</strong> (UAE) with a good time, or simply reply to this email with your "
                  "questions.</p>"
                  + _btn(SITE, 'Explore the free tools'))},
     ]},
]
