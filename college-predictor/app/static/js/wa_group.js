/* "Send to WhatsApp group": WhatsApp has no way to pre-fill a group message from a website, so copy the text, then open the group. */
(function () {
  function toast(msg) {
    var t = document.createElement('div');
    t.textContent = msg; t.setAttribute('role', 'status');
    t.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#0A2560;color:#fff;padding:10px 16px;border-radius:10px;z-index:9999;font:600 14px system-ui;max-width:90vw;box-shadow:0 6px 20px rgba(0,0,0,.25)';
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, 4500);
  }
  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (ok, no) {
      var a = document.createElement('textarea'); a.value = text; a.style.position = 'fixed'; a.style.opacity = '0';
      document.body.appendChild(a); a.select();
      try { document.execCommand('copy') ? ok() : no(); } catch (e) { no(e); }
      a.remove();
    });
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('.wag-send'); if (!b) return;
    ev.preventDefault();
    var src = b.getAttribute('data-wag-source'), el = src ? document.querySelector(src) : null;
    var text = (el ? el.value : b.getAttribute('data-wag-text')) || '';
    var link = b.getAttribute('data-wag-link'), name = b.getAttribute('data-wag-name') || 'the WhatsApp group';
    if (!text.trim()) { toast('Write a message first.'); return; }
    if (!link) { toast('No WhatsApp group is saved for this member yet. Add the group invite link first.'); return; }
    var w = window.open('', '_blank');           // open synchronously so the pop-up is allowed
    copy(text).then(function () { toast('Message copied. Paste it into ' + name + ' and press send.'); },
                    function () { toast('Could not copy automatically. Select the message, copy it, then paste it in the group.'); })
      .then(function () { if (w) { w.opener = null; w.location = link; } else { window.location = link; } });
  });
})();
