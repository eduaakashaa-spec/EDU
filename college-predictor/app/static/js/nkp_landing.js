/* Neikkarapatti & Palani landing page: language toggle (English / Tamil), code check, validation, registration. */

(function () {
  "use strict";

  /* ---------- CONFIG ----------
     The form posts to the portal (same origin). If the network fails the details are handed to WhatsApp instead, so nothing is lost. */
  var CONFIG = {
    endpoint: "/neikkarapatti-palani/register",
    whatsapp: "918015722706",
    code: "NKP",
    campaign: "NKP-Neikkarapatti-Palani-2027",
    siteUrl: "https://www.eduaakashaa.com/neikkarapatti-palani"
  };

  /* ---------- Tamil copy ---------- */
  var TA = {
    ann_k: "சிறப்பு அறிவிப்பு", ann_t: "நெய்க்காரப்பட்டி, பழனி 12-ஆம் வகுப்பு மாணவர்களுக்கு இலவச Membership · குறியீடு NKP", ann_b: "இப்போதே பதிவு செய்யுங்கள்",
    n_story: "எங்கள் வேர்கள்", n_portal: "Portal நன்மைகள்", n_how: "Claim செய்ய", n_faq: "FAQ",
    n_cta: "Membership பெறுங்கள்",
    h_eye: "நெய்க்காரப்பட்டி, பழனி · Class of 2027",
    h_h1: 'நாங்களும் இங்கே படித்தவர்கள். உங்களுக்கு <span class="highlight">Complimentary</span> Membership.',
    h_lead: 'EduAakashaa-வின் Founders பழனி, நெய்க்காரப்பட்டியில் உள்ள Schools-ல் படித்தவர்கள். இந்த ஊருக்குத் திருப்பிக் கொடுக்கும் விதமாக, 2027-ல் <strong>NEET, JEE அல்லது TNEA</strong> Admissions-க்குத் தயாராகும் ஒவ்வொரு Grade 12 student-க்கும் EduAakashaa Portal-ல் Complimentary Membership வழங்குகிறோம்.',
    h_cta1: "Membership பெறுங்கள்", h_cta2: "Portal-ல் என்ன கிடைக்கும் என்று பாருங்கள்",
    h_note: "Registration form-ல் NKP Code உள்ளிடுங்கள்",
    c_label: "உங்கள் School Code", c_copy: "Code-ஐ Copy செய்யுங்கள்",
    c_l1: "தகுதியான Students-க்கு Complimentary Portal access",
    c_l2: "பழனி, நெய்க்காரப்பட்டி Schools-ன் Grade 12 students-க்கு",
    c_l3: "NEET, JEE, TNEA 2027 Admissions-க்கு",
    c_l4: "Registration செய்ய சுமார் இரண்டு நிமிடங்கள் ஆகும்",
    s1: "தகுதியான Students-க்கு Membership fee", s2: "Covered · NEET, JEE, TNEA",
    s3: "Admission year · Grade 12 batch", s4: "Form-ல் உள்ளிட வேண்டிய Code",
    st_eye: "எங்கள் வேர்கள் · ஏன் இந்த Offer",
    st_h2: 'நாங்களும் படித்தது <em>இதே Schools-ல்</em>',
    st_p1: "இந்தியாவில் College Admissions ஒரு புதிர்ப்பாதை: Entrance exams, Rank, Counselling rounds, Choice filling. சிறிய ஊர்களில் உள்ள குடும்பங்கள் பெரும்பாலும் Guide இல்லாமல் இதைக் கடக்க வேண்டியுள்ளது.",
    st_p2: "எங்கள் Founders பழனி, நெய்க்காரப்பட்டி Schools-ல் படித்தவர்கள்; அதனால் இது எங்களுக்கு மிகவும் நெருக்கமானது. 2027-ல் இங்குள்ள ஒவ்வொரு Grade 12 student-க்கும் ஒரு Guide இருக்க வேண்டும் என்பதே எங்கள் விருப்பம்.",
    e_title: "யார் Claim செய்யலாம்",
    e1: "2026–27-ல் Grade 12 படிப்பவர்",
    e2: "பழனி, நெய்க்காரப்பட்டியில் உள்ள School student",
    e3: "2027-ல் NEET, JEE மற்றும்/அல்லது TNEA Admissions-க்குத் தயாராகுபவர்",
    e4: "Parent அல்லது Guardian-க்குத் தெரிந்து Register செய்பவர்",
    e_note: "நீங்கள் வழங்கும் Details உங்கள் School-உடன் சரிபார்க்கப்படலாம்.",
    pc_cap: "Palani · Tamil Nadu",
    pc_k: "எங்கள் வேர்கள் · நெய்க்காரப்பட்டி, பழனி",
    pc_h: 'Palani Schools-ல் இருந்து உங்கள் <em>Future</em>-க்கு',
    pc_p: "எங்கள் Founders பழனி, நெய்க்காரப்பட்டி Schools-ல் படித்தவர்கள். எங்களுக்குக் கற்றுக்கொடுத்த இந்த மண்ணுக்குத் திருப்பிக் கொடுக்கும் வழி தான் இந்த Complimentary Membership.",
    p_eye: "Portal · என்ன கிடைக்கும்",
    p_h2: 'உங்கள் <em>2027 Admissions</em>-ஐத் திட்டமிட ஒரே இடம்',
    p_sub: "EduAakashaa Portal ஒவ்வொரு Member-க்குமான private online space. Exams, Rank, Colleges பற்றித் தெளிவு தேடும் Students-க்கும், உடன் இருந்து பார்க்க விரும்பும் Parents-க்கும் ஏற்றது. Phone browser-லேயே வேலை செய்யும்.",
    f1t: "Mock tests & Assessments", f1d: "நீங்கள் எங்கே இருக்கிறீர்கள் என்று பாருங்கள். எந்த Concepts உறுதியாக உள்ளன, எவை weak என்பதை Assessments காட்டும்; உங்கள் நேரம் தேவையான இடத்தில் செலவாகும்.",
    f2t: "Branch & Stream guidance", f2d: "Popular என்பதற்காக அல்லாமல், உங்கள் Strengths மற்றும் Interests-க்குப் பொருந்தும் Branch அல்லது Stream குறித்த Personalised advice.",
    f3t: "Rank & College reports", f3d: "உங்கள் Rank-க்கு எந்த Colleges, Branches realistic என்பதை, அதற்கான Data-வுடன் காட்டும் Reports.",
    f4t: "Exam dates & Reminders", f4d: "NEET, JEE, TNEA Dates ஒரே Schedule-ல். Phone calendar-ல் சேர்க்கலாம்; Parents-உடன் WhatsApp-ல் Share செய்யலாம்.",
    f5t: "Document vault", f5d: "Marksheets, Certificates, Admission documents-ஐ ஒரே பாதுகாப்பான இடத்தில் வைத்திருங்கள்; Counselling தொடங்கும்போது ready-ஆக இருக்கும்.",
    f6t: "Team-இடமிருந்து Updates", f6d: "Announcements, Deadlines, Counsellor updates; எந்த Date-உம் தவறாது.",
    pn_k: "Parents-க்கு", pn_p: "எல்லாம் எளிய மொழியில் இருப்பதால், உங்கள் பிள்ளையுடன் சேர்ந்து Plan-ஐப் பின்தொடரலாம்.",
    hw_eye: "Claim செய்வது எப்படி · 3 Steps",
    hw_h2: 'மூன்று Steps. <em>இரண்டு நிமிடங்கள்.</em>',
    hw1t: "Registration form-ஐத் திறக்கவும்", hw1d: "இந்தப் பக்கத்தின் கீழேயே உள்ளது. உங்கள் Name, School, நீங்கள் தயாராகும் Admissions ஆகியவற்றை நிரப்பவும்.",
    hw2t: "NKP Code-ஐ உள்ளிடவும்", hw2d: "Code box-ல் NKP என்று type செய்யவும். Accept ஆனால் Green tick தெரியும்.",
    hw3t: "Submit செய்து Access பெறுங்கள்", hw3d: "எங்கள் Team உங்கள் Details-ஐ confirm செய்து, Portal login-ஐப் பகிரும்.",
    hw_cl: "உங்கள் Code", hw_cn: "இதே போல் type செய்யவும்: N · K · P",
    r_eye: "Registration · Complimentary",
    r_h2: 'உங்கள் Complimentary <em>Membership</em>-ஐப் பெறுங்கள்',
    r_sub: "Form-ஐ நிரப்பி, Code box-ல் NKP என்று உள்ளிடவும். சுமார் இரண்டு நிமிடங்கள் ஆகும்.",
    r_help: "Help வேண்டுமா? Call அல்லது WhatsApp செய்யவும்",
    f_name: "Student-ன் முழுப் பெயர்", f_school: "School name", f_school_ph: "பழனி, நெய்க்காரப்பட்டியில் உள்ள School",
    f_stream: "Stream / Group", o_sel: "Select செய்யவும்",
    o_pcm: "PCM (Physics, Chemistry, Maths)", o_pcb: "PCB (Physics, Chemistry, Biology)", o_pcmb: "PCMB (நான்கும்)", o_oth: "Other",
    f_mobile: "Student-ன் Mobile (WhatsApp)",
    f_exams: "2027-ல் நீங்கள் தயாராகும் Admissions",
    f_email: "Email", f_email_h: "உங்கள் Portal login இங்கு அனுப்பப்படும். உங்களிடம் இல்லையெனில் Parent-ன் Email கொடுக்கவும்.",
    f_parent: "Parent / Guardian name", f_pmobile: "Parent / Guardian mobile", f_opt: "(optional)",
    f_lang: "Guidance-க்கு விருப்ப மொழி", l_ta: "Tamil", l_en: "English",
    f_code: "Offer code", f_code_ph: "Code உள்ளிடவும்", f_use: "Use NKP",
    f_consent: "நான் Register செய்வது என் Parent/Guardian-க்குத் தெரியும்; என் Complimentary Membership குறித்து EduAakashaa WhatsApp, Phone அல்லது Email-ல் என்னைத் தொடர்புகொள்ள ஒப்புக்கொள்கிறேன்.",
    f_submit: "Submit செய்து Membership பெறுங்கள்",
    f_note: "பழனி, நெய்க்காரப்பட்டியின் தகுதியான Grade 12 students-க்கு Complimentary. உங்கள் Details Membership அமைக்கவும் வழிகாட்டவும் பயன்படுத்தப்படும்.",
    q_eye: "FAQ · Students & Parents",
    q_h2: 'Families <em>கேட்கும் Questions</em>',
    q1e: "Q·01 · Students-க்கு", q1: "Complimentary Membership-ஐ யார் Claim செய்யலாம்?",
    a1: "பழனி, நெய்க்காரப்பட்டியில் உள்ள Schools-ல் தற்போது Grade 12 (2026–27) படிக்கும், 2027-ல் NEET, JEE மற்றும்/அல்லது TNEA Admissions-க்குத் தயாராகும் Students.",
    q2e: "Q·02 · Students-க்கு", q2: "NKP Code-ஐ எங்கே உள்ளிட வேண்டும்?",
    a2: "இந்தப் பக்கத்தில் உள்ள Registration form-ன் “Offer code” box-ல் NKP என்று type செய்யவும். Green tick தெரியும்.",
    q3e: "Q·03 · Parents-க்கு", q3: "Membership உண்மையிலேயே Complimentary-யா?",
    a3: "ஆம். NKP Code-உடன் Register செய்யும் தகுதியான Students-க்கு Membership Complimentary. Register செய்ய எந்தக் கட்டணமும் இல்லை.",
    q4e: "Q·04 · Parents-க்கு", q4: "இது School அல்லது Coaching classes-க்கு மாற்றா?",
    a4: "இல்லை. Admissions-க்கான Structure, Assessments, Data, Guidance-ஐ Portal கூடுதலாகத் தருகிறது. உங்கள் பிள்ளையின் Preparation-உம் School, Coaching classes-உம் வழக்கம்போல் தொடரும்.",
    q5e: "Q·05 · Parents-க்கு", q5: "Rank அல்லது Seat Guarantee உண்டா?",
    a5: "இல்லை; அப்படி Promise செய்பவர்களிடம் எச்சரிக்கையாக இருங்கள். உங்கள் பிள்ளை சிறப்பாகத் தயாராகவும், சரியாகத் தேர்வு செய்யவும் உதவுவோம்; Exam-உம் உழைப்பும் அவர்களுடையது.",
    q6e: "Q·06 · Students-க்கு", q6: "Laptop தேவையா?",
    a6: "தேவையில்லை. Portal Phone browser-ல் வேலை செய்யும். நீண்ட Reports-க்கு Laptop உதவும்; ஆனால் கட்டாயமில்லை.",
    q7e: "Q·07 · Students-க்கு", q7: "நான் Grade 11, அல்லது என் School பழனி, நெய்க்காரப்பட்டிக்கு வெளியே உள்ளது. சேரலாமா?",
    a7: "இந்த Offer பழனி, நெய்க்காரப்பட்டி Schools-ன் Grade 12 students-க்கானது. மற்ற Options அறிய info@eduaakashaa.com-க்கு எழுதவும் அல்லது Call செய்யவும்.",
    sh_h: "பழனி, நெய்க்காரப்பட்டியைச் சேர்ந்த Grade 12 student-ஐ உங்களுக்குத் தெரியுமா?",
    sh_p: "இந்தப் பக்கத்தை அவர்களுக்கு அனுப்புங்கள். இந்த Offer Class of 2027 அனைவருக்கும்.",
    sh_wa: "WhatsApp-ல் Share செய்க", sh_copy: "Message-ஐ Copy செய்க",
    /* dynamic */
    copied: "Copied", copy_fail: "Copy செய்ய முடியவில்லை",
    e_req: "இந்த Field அவசியம்", e_mobile: "சரியான 10 digit Mobile number உள்ளிடவும்",
    e_email: "சரியான Email address உள்ளிடவும்", e_exam: "குறைந்தது ஒன்றைத் தேர்வு செய்யவும்",
    e_consent: "தொடர Tick செய்யவும்", e_code: "NKP என்ற Code-ஐ உள்ளிடவும்",
    code_hint: "பழனி, நெய்க்காரப்பட்டி Schools-க்கான Code: NKP",
    code_ok: "NKP Code Accept ஆனது. பழனி, நெய்க்காரப்பட்டி Grade 12 students-க்கு Complimentary Membership.",
    code_bad: "இந்த Offer-க்கு இந்த Code செல்லாது. NKP என்று உள்ளிடவும்.",
    sending: "Submit ஆகிறது…",
    ok_t: "Registration முடிந்தது", ok_p: "நன்றி, {name}. எங்கள் Team உங்கள் Details-ஐ confirm செய்து, Portal login-ஐ WhatsApp அல்லது Email-ல் பகிரும்.",
    wa_t: "ஒரு கடைசி Step", wa_p: "உங்கள் Details ready, {name}. Complimentary access activate ஆக, அவற்றை WhatsApp-ல் எங்களுக்கு அனுப்பவும்.",
    wa_fail: "தானாக Submit செய்ய முடியவில்லை. தயவுசெய்து WhatsApp-ல் அனுப்பவும்.",
    wa_btn: "WhatsApp-ல் அனுப்புக", copy_det: "Details Copy செய்க", edit: "Edit செய்க",
    share_msg: "பழனி, நெய்க்காரப்பட்டி Schools-ன் Grade 12 students-களே (Class of 2027): NEET / JEE / TNEA Guidance-க்கு EduAakashaa Complimentary Membership வழங்குகிறது. NKP Code-உடன் Register செய்யுங்கள்:"
  };

  var EN = {
    copied: "Copied", copy_fail: "Could not copy. Please type NKP",
    e_req: "This field is required", e_mobile: "Enter a valid 10-digit mobile number",
    e_email: "Enter a valid email address", e_exam: "Choose at least one",
    e_consent: "Please tick to continue", e_code: "Please enter the code NKP",
    code_hint: "Code for Neikkarapatti (Palani) schools: NKP",
    code_ok: "Code NKP accepted. Complimentary membership for Grade 12 students of Neikkarapatti & Palani.",
    code_bad: "This code is not valid for this offer. Please enter NKP.",
    sending: "Submitting…",
    ok_t: "You're registered", ok_p: "Thank you, {name}. Our team will confirm your details and share your portal login on WhatsApp or email.",
    wa_t: "One last step", wa_p: "Your details are ready, {name}. Send them to us on WhatsApp so we can activate your complimentary access.",
    wa_fail: "We could not submit automatically. Please send your details on WhatsApp instead.",
    wa_btn: "Send on WhatsApp", copy_det: "Copy details", edit: "Edit details",
    share_msg: "Grade 12 students of Neikkarapatti, Palani schools (Class of 2027): EduAakashaa is offering a complimentary membership for NEET / JEE / TNEA guidance. Register with code NKP:"
  };

  var lang = "en";
  var lastResult = null;

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function msg(k) { return (lang === "ta" && TA[k]) ? TA[k] : EN[k]; }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }

  /* remember the English source text */
  $$("[data-t]").forEach(function (n) { n.setAttribute("data-en", n.innerHTML); });
  $$("[data-t-ph]").forEach(function (n) { n.setAttribute("data-en-ph", n.getAttribute("placeholder") || ""); });

  /* ---------- language ---------- */
  function setLang(l) {
    lang = l;
    document.documentElement.lang = l === "ta" ? "ta" : "en";
    $$("[data-t]").forEach(function (n) {
      var k = n.getAttribute("data-t");
      n.innerHTML = (l === "ta" && TA[k]) ? TA[k] : n.getAttribute("data-en");
    });
    $$("[data-t-ph]").forEach(function (n) {
      var k = n.getAttribute("data-t-ph");
      n.setAttribute("placeholder", (l === "ta" && TA[k]) ? TA[k] : n.getAttribute("data-en-ph"));
    });
    $$(".lang button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === l)); });
    $$(".err").forEach(function (e) { if (!e.hidden && e.getAttribute("data-k")) e.textContent = msg(e.getAttribute("data-k")); });
    updateCode(false);
    renderResult();
    updateShare();
    try { localStorage.setItem("ea_lang", l); } catch (e) {}
  }
  $$(".lang button").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
  });

  /* ---------- copy helpers ---------- */
  function copyText(text) {
    return new Promise(function (resolve, reject) {
      function legacy() {
        try {
          var ta = document.createElement("textarea");
          ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
          document.body.appendChild(ta); ta.select();
          var ok = document.execCommand("copy");
          document.body.removeChild(ta);
          ok ? resolve() : reject();
        } catch (e) { reject(e); }
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(resolve, legacy);
      } else { legacy(); }
    });
  }
  function flash(btnSpan, key) {
    var k = btnSpan.getAttribute("data-t");
    var orig = (lang === "ta" && TA[k]) ? TA[k] : btnSpan.getAttribute("data-en");
    btnSpan.textContent = msg(key);
    setTimeout(function () { btnSpan.innerHTML = (lang === "ta" && TA[k]) ? TA[k] : btnSpan.getAttribute("data-en"); }, 1800);
  }
  $$(".js-copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var s = $("span", b);
      copyText(CONFIG.code).then(function () { flash(s, "copied"); }, function () { flash(s, "copy_fail"); });
    });
  });

  /* ---------- share ---------- */
  function pageUrl() {
    try { if (/^https?:/.test(location.protocol)) return location.href.split("#")[0]; } catch (e) {}
    return CONFIG.siteUrl;
  }
  function shareText() { return msg("share_msg") + " " + pageUrl(); }
  function updateShare() { $("#shareWa").setAttribute("href", "https://wa.me/?text=" + encodeURIComponent(shareText())); }
  $("#shareCopy").addEventListener("click", function () {
    var s = $("span", this);
    copyText(shareText()).then(function () { flash(s, "copied"); }, function () { flash(s, "copy_fail"); });
  });

  /* ---------- form ---------- */
  var form = $("#regForm"), codeInp = $("#fCode"), codeSt = $("#codeStatus");
  function updateCode(blur) {
    var v = codeInp.value.trim().toUpperCase();
    codeSt.className = "code-status";
    if (v === CONFIG.code) { codeSt.classList.add("ok"); codeSt.textContent = msg("code_ok"); }
    else if (v && (blur || v.length >= 3)) { codeSt.classList.add("bad"); codeSt.textContent = msg("code_bad"); }
    else { codeSt.textContent = msg("code_hint"); }
  }
  codeInp.addEventListener("input", function () { clearErr("fCode"); updateCode(false); });
  codeInp.addEventListener("blur", function () { updateCode(true); });
  $("#useCode").addEventListener("click", function () { codeInp.value = CONFIG.code; clearErr("fCode"); updateCode(false); codeInp.focus(); });

  function setErr(id, key) {
    var e = $("#e-" + id); if (!e) return;
    e.hidden = false; e.setAttribute("data-k", key); e.textContent = msg(key);
    var f = document.getElementById(id);
    if (f && f.tagName !== "FIELDSET") f.setAttribute("aria-invalid", "true");
  }
  function clearErr(id) {
    var e = $("#e-" + id); if (e) { e.hidden = true; e.removeAttribute("data-k"); }
    var f = document.getElementById(id); if (f) f.removeAttribute("aria-invalid");
  }
  ["fName", "fSchool", "fStream", "fMobile", "fEmail", "fParent", "fPMobile", "fConsent"].forEach(function (id) {
    var f = document.getElementById(id);
    f.addEventListener("input", function () { clearErr(id); });
    f.addEventListener("change", function () { clearErr(id); });
  });
  $$("input[name=exams]").forEach(function (c) { c.addEventListener("change", function () { clearErr("fExams"); }); });

  function digits(v) {
    var d = String(v || "").replace(/\D/g, "");
    if (d.length === 12 && d.indexOf("91") === 0) d = d.slice(2);
    if (d.length === 11 && d.charAt(0) === "0") d = d.slice(1);
    return d;
  }
  function validate() {
    var bad = [];
    function need(id, key) { setErr(id, key); bad.push(id); }
    ["fExams"].concat(["fName", "fSchool", "fStream", "fMobile", "fEmail", "fParent", "fPMobile", "fCode", "fConsent"]).forEach(clearErr);

    if ($("#fName").value.trim().length < 2) need("fName", "e_req");
    if ($("#fSchool").value.trim().length < 3) need("fSchool", "e_req");
    if (!$("#fStream").value) need("fStream", "e_req");
    if (!/^[6-9]\d{9}$/.test(digits($("#fMobile").value))) need("fMobile", "e_mobile");
    if (!$$("input[name=exams]:checked").length) { setErr("fExams", "e_exam"); bad.push("fExams"); }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test($("#fEmail").value.trim())) need("fEmail", "e_email");
    if ($("#fParent").value.trim().length < 2) need("fParent", "e_req");
    var pm = $("#fPMobile").value.trim();
    if (pm && !/^[6-9]\d{9}$/.test(digits(pm))) need("fPMobile", "e_mobile");
    if (codeInp.value.trim().toUpperCase() !== CONFIG.code) { need("fCode", "e_code"); updateCode(true); }
    if (!$("#fConsent").checked) need("fConsent", "e_consent");
    return bad;
  }
  function collect() {
    var pm = digits($("#fPMobile").value);
    return {
      timestamp: new Date().toISOString(),
      campaign: CONFIG.campaign,
      code: CONFIG.code,
      studentName: $("#fName").value.trim(),
      school: $("#fSchool").value.trim(),
      stream: $("#fStream").value,
      admissions: $$("input[name=exams]:checked").map(function (c) { return c.value; }),
      mobile: "+91" + digits($("#fMobile").value),
      email: $("#fEmail").value.trim(),
      parentName: $("#fParent").value.trim(),
      parentMobile: pm ? "+91" + pm : "",
      guidanceLanguage: ($("input[name=glang]:checked") || {}).value || "Tamil",
      consent: true,
      pageLanguage: lang
    };
  }
  function detailsText(d) {
    return [
      "Hello EduAakashaa, I would like to claim the complimentary membership for Grade 12 students of Neikkarapatti & Palani (Class of 2027).",
      "Code: " + d.code,
      "Student: " + d.studentName,
      "School: " + d.school,
      "Stream: " + d.stream,
      "Admissions: " + d.admissions.join(", "),
      "Mobile: " + d.mobile,
      "Email: " + d.email,
      "Parent/guardian: " + d.parentName + (d.parentMobile ? " (" + d.parentMobile + ")" : ""),
      "Guidance language: " + d.guidanceLanguage
    ].join("\n");
  }

  var resBox = $("#result");
  function renderResult() {
    if (!lastResult) return;
    var r = lastResult, name = r.data.studentName.split(" ")[0];
    resBox.innerHTML = "";
    if (r.type === "ok") {
      var mark = el("div", "okmark"); mark.innerHTML = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
      resBox.appendChild(mark);
      resBox.appendChild(el("h3", "", msg("ok_t")));
      resBox.appendChild(el("p", "", msg("ok_p").replace("{name}", name)));
      if (r.data.reference) resBox.appendChild(el("p", "code-status ok", (lang === "ta" ? "குறிப்பு எண்: " : "Reference: ") + r.data.reference));
    } else {
      resBox.appendChild(el("h3", "", msg("wa_t")));
      resBox.appendChild(el("p", "", (r.failed ? msg("wa_fail") + " " : "") + msg("wa_p").replace("{name}", name)));
      var acts = el("div", "acts");
      var a = el("a", "btn-primary"); a.href = "https://wa.me/" + CONFIG.whatsapp + "?text=" + encodeURIComponent(r.text);
      a.target = "_blank"; a.rel = "noopener";
      a.appendChild(el("span", "", msg("wa_btn"))); var arr = el("span", "arr", "→"); arr.setAttribute("aria-hidden", "true"); a.appendChild(arr);
      acts.appendChild(a);
      var cp = el("button", "btn-ghost", msg("copy_det")); cp.type = "button";
      cp.addEventListener("click", function () {
        copyText(r.text).then(function () { cp.textContent = msg("copied"); }, function () { cp.textContent = msg("copy_fail"); });
        setTimeout(function () { cp.textContent = msg("copy_det"); }, 1800);
      });
      acts.appendChild(cp);
      resBox.appendChild(acts);
    }
    var edit = el("button", "link-btn", msg("edit")); edit.type = "button";
    edit.addEventListener("click", function () { lastResult = null; resBox.hidden = true; form.hidden = false; $("#fName").focus(); });
    resBox.appendChild(edit);
    form.hidden = true; resBox.hidden = false;
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if ($("input[name=website]").value) return; /* honeypot */
    var bad = validate();
    if (bad.length) {
      var first = bad[0], t = document.getElementById(first);
      if (first === "fExams") t = $("input[name=exams]");
      if (t) { t.focus(); try { t.scrollIntoView({ block: "center", behavior: "smooth" }); } catch (e) {} }
      return;
    }
    var data = collect(), text = detailsText(data), btn = $("#submitBtn"), lbl = $("span", btn);

    function done(ok, failed) {
      btn.disabled = false; lbl.innerHTML = (lang === "ta" && TA.f_submit) ? TA.f_submit : lbl.getAttribute("data-en");
      lastResult = { type: ok ? "ok" : "wa", data: data, text: text, failed: !!failed };
      renderResult();
      try { resBox.scrollIntoView({ block: "center", behavior: "smooth" }); } catch (e) {}
    }

    var fe = $("#formErr"); fe.hidden = true;
    btn.disabled = true; lbl.textContent = msg("sending");
    fetch(CONFIG.endpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (res) {
        if (res.body && res.body.ok) { lastResult = null; data.reference = res.body.reference; done(true, false); return; }
        btn.disabled = false; lbl.innerHTML = (lang === "ta" && TA.f_submit) ? TA.f_submit : lbl.getAttribute("data-en");
        if (res.status >= 400 && res.status < 500 && res.body && res.body.error) {
          fe.textContent = (lang === "ta" && res.body.error_ta) ? res.body.error_ta : res.body.error; fe.hidden = false;
          try { fe.scrollIntoView({ block: "center", behavior: "smooth" }); } catch (e) {}
          return;
        }
        done(false, true);
      })
      .catch(function () { done(false, true); });
  });

  /* ---------- FAQ ---------- */
  $$(".faq-q").forEach(function (q) {
    q.addEventListener("click", function () {
      var item = q.parentNode, open = !item.classList.contains("open");
      item.classList.toggle("open", open);
      q.setAttribute("aria-expanded", String(open));
    });
  });

  /* ---------- scroll reveal ---------- */
  var rv = $$(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); } });
    }, { threshold: .12, rootMargin: "0px 0px -40px 0px" });
    rv.forEach(function (n) { io.observe(n); });
  } else { rv.forEach(function (n) { n.classList.add("visible"); }); }

  /* ---------- init ---------- */
  var startLang = "en";
  try {
    var qs = new URLSearchParams(location.search);
    if (qs.get("lang") === "ta") startLang = "ta";
    else if (qs.get("lang") !== "en" && localStorage.getItem("ea_lang") === "ta") startLang = "ta";
    var pre = (qs.get("code") || "").trim().toUpperCase();
    if (pre === CONFIG.code) codeInp.value = pre;
  } catch (e) {}
  if (startLang === "ta") setLang("ta"); else { updateCode(false); updateShare(); }
})();

