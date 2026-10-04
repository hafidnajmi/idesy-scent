// Umami analytics loader — indoeasyscent.com
//
// Dipisah dari cart.js dengan sengaja: cart.js adalah logika keranjang
// inquiry, analytics adalah telemetri. Mencampur keduanya berarti satu error
//yntax di analytics mematikan keranjang.
//
// Tracker diambil dari subdomain analytics, bukan host situs, supaya CSP
// script-src bisa mengizinkan domain itu secara eksplisit dan skrip tetap
// ter-cache lintas halaman.
//
// data-domains sengaja TIDAK diisi: panel dan situs di subdomain berbeda, jadi
// tidak ada kebutuhan membatasi host. Kalau nanti ada staging, tambahkan
// "indoeasyscent.com,www.indoeasyscent.com" di sini.
(function () {
  'use strict';

  var WEBSITE_ID = '9b92af51-a8cc-4813-836e-198cf7c8715c';
  var HOST_URL = 'https://analytics.indoeasyscent.com';

  // Jangan hitung bot/crawler — mereka tidak diwakili dalam analytics mana pun
  // dan hanya mengotori grafik.
  if (navigator.doNotTrack === '1') return;

  var s = document.createElement('script');
  s.defer = true;
  // v3 menyajikan tracker di /script.js. /umami.js membalas 404.
  s.src = HOST_URL + '/script.js';
  s.setAttribute('data-website-id', WEBSITE_ID);
  // Kirim ke host yang sama dengan tempat skrip berada (default), tapi disebut
  // eksplisit supaya maksudnya jelas kalau subdomain-nya nanti berubah.
  s.setAttribute('data-host-url', HOST_URL);
  document.head.appendChild(s);
})();