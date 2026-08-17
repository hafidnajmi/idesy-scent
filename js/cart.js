// Sistem Keranjang Belanja & Inquiry untuk Indoeasy Scent
// Menyimpan data di LocalStorage dan merender panel inquiry secara dinamis & aman (XSS-safe)

let cart = JSON.parse(localStorage.getItem('indoeasy_cart')) || [];

// Helper untuk sanitasi HTML (mencegah XSS)
function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function saveCart() {
    localStorage.setItem('indoeasy_cart', JSON.stringify(cart));
    updateCartUI();
}

function addToCart(item) {
    // item: { id, title, price, image, category }
    if (!item || !item.id) return;
    const existing = cart.find(i => i.id === item.id);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({
            id: String(item.id),
            title: String(item.title || 'Produk Scent'),
            price: Number(item.price) || 0,
            image: String(item.image || 'img/LOGO IDESY SCENT.png'),
            category: String(item.category || 'Diffuser'),
            quantity: 1
        });
    }
    saveCart();
    showToast(`Berhasil menambahkan "${escapeHtml(item.title)}" ke daftar inquiry`);
    openCartDrawer();
}

function removeFromCart(id) {
    cart = cart.filter(i => i.id !== id);
    saveCart();
}

function updateQuantity(id, delta) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.quantity += delta;
        if (item.quantity <= 0) {
            removeFromCart(id);
        } else {
            saveCart();
        }
    }
}

function clearCart() {
    cart = [];
    saveCart();
}

function getCartCount() {
    return cart.reduce((sum, item) => sum + (Number(item.quantity) || 0), 0);
}

// Format harga IDR
function formatPrice(val) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        maximumFractionDigits: 0
    }).format(Number(val) || 0);
}

function getCartTotal() {
    return cart.reduce((sum, item) => sum + ((Number(item.price) || 0) * (Number(item.quantity) || 0)), 0);
}

// Sistem notifikasi toast
function showToast(message) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'fixed bottom-8 right-8 z-[100] flex flex-col gap-3 pointer-events-none';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'bg-[#0D2A1D] text-white border-l-4 border-[#C9A24B] px-6 py-4 shadow-xl translate-y-10 opacity-0 transition-all duration-500 pointer-events-auto flex items-center gap-3 font-sans text-sm rounded-r-lg';
    toast.innerHTML = `
        <span class="material-symbols-outlined text-[#C9A24B]">check_circle</span>
        <span>${escapeHtml(message)}</span>
    `;
    container.appendChild(toast);

    // Animasi masuk
    setTimeout(() => {
        toast.classList.remove('translate-y-10', 'opacity-0');
    }, 10);

    // Hapus otomatis
    setTimeout(() => {
        toast.classList.add('opacity-0', 'translate-y-[-10px]');
        setTimeout(() => toast.remove(), 500);
    }, 3200);
}

// Menyisipkan HTML Keranjang Belanja
function injectCartDrawer() {
    if (document.getElementById('cart-drawer')) return;

    const drawer = document.createElement('div');
    drawer.id = 'cart-drawer';
    drawer.className = 'fixed inset-0 z-[60] overflow-hidden pointer-events-none transition-all duration-500';
    drawer.innerHTML = `
        <!-- Overlay -->
        <div id="cart-overlay" class="absolute inset-0 bg-black/50 opacity-0 transition-opacity duration-500 pointer-events-none backdrop-blur-xs"></div>
        
        <!-- Panel Keranjang -->
        <div id="cart-panel" class="absolute right-0 top-0 bottom-0 w-full max-w-md bg-[#F7F3EC] text-[#1F1F1D] flex flex-col translate-x-full transition-transform duration-500 ease-out shadow-2xl pointer-events-auto border-l border-[#0D2A1D]/10 font-sans">
            <!-- Header -->
            <div class="px-6 py-6 border-b border-[#0D2A1D]/10 flex justify-between items-center bg-[#F7F3EC]">
                <h3 class="font-serif text-2xl uppercase tracking-widest text-[#0D2A1D] flex items-center gap-2">
                    <span class="material-symbols-outlined !text-2xl text-[#C9A24B]">shopping_bag</span> Permintaan Scent
                </h3>
                <button id="close-cart-btn" class="p-2 text-[#1F1F1D]/60 hover:text-[#C9A24B] transition-colors focus:outline-none" aria-label="Tutup Keranjang">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            
            <!-- Daftar Item -->
            <div id="cart-items" class="flex-1 overflow-y-auto px-6 py-4 space-y-6">
                <!-- Item ditambahkan di sini secara dinamis -->
            </div>
            
            <!-- Ringkasan Footer -->
            <div class="border-t border-[#0D2A1D]/10 p-6 bg-[#F7F3EC] space-y-4">
                <div class="flex justify-between items-center text-sm font-label-caps text-[#1F1F1D]/60 tracking-wider">
                    <span>Estimasi Subtotal</span>
                    <span id="cart-subtotal" class="text-lg font-bold text-[#0D2A1D]">Rp 0</span>
                </div>
                <p class="text-xs text-[#1F1F1D]/50 italic">Diskon kuantitas besar &amp; penawaran komersial kustom akan dihitung secara presisi.</p>
                <div class="pt-2 flex flex-col gap-3">
                    <a href="checkout.html" class="w-full bg-[#0D2A1D] text-white hover:bg-[#C9A24B] hover:text-[#0D2A1D] transition-all duration-300 py-4 text-center font-label-caps tracking-widest font-bold block text-sm active:scale-[0.98] rounded-xl shadow-lg">
                        KIRIM INQUIRY WA
                    </a>
                    <button id="clear-cart-btn" class="w-full bg-transparent border border-[#0D2A1D]/20 text-[#1F1F1D]/60 hover:border-[#0D2A1D] hover:text-[#1F1F1D] transition-all duration-300 py-3 font-label-caps tracking-widest text-xs active:scale-[0.98] rounded-xl">
                        BERSIHKAN DAFTAR
                    </button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(drawer);

    // Event Listener untuk menutup keranjang
    const closeBtn = document.getElementById('close-cart-btn');
    const overlay = document.getElementById('cart-overlay');
    const clearBtn = document.getElementById('clear-cart-btn');

    if (closeBtn) closeBtn.addEventListener('click', closeCartDrawer);
    if (overlay) overlay.addEventListener('click', closeCartDrawer);
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            clearCart();
            showToast('Daftar inquiry dibersihkan');
        });
    }
}

function openCartDrawer() {
    injectCartDrawer();
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.getElementById('cart-overlay');
    const panel = document.getElementById('cart-panel');

    if (!drawer || !overlay || !panel) return;

    drawer.classList.remove('pointer-events-none');
    overlay.classList.add('opacity-100');
    overlay.classList.remove('pointer-events-none');
    panel.classList.remove('translate-x-full');
    
    updateCartUI();
}

function closeCartDrawer() {
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.getElementById('cart-overlay');
    const panel = document.getElementById('cart-panel');

    if (!drawer || !overlay || !panel) return;

    overlay.classList.remove('opacity-100');
    overlay.classList.add('pointer-events-none');
    panel.classList.add('translate-x-full');
    
    setTimeout(() => {
        drawer.classList.add('pointer-events-none');
    }, 500);
}

function updateCartUI() {
    const badges = document.querySelectorAll('.cart-badge');
    const count = getCartCount();

    badges.forEach(badge => {
        badge.textContent = count;
        if (count > 0) {
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    });

    const cartIcons = document.querySelectorAll('span.material-symbols-outlined');
    cartIcons.forEach(icon => {
        if (icon.textContent.trim() === 'shopping_bag' && !icon.classList.contains('cart-icon-bound')) {
            icon.classList.add('cart-icon-bound', 'cursor-pointer');
            const parent = icon.parentElement;
            if (parent && !parent.querySelector('.cart-badge')) {
                parent.classList.add('relative', 'inline-block');
                const badge = document.createElement('span');
                badge.className = 'cart-badge absolute -top-1.5 -right-1.5 bg-[#C9A24B] text-[#0D2A1D] text-[9px] font-bold rounded-full w-4 h-4 flex items-center justify-center border border-[#F7F3EC]';
                if (count > 0) {
                    badge.textContent = count;
                } else {
                    badge.classList.add('hidden');
                }
                parent.appendChild(badge);
            }
            icon.addEventListener('click', (e) => {
                e.preventDefault();
                openCartDrawer();
            });
        }
    });

    const cartItemsContainer = document.getElementById('cart-items');
    const subtotalContainer = document.getElementById('cart-subtotal');

    if (!cartItemsContainer || !subtotalContainer) return;

    subtotalContainer.textContent = formatPrice(getCartTotal());

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="h-64 flex flex-col items-center justify-center text-center opacity-40">
                <span class="material-symbols-outlined !text-5xl mb-4">shopping_bag</span>
                <p class="font-sans text-sm font-light">Daftar permintaan Anda kosong.</p>
            </div>
        `;
        return;
    }

    cartItemsContainer.innerHTML = '';
    cart.forEach(item => {
        const itemEl = document.createElement('div');
        itemEl.className = 'flex items-center gap-4 py-4 border-b border-[#0D2A1D]/10 group';
        
        const safeTitle = escapeHtml(item.title);
        const safeCat = escapeHtml(item.category);
        const safeImg = escapeHtml(item.image);
        
        let imgHtml = '';
        if (safeImg && (safeImg.startsWith('http') || safeImg.startsWith('img/') || safeImg.endsWith('.png') || safeImg.endsWith('.jpg') || safeImg.endsWith('.jpeg'))) {
            imgHtml = `<img class="w-16 h-16 object-cover bg-white rounded-lg shadow-xs" src="${safeImg}" alt="${safeTitle}">`;
        } else {
            imgHtml = `
                <div class="w-16 h-16 bg-[#EDE6D8] rounded-lg flex items-center justify-center text-[#0D2A1D]/40">
                    <span class="material-symbols-outlined !text-3xl">spa</span>
                </div>
            `;
        }

        itemEl.innerHTML = `
            <div class="flex-shrink-0">
                ${imgHtml}
            </div>
            <div class="flex-1 min-w-0 font-sans">
                <h4 class="text-sm font-bold text-[#0D2A1D] truncate">${safeTitle}</h4>
                <p class="text-xs text-[#1F1F1D]/60 uppercase tracking-widest mt-0.5">${safeCat}</p>
                <div class="flex items-center justify-between mt-3 font-sans">
                    <span class="text-sm text-[#C9A24B] font-semibold">${formatPrice(item.price)}</span>
                    
                    <div class="flex items-center border border-[#0D2A1D]/15 bg-white rounded-md overflow-hidden">
                        <button class="px-2 py-0.5 text-xs text-[#1F1F1D]/60 hover:text-[#0D2A1D] qty-minus-btn" data-id="${escapeHtml(item.id)}">-</button>
                        <span class="px-3 py-0.5 text-xs font-bold text-[#0D2A1D]">${Number(item.quantity)}</span>
                        <button class="px-2 py-0.5 text-xs text-[#1F1F1D]/60 hover:text-[#0D2A1D] qty-plus-btn" data-id="${escapeHtml(item.id)}">+</button>
                    </div>
                </div>
            </div>
            <button class="text-[#1F1F1D]/40 hover:text-red-600 transition-colors remove-item-btn p-1" data-id="${escapeHtml(item.id)}" aria-label="Hapus Item">
                <span class="material-symbols-outlined !text-lg">delete</span>
            </button>
        `;

        cartItemsContainer.appendChild(itemEl);
    });

    document.querySelectorAll('.qty-minus-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            updateQuantity(btn.dataset.id, -1);
        });
    });

    document.querySelectorAll('.qty-plus-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            updateQuantity(btn.dataset.id, 1);
        });
    });

    document.querySelectorAll('.remove-item-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            removeFromCart(btn.dataset.id);
            showToast('Item dihapus dari daftar');
        });
    });
}

// Inisialisasi menu mobile (Disabled: Diatur secara terpusat oleh initMobileDrawer di transitions.js)
function setupMobileMenu() {
    return;
}

// Jalankan ketika halaman dimuat
document.addEventListener('DOMContentLoaded', () => {
    injectCartDrawer();
    updateCartUI();
    // setupMobileMenu(); // Handled by transitions.js
});


