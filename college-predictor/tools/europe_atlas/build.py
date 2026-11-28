"""Build app/data/europe/atlas.html, the members' Europe Admissions Atlas (/europe-admissions-atlas).

Inputs: data/*.json (research from official pages, checked 28 Nov 2026), the counsellor overlay below (fees used, entry route, dates, SWOT, NRI view)
and template.html. To refresh: update those, then run  python tools/europe_atlas/build.py  from college-predictor/.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
load = lambda n: json.load(open(os.path.join(HERE, 'data', n), encoding='utf-8'))  # noqa: E731

raw = {}
for f in ('eu_A.json', 'eu_B.json', 'eu_C.json'):
    for u in load(f)['universities']:
        raw[u['name']] = u
CT = load('eu_countries.json')
FX = CT['fx']['usd_per_unit']
INR_PER_USD = 101.904 / 1.0957  # both from the ECB file of 2026-11-27

C = {c['iso2']: c for c in CT['countries']}

# salary placeholders (roi) are in GBP for the UK, CHF for Switzerland and EUR elsewhere
# country overlay: post-study months for a bachelor's graduate (None = not confirmed), PR years, work rule, one-line verdicts
CO = {
    'DE': dict(iso3='DEU', psw=18, pswt='Up to 18 months', pr=2, prt='Settlement after 2 years of skilled work following German study, with pension and other conditions; half of study years count for general settlement.', work='140 working days a year', funds=11904, fundsper=1, fee=None, flagc='#DD0000'),
    'NL': dict(iso3='NLD', psw=12, pswt='1-year orientation year', pr=5, prt='EU long-term residence after 5 years; study time may count at 50%.', work='16 h/week with work permit, or full time Jun-Aug', funds=1130.77, fundsper=12, fee=254, flagc='#1E4785'),
    'CH': dict(iso3='CHE', psw=6, pswt='6-month job-search permit', pr=10, prt='Settlement permit C usually after 10 years; study years count only in limited cases.', work='15 h/week, only after 6 months of study', funds=None, fundsper=1, fee=0, flagc='#D52B1E'),
    'GB': dict(iso3='GBR', psw=18, pswt='18-month Graduate visa (applications from 1 Jan 2027)', pr=10, prt='Settlement via work routes; standard period moving to 10 years under the earned-settlement policy. Student and Graduate time does not lead to settlement.', work='20 h/week in term', funds=1171, fundsper=9, fee=558, flagc='#012169'),
    'IE': dict(iso3='IRL', psw=12, pswt='12 months after an honours bachelor’s (level 8)', pr=5, prt='Work permit, then naturalisation after 5 reckonable years; student time does not count.', work='20 h/week in term, full time in holidays', funds=10000, fundsper=1, fee=360, flagc='#169B62'),
    'FR': dict(iso3='FRA', psw=None, pswt='India-France 1+1 year stay is for Master’s graduates; not confirmed after a bachelor’s alone', pr=5, prt='EU long-term resident card after 5 years; whether student years count was not verified.', work='964 h a year', funds=877.5, fundsper=12, fee=50, flagc='#0055A4'),
    'IT': dict(iso3='ITA', psw=12, pswt='About 9-12 months to seek work', pr=None, prt='Permanent residence route not verified.', work='20 h/week, 1,040 h a year', funds=10179.85, fundsper=1, fee=None, flagc='#008C45'),
    'ES': dict(iso3='ESP', psw=12, pswt='12 or 24 months (official pages conflict)', pr=5, prt='EU long-term residence after 5 years; study counts at 50%.', work='30 h/week', funds=600, fundsper=12, fee=None, flagc='#AA151B'),
    'FI': dict(iso3='FIN', psw=24, pswt='Up to 2 years to look for work', pr=6, prt='Generally 6 years from 2026; Migri lists a shorter route for some Finnish degree holders (check conditions).', work='30 h/week on average', funds=800, fundsper=12, fee=600, flagc='#003580'),
    'SE': dict(iso3='SWE', psw=12, pswt='Up to 1 year', pr=4, prt='Permanent residence after 4 years of qualifying work in 7; rules are being tightened.', work='15 h/week (permits from June 2026)', funds=10656, fundsper=12, fee=1500, flagc='#006AA7'),
    'DK': dict(iso3='DNK', psw=12, pswt='6 or 12 months (cut from 3 years on 1 Oct 2026)', pr=8, prt='Usually 8 years; 4 only if every supplementary condition is met.', work='90 h/month, full time Jun-Aug', funds=7426, fundsper=12, fee=3060, flagc='#C8102E'),
}
CUR = {'DE': 'EUR', 'NL': 'EUR', 'CH': 'CHF', 'GB': 'GBP', 'IE': 'EUR', 'FR': 'EUR', 'IT': 'EUR', 'ES': 'EUR', 'FI': 'EUR', 'SE': 'SEK', 'DK': 'DKK'}


def U(key, short, iso, lat, lon, **k):
    k.update(key=key, short=short, iso=iso, lat=lat, lon=lon)
    return k


# Overlay. tui/live are per YEAR in local currency; None = no verified figure. entry: direct | conditional | indirect.
# eng: yes | limited | none. Dates are ISO; 'win' = [open, close, label].
OV = {
    'Technical University of Munich': U('tum', 'TU Munich', 'DE', 48.149, 11.568, yrs=3, tui=6800, tuin='EUR 2,300 or 3,400 per semester from winter 2027/28 (upper band used)', live=19800, liven='Midpoint of EUR 1,300-2,000 a month', ye=194, one=0, eng='limited', entry='conditional', entryt='Class 12 alone is generally not enough: JEE Advanced route, Studienkolleg, or one year of university; APS certificate.',
        sat='Not a stated route', exam='JEE Advanced rank or Studienkolleg exam; aptitude assessment', iv='About 20 min for some programmes', ielts='Not verified', lang='German A2 even for English programmes', win=[['2027-05-15', '2027-07-15', 'Application window']], due='2027-07-15', dueL='15 Jul 2027 (annual window)', roi=65000,
        sch='Small grants and waivers; first-year eligibility not confirmed', cls='Continental; cold winters, warm summers', nri='High-prestige, low-fee name that Indian families know well. The surprise for most is that a CBSE or ISC certificate alone rarely gives direct entry.',
        S=['Top-25 in both QS and THE', 'Low tuition against UK and Switzerland'], W=['Few English bachelors', 'No guaranteed housing'], O=['JEE Advanced rank can open a direct route', '18-month job search and a short settlement path after German study'], T=['Non-EU fees rising from 2027/28', 'Munich rent and 1-4 semester dorm waits']),
    'RWTH Aachen University': U('rwth', 'RWTH Aachen', 'DE', 50.777, 6.078, yrs=3, tui=0, tuin='No tuition; semester contribution about EUR 300-360', ye=716, one=0, live=13200, liven='At least EUR 1,100 a month', eng='none', entry='conditional', entryt='Class 12 alone is generally not enough; German C1 at enrolment; 7% non-EU quota in restricted programmes.',
        sat='Not used', exam='TestAS can offset a weaker grade', iv='Not stated', ielts='B2 English for some programmes', lang='German C1 (all bachelors in German)', win=[['2027-05-04', '2027-07-15', '2026 pattern; 2027 dates unpublished']], due='2027-07-15', dueL='About 15 Jul (2027 not published)', roi=58000,
        sch='None verified', cls='Mild, damp western Germany', nri='Seen as the value engineering choice. Only realistic for a student who will reach C1 German first.',
        S=['No tuition fee', 'Strong engineering brand'], W=['No English bachelor', 'Housing and scholarship data not verified'], O=['Germany’s job-search and settlement routes', 'Industry region with large engineering employers'], T=['C1 German takes 1-2 years', 'Quota competition']),
    'Delft University of Technology': U('delft', 'TU Delft', 'NL', 52.002, 4.373, yrs=3, tui=20563, tuin='2027/28 non-EU fee', live=14200, liven='2026/27 permit requirement', ye=0, one=639, eng='yes', entry='direct', entryt='CBSE: five subjects each B1 or better; ISC: 75% in each; Maths required.',
        sat='Not required', exam='Numerus fixus selection (maths and reasoning)', iv='None stated', ielts='6.5 or 7.0 (official pages differ)', lang='None identified for English tracks', win=[['2026-12-01', '2027-01-15', 'Numerus fixus (CS, Aerospace)'], ['2026-12-01', '2027-04-01', 'Other programmes']], due='2027-01-15', dueL='15 Jan 2027 (CS, Aerospace)', roi=48000,
        sch='None verified for non-EU bachelors', cls='Mild, windy, often rainy', nri='Popular with Indian families wanting English teaching in continental Europe; the early January deadline catches many out.',
        S=['QS 48, THE 50', 'Direct CBSE/ISC entry'], W=['Rooms for under 45% of new internationals', 'No bachelor scholarship found'], O=['English CS track of 345 places in 2027-28', 'Orientation year for job search'], T=['Selective numerus fixus', 'Rent EUR 500-1,350']),
    'Eindhoven University of Technology': U('tue', 'TU Eindhoven', 'NL', 51.448, 5.490, yrs=3, tui=22400, tuin='2027-28 non-EEA fee', live=14400, liven='TU/e estimate of required funds', ye=0, one=354, eng='yes', entry='direct', entryt='CBSE: five subjects all A1-B1; ISC: 75% overall and 70% in required subjects.',
        sat='Not required', exam='CSE online selection day, 6 Mar 2027', iv='None stated', ielts='6.5 (6.0 each)', lang='None for most programmes', win=[['2026-10-01', '2027-01-15', 'Numerus fixus'], ['2026-10-01', '2027-05-01', 'Other programmes']], due='2027-01-15', dueL='15 Jan 2027 (CSE, Mechanical)', roi=48000,
        sch='None verified', cls='Mild, grey winters', nri='A strong tech-campus option, but the July 2026 announcement about international bachelor recruitment makes families cautious. Confirm with TU/e before applying.',
        S=['Widest English engineering choice here', 'Industry-rich Brainport region'], W=['EUR 22,700 guarantee fee paid in advance', 'No housing guarantee'], O=['Direct entry from CBSE/ISC', 'Orientation year'], T=['Announced end of international bachelor recruitment (no start year given)', 'Announced non-EEA fee rise']),
    'ETH Zurich': U('eth', 'ETH Zurich', 'CH', 47.376, 8.548, yrs=3, tui=4380, tuin='CHF 2,190 per semester', live=26650, liven='Midpoint of ETH total-cost sheet (includes some fees)', ye=138, one=550, eng='none', entry='indirect', entryt='Entrance exam in German for CBSE/ISC. January 2027 registration closed 15 Oct 2026, so exam-route students start no earlier than September 2028.',
        sat='Not used', exam='ETH Entrance Examination (CHF 550/800)', iv='None stated', ielts='Not applicable', lang='German C1 by 31 March', win=[['2026-12-01', '2027-03-31', 'Application (direct-qualified only)'], ['2027-09-15', '2027-10-15', 'Exam registration for 2028 (expected pattern)']], due='2027-03-31', dueL='Exam route: next start Sept 2028', roi=85000,
        sch='None verified', cls='Cold winters, warm summers', nri='Admired as Europe’s top technical university; rarely practical straight after Class 12 for a Gulf-schooled student without German.',
        S=['QS joint 8th, THE 12th', 'Low tuition for the rank'], W=['German-only bachelors', 'High living costs'], O=['Defined exam route for Indian certificates', 'High Swiss graduate pay'], T=['2027 start closed for exam route', '10-year settlement period']),
    'EPFL (Ecole polytechnique federale de Lausanne)': U('epfl', 'EPFL', 'CH', 46.519, 6.567, yrs=3, tui=4380, tuin='CHF 2,190 per semester (confirm; older pages differ)', live=29000, liven='EPFL advice', ye=0, one=700, eng='none', entry='indirect', entryt='No direct entry on an Indian certificate: entrance exam or CMS preparatory year (India’s CMS eligibility unverified).',
        sat='Not used', exam='EPFL entrance exam, science papers 18-22 Jan 2027', iv='None stated', ielts='Not applicable', lang='French B2 (C1 advised)', win=[['2026-10-01', '2026-12-01', 'Entrance exam registration'], ['2026-11-15', '2027-04-30', 'Online application']], due='2026-12-01', dueL='Exam registration closes 1 Dec 2026', roi=85000,
        sch='None verified', cls='Lake climate; cool winters', nri='Considered mainly by French-speaking families. The exam and teaching are French-medium.',
        S=['QS joint 22nd, THE 36th', 'Passing the exam guarantees a place'], W=['French-medium', 'First-year places capped'], O=['Open exam route for non-EU certificates', 'Strong research campus'], T=['Very short registration window', 'CHF 29,000 living costs']),
    'Imperial College London': U('imperial', 'Imperial', 'GB', 51.499, -0.175, yrs=4, tui=47800, tuin='2027 overseas fee seen on EEE, Mechanical and some Computing pages', live=22700, liven='About GBP 1,890 a month', ye=776, one=593, eng='yes', entry='direct', entryt='90% minimum in CBSE/ISC; 95% for Electrical Engineering.',
        sat='Not a stated route', exam='TMUA (Computing), ESAT (EEE)', iv='Sometimes', ielts='6.5 or 7.0 by course', lang='None beyond English', win=[['2026-05-12', '2027-01-13', 'UCAS equal consideration'], ['2026-11-28', '2027-02-05', 'Imperial Inspires scholarship']], due='2027-01-13', dueL='13 Jan 2027 (UCAS)', roi=45000,
        sch='Imperial Inspires GBP 15,000 a year (one page conflicts)', cls='Mild, cloudy', nri='The top aspiration for high-scoring NRI students; families weigh the name against a total near US$ 370,000.',
        S=['QS joint 2nd, THE 8th', 'Integrated MEng'], W=['Highest cost in this list', '95% bar for some courses'], O=['Large overseas scholarship round', 'London employers'], T=['18-month Graduate visa from 2027', 'Settlement now 10 years']),
    'University of Edinburgh': U('edinburgh', 'Edinburgh', 'GB', 55.947, -3.188, yrs=4, tui=36800, tuin='NOT the 2027 fee: 2026 indicative laboratory-degree level used', live=18552, liven='2026-27 full-year estimate', ye=776, one=593, eng='yes', entry='direct', entryt='80% overall and in required subjects (85% for some); CBSE Applied Maths not counted.',
        sat='Not required', exam='None found', iv='None found', ielts='6.5 (5.5 each)', lang='None beyond English', win=[['2026-05-12', '2027-01-13', 'UCAS equal consideration']], due='2027-01-13', dueL='13 Jan 2027 (UCAS)', roi=40000,
        sch='No India engineering/CS award found', cls='Cool, windy, often wet', nri='A well-liked, safe-city choice with an accessible 80% threshold for a top-40 university.',
        S=['QS 35th, THE joint 29th', 'First-year housing guarantee'], W=['4-year degree adds a year of cost', '2027/28 fee not retrieved'], O=['Informatics breadth including AI', 'Advanced entry to year 2 at 85%'], T=['18-month Graduate visa', 'Limited scholarships']),
    'University of Manchester': U('manchester', 'Manchester', 'GB', 53.467, -2.234, yrs=3, tui=39700, tuin='BSc Computer Science 2027/28; may rise up to 7% a year', live=16590, liven='41-week estimate including flights, health surcharge taken out and counted separately', ye=776, one=593, eng='yes', entry='direct', entryt='Computer Science: 90% overall, 90% Maths, 85% Physics or CS; foundation year from 70%.',
        sat='Not required', exam='No test for BSc CS', iv='Not mentioned', ielts='6.5 (EEE 7.0)', lang='None beyond English', win=[['2026-05-12', '2027-01-13', 'UCAS equal consideration'], ['2026-11-28', '2027-03-30', 'Global Futures scholarship']], due='2027-01-13', dueL='13 Jan 2027 (UCAS)', roi=38000,
        sch='GBP 36,000 Global Futures for India-domiciled students', cls='Mild, rainy', nri='Strong Indian-student city. Note the headline scholarship needs India domicile, so Gulf-based NRI families may not qualify.',
        S=['QS joint 40th', 'Clear India thresholds'], W=['Fee can rise 7% a year', 'Scholarship covers 3 years only'], O=['Foundation route', 'Large employer market'], T=['NRI domicile may exclude the scholarship', '18-month Graduate visa']),
    'Trinity College Dublin': U('trinity', 'Trinity Dublin', 'IE', 53.344, -6.257, yrs=4, tui=30450, tuin='2027/28 first-year fee, CS and Engineering', live=24500, liven='Midpoint of EUR 19,937-29,050', ye=300, one=115, eng='yes', entry='direct', entryt='Competitive average 85 for CS, 75 for Engineering; born before 15 Jan 2011.',
        sat='US curriculum only', exam='None', iv='None stated', ielts='6.5 (6.0 each)', lang='None for this route', win=[['2026-11-01', '2027-02-01', 'Priority date'], ['2027-02-02', '2027-06-30', 'Final deadline']], due='2027-02-01', dueL='1 Feb 2027 priority', roi=45000,
        sch='India award EUR 3,000-5,000, first year (check eligibility)', cls='Mild, wet', nri='Valued for English-speaking Europe and a European tech-company base; housing is the complaint heard most.',
        S=['QS 75th', 'Published India entry bands'], W=['Costly, unguaranteed housing', 'General excellence award excludes CS and engineering'], O=['Dublin tech employers', 'Graduate stay-back permit'], T=['Student years do not count for residency', 'Rent pressure']),
    'University College Dublin': U('ucd', 'UC Dublin', 'IE', 53.308, -6.224, yrs=4, tui=None, tuin='2027/28 non-EU fee not retrieved', live=22000, liven='Estimate from 2026 monthly figures', ye=300, one=130, eng='yes', entry='direct', entryt='Best five 80%; Engineering needs 85% Maths and a lab science (possible maths test).',
        sat='Not stated', exam='OMPT-D pilot for Engineering (check)', iv='None found', ielts='Not verified (80% Class XII English accepted)', lang='None beyond English', win=[['2026-11-28', '2027-03-31', 'Global Excellence scholarship (date inferred)']], due='2027-03-31', dueL='Rolling; scholarship about 31 Mar', roi=43000,
        sch='100% or 50% tuition Global Excellence', cls='Mild, wet', nri='A friendly-campus alternative to Trinity with a lower mark bar.',
        S=['QS joint 100th', 'Large tuition scholarships'], W=['Fee not published in what we read', 'No housing guarantee'], O=['93% in work or study at 9 months', 'Dublin tech employers'], T=['Dublin rent', 'Short bachelor stay-back']),
    'École Polytechnique (Institut Polytechnique de Paris), Bachelor of Science': U('x', 'Polytechnique', 'FR', 48.714, 2.210, yrs=3, tui=19600, tuin='2027 intake', live=12000, liven='School estimate including housing', ye=283, one=155, eng='yes', entry='direct', entryt='School certificate with advanced maths plus an advanced science; selective interview.',
        sat='Not required', exam='No separate test', iv='About 50 min online, shortlisted', ielts='6.5 (6.0 each)', lang='French B2 to graduate', win=[['2026-10-21', '2027-01-06', 'Round 2'], ['2027-01-07', '2027-02-08', 'Round 3']], due='2027-01-06', dueL='Round 2: 6 Jan 2027', roi=48000,
        sch='Excellence and Women in Science EUR 4,800 a year; Olympiad award', cls='Paris region; cool grey winters', nri='Less known among families than UK names, yet a very selective Maths-CS route with guaranteed housing.',
        S=['Guaranteed campus housing', 'English-taught Maths and CS'], W=['Narrow programme choice', 'Heavy workload leaves no room for jobs'], O=['Research internship in year 3', 'Merit scholarships'], T=['Post-study stay unclear after bachelor alone', 'French requirement']),
    'Politecnico di Milano': U('polimi', 'PoliMi', 'IT', 45.478, 9.227, yrs=3, tui=3943, tuin='2026/27 maximum', live=11040, liven='Midpoint of university monthly ranges', ye=0, one=0, eng='limited', entry='conditional', entryt='12 years of school plus TOL, CEnT-S or SAT; Universitaly pre-enrolment; reserved non-EU places.',
        sat='Accepted instead of TOL', exam='TOL / TOLC-I / CEnT-S / SAT', iv='None', ielts='5.0', lang='Italian obligation before graduating', win=[['2027-05-01', '2027-07-31', '2027/28 phases from May (dates pending)']], due='2027-05-01', dueL='Opens May 2027', roi=33000,
        sch='Need and merit based DSU grant', cls='Hot summers, foggy winters', nri='Attractive on price and ranking; families need to check the English programme is the one the student wants.',
        S=['QS 87', 'Fees capped near EUR 3,943'], W=['No English computer engineering bachelor found', 'Limited residences'], O=['93% employment for Italian bachelor leavers', 'SAT route'], T=['Timeline published late', 'Visa pre-enrolment deadlines']),
    'University of Bologna': U('bologna', 'Bologna', 'IT', 44.497, 11.353, yrs=3, tui=6000, tuin='Planning ceiling from a search summary; reduced fee of EUR 1,157 is conditional', live=9600, liven='Estimate from room and grocery figures', ye=700, one=0, eng='none', entry='conditional', entryt='Engineering and CS bachelors are in Italian; TOLC test; Universitaly pre-enrolment.',
        sat='Some programmes only', exam='TOLC-I', iv='None', ielts='Not verified', lang='Italian (visa may need B2)', win=[['2027-04-01', '2027-07-21', 'Expected pattern; 2027/28 call pending']], due='2027-07-21', dueL='Call not yet published', roi=30000,
        sch='ER.GO grant, housing and meals', cls='Hot summers, foggy winters', nri='Appeals on cost and student-city life, mostly to students ready to study in Italian.',
        S=['Low cost', 'Historic student city'], W=['No English engineering/CS bachelor found', 'No guaranteed housing'], O=['Need-based support', 'Reduced fee for eligible nationals'], T=['Language barrier', 'Late calls']),
    'IE University': U('ie', 'IE University', 'ES', 40.953, -4.121, yrs=4, tui=27300, tuin='2027-28 first year; one-off IE Foundation EUR 1,200', live=13200, liven='Planning estimate from Segovia ranges', ye=0, one=1350, eng='yes', entry='direct', entryt='80% average; legalised Indian documents.',
        sat='Optional: 1300+, Math 700', exam='IE test or SAT/ACT', iv='Selected candidates', ielts='7.0', lang='None stated', win=[['2026-11-07', '2027-01-15', 'Round 2'], ['2027-01-16', '2027-03-05', 'Round 3']], due='2027-01-15', dueL='Round 2: 15 Jan 2027', roi=32000,
        sch='Merit and need awards 10-60%', cls='Hot dry summers, cold winters', nri='Chosen for small English classes and business-tech mix; priced like a premium private university.',
        S=['English CS and AI', 'Rolling rounds'], W=['High fee', 'QS 446'], O=['Awards up to 60%', '95% employability (self-reported)'], T=['Post-study rule conflicting', 'Document legalisation time']),
    'Aalto University': U('aalto', 'Aalto', 'FI', 60.186, 24.828, yrs=3, tui=12000, tuin='Technology fields', live=9600, liven='Minimum EUR 800 a month', ye=0, one=700, eng='yes', entry='direct', entryt='SAT 1350+ with Math 700, or ACT 29/30.',
        sat='Required: 1350, Math 700', exam='SAT or ACT', iv='None', ielts='Not required on this route', lang='None stated', win=[['2027-01-07', '2027-01-22', 'Application'], ['2027-01-23', '2027-01-29', 'Scores due']], due='2027-01-22', dueL='7-22 Jan 2027', roi=42000,
        sch='Merit tuition waiver; 25% first-year early bird', cls='Long dark winters', nri='A rising choice for SAT-prepared Gulf students; winter and the narrow window deter some.',
        S=['Six English tech bachelors', 'No English test on SAT route'], W=['Few places', 'No housing guarantee'], O=['2-year job-search permit', 'Merit waivers'], T=['Two-week window', 'Changed PR rules']),
    'KTH Royal Institute of Technology': U('kth', 'KTH', 'SE', 59.350, 18.070, yrs=3, tui=151000, tuin='SEK 453,000 for the programme', live=153204, liven='Midpoint of exchange-student estimate', ye=0, one=2400, eng='limited', entry='conditional', entryt='Grades only, no predicted-grade offers; documents due 1 Feb 2027, so ask whether a current Class 12 student can compete.',
        sat='Not used', exam='None', iv='None', ielts='6.5 (CBSE/ISC English may suffice)', lang='None for ICT', win=[['2026-10-16', '2027-01-15', 'Round 1'], ['2027-01-16', '2027-02-01', 'Documents and fee']], due='2027-01-15', dueL='15 Jan 2027', roi=45000,
        sch='None for bachelors', cls='Cold, dark winters', nri='Respected, but realistically suited to students who already hold final results.',
        S=['QS 82', 'First-year housing guarantee'], W=['One English bachelor', 'No scholarships'], O=['Stockholm tech scene', '97% in employment (older cohorts)'], T=['About 10% admitted in 2024', 'Class 12 timing']),
    'Technical University of Denmark (DTU)': U('dtu', 'DTU', 'DK', 55.786, 12.523, yrs=3, tui=15000, tuin='Per academic year', live=11923, cur='EUR', liven='Immigration funds level of DKK 7,426 a month, shown in euros (no university figure)', ye=0, one=509, eng='limited', entry='conditional', entryt='Maths A, Physics B, Chemistry B equivalence; ask for pre-assessment.',
        sat='Not used', exam='None stated', iv='None', ielts='6.5 (required for Indians)', lang='None for General Engineering', win=[['2027-02-01', '2027-03-15', 'Application']], due='2027-03-15', dueL='15 Mar 2027', roi=50000,
        sch='None for bachelors', cls='Cool, windy', nri='Quietly strong; offers arrive late (28 July), which squeezes visa and housing.',
        S=['QS 105', 'Broad engineering BSc'], W=['One English bachelor', 'No scholarships'], O=['Good engineering employment', 'Group-project teaching'], T=['Job-search permit cut', '8-year residency rule']),
}

TOP_ISSUES = {  # top three issues parents should weigh
    'tum': ['Class 12 alone rarely gives direct entry', 'German needed even for English courses', 'Munich housing'],
    'rwth': ['German C1 for every bachelor', 'Non-EU quota', 'Class 12 recognition route'],
    'delft': ['15 January selective deadline', 'Housing for under 45% of newcomers', 'B1 in every CBSE subject'],
    'tue': ['Announced end of international bachelor recruitment', 'EUR 22,700 advance guarantee fee', 'No housing guarantee'],
    'eth': ['2027 closed for exam-route students', 'German C1', 'Cost of living'],
    'epfl': ['Registration closes 1 December 2026', 'French-medium exam and teaching', 'Capped places'],
    'imperial': ['90-95% marks plus TMUA/ESAT', 'Very high cost', 'Scholarship pages conflict'],
    'edinburgh': ['2027/28 fee not confirmed', 'Four years of cost', 'Few engineering scholarships'],
    'manchester': ['90% bar for Computer Science', 'Fee escalation up to 7%', 'Scholarship needs India domicile'],
    'trinity': ['Dublin rent and no guarantee', 'Subject and age rules', 'Small first-year-only award'],
    'ucd': ['Fee not yet confirmed', 'Housing', 'Possible maths test'],
    'x': ['Very selective', 'French B2 to graduate', 'Post-study route unclear'],
    'polimi': ['Limited English options', 'Late 2027 dates', 'Italian obligation'],
    'bologna': ['Italian-taught engineering', 'Fee category must be checked', 'Private rental search'],
    'ie': ['Premium fees', 'IELTS 7.0', 'Legalising documents'],
    'aalto': ['Two-week application window', 'High SAT bar for few places', 'Winter and housing'],
    'kth': ['Class 12 timing risk', 'Very competitive', 'No scholarship'],
    'dtu': ['Subject-level equivalence', 'No scholarship', 'Late offers'],
}

assert set(OV) == set(raw), set(OV) ^ set(raw)


def txt(x):
    if isinstance(x, dict):
        return x.get('text') or x.get('statistic') or x.get('amount_text')
    return x


unis = []
for name, o in OV.items():
    r = raw[name]
    cur = o.get('cur') or CUR[o['iso']]
    fx = FX[cur]
    usd = lambda v: None if v is None else round(v * fx)  # noqa: E731
    tu, lv = usd(o['tui']), usd(o['live'])
    ye, one = usd(o['ye']), usd(o['one'])
    total = None if tu is None else (tu + lv + ye) * o['yrs'] + one
    alumni = r.get('alumni') or []
    d = dict(o)
    d.update(
        name=name.replace(', Bachelor of Science', ''), city=r['city'], cur=cur, tuiU=tu, liveU=lv, oneU=one, yeU=ye, totalU=total,
        roiU=usd(o['roi'] if cur == 'EUR' else None) if cur == 'EUR' else None,
        qs=r.get('qs_rank'), the=r.get('the_rank'), web=r.get('website'), adm=r.get('admissions_url'),
        feeurl=(r.get('tuition_non_eu') or {}).get('url'), liveurl=(r.get('living_cost') or {}).get('url'),
        progs=r.get('programmes_english') or [], teach=r.get('teaching_language_bachelor'),
        elig=r.get('eligibility_cbse'), other=r.get('other_requirements'), app=r.get('application') or {},
        fees_other=r.get('other_fees'), living_text=(r.get('living_cost') or {}).get('amount_text'),
        schol=r.get('scholarships') or [], hostel=r.get('hostel') or {}, place=r.get('placement_employability'),
        alumni=alumni, sources=r.get('sources') or [], notes=r.get('notes'), tests=r.get('tests') or {}, issues=TOP_ISSUES[o['key']])
    del d['roiU']
    unis.append(d)

countries = []
for iso, c in C.items():
    o = CO[iso]
    fx = FX[CUR[iso]]
    funds = None if o['funds'] is None else round(o['funds'] * o['fundsper'] * fx)
    fee = None if o['fee'] is None else round(o['fee'] * fx)
    countries.append(dict(
        iso=iso, iso3=o['iso3'], name=c['country'], color=o['flagc'], cur=CUR[iso], psw=o['psw'], pswt=o['pswt'], pr=o['pr'], prt=o['prt'], work=o['work'],
        fundsU=funds, fundsT=(c['student_visa']['proof_of_funds'] or {}).get('amount_text'), feeU=fee, feeT=c['student_visa'].get('fee'),
        visa=c['student_visa']['name'], reqs=c['student_visa']['key_requirements'], visaurl=c['student_visa'].get('url'),
        workurl=(c.get('work_during_study') or {}).get('url'), pswurl=(c.get('post_study_work') or {}).get('url'), prurl=(c.get('pr_route') or {}).get('url'),
        health=(c.get('health_insurance') or {}).get('text'), india=(c.get('india_specific') or {}).get('text'), indiaurl=(c.get('india_specific') or {}).get('url'),
        climate=c.get('climate', '').replace('General knowledge: ', ''), culture=c.get('culture_note', '').replace('General knowledge: ', ''),
        nri=(c.get('nri_note') or {}).get('text'), sources=c.get('sources') or []))

data = dict(unis=unis, countries=countries, fx=FX, fxdate=CT['fx']['date'], fxurl=CT['fx']['url'], inr=round(INR_PER_USD, 2), checked='2026-11-28')
blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
page = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read().replace('/*DATA*/null', blob)
# a complete light-theme document: the portal serves it sandboxed inside its own page
head, body = page.split('</style>', 1)
page = '\n'.join(['<!doctype html>', '<html lang="en" data-theme="light">', '<head>', '<meta charset="utf-8">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1">', head + '</style>', '</head>', '<body>' + body, '</body>', '</html>', ''])
out = os.path.normpath(os.path.join(HERE, '..', '..', 'app', 'data', 'europe', 'atlas.html'))
with open(out, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(page)
print('written', out, len(page.encode('utf-8')), 'bytes', len(unis), 'universities')
for u in sorted(unis, key=lambda u: (u['totalU'] is None, u['totalU'] or 0)):
    print(f"  {u['short']:16} tuition/yr {u['tuiU']}  living/yr {u['liveU']}  programme {u['totalU']}")
