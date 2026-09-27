function formatDate(iso) {
    if (!iso) return 'unknown date';
    const d = new Date(iso);
    return isNaN(d) ? iso : d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

const BUCKET_LABELS = {
    overdue: 'Overdue',
    thisWeek: 'This Week',
    nextWeek: 'Next Week',
    later: 'Later',
    noDate: 'No Date Set',
};
const BUCKET_ORDER = ['overdue', 'thisWeek', 'nextWeek', 'later', 'noDate'];

function startOfWeek(date) {
    const d = new Date(date);
    const day = d.getDay(); // 0 (Sun) - 6 (Sat)
    const diffToMonday = day === 0 ? -6 : 1 - day;
    d.setDate(d.getDate() + diffToMonday);
    d.setHours(0, 0, 0, 0);
    return d;
}

function getDateBucket(dateStr) {
    if (!dateStr || dateStr === 'TBD') return 'noDate';
    const date = new Date(dateStr + 'T00:00:00');
    if (isNaN(date)) return 'noDate';

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const thisMonday = startOfWeek(today);
    const thisSunday = new Date(thisMonday); thisSunday.setDate(thisMonday.getDate() + 6);
    const nextSunday = new Date(thisMonday); nextSunday.setDate(thisMonday.getDate() + 13);

    if (date < thisMonday) return 'overdue';
    if (date <= thisSunday) return 'thisWeek';
    if (date <= nextSunday) return 'nextWeek';
    return 'later';
}

function historyHtmlFor(priorHistory) {
    if (priorHistory.length === 0) return '';
    return `<div class="history">${priorHistory.slice().reverse().map(t => `
        <div class="history-item">
            ${escapeHtml(t.note !== undefined ? t.note : (t.action || 'follow up'))}${t.date ? ' &middot; ' + escapeHtml(t.date) : ''}
            <span class="from-note">(from note on ${formatDate(t.noted_at)})</span>
        </div>
    `).join('')}</div>`;
}

function renderItemLi(item, latest, priorHistory, currentLabel) {
    const li = document.createElement('li');
    li.className = 'contact-item';
    li.innerHTML = `
        <details>
            <summary>
                <span><span class="contact-name">${escapeHtml(item.name)}</span>${priorHistory.length ? `<span class="history-count">${priorHistory.length} earlier touchpoint(s)</span>` : ''}</span>
                <span class="contact-current">${currentLabel}<br><span class="from-note">from note on ${formatDate(latest.noted_at)}</span></span>
            </summary>
            ${historyHtmlFor(priorHistory)}
        </details>
    `;
    return li;
}

/** Render items grouped into This Week / Next Week / Later / No Date sections, based on each item's latest touchpoint date. */
function renderGroupedByDate(listEl, items, emptyMessage) {
    listEl.innerHTML = '';

    if (!items || items.length === 0) {
        listEl.innerHTML = `<div class="empty">${emptyMessage}</div>`;
        return;
    }

    const grouped = {};
    BUCKET_ORDER.forEach(b => grouped[b] = []);

    items.forEach(item => {
        const touchpoints = item.touchpoints || [];
        const latest = touchpoints[touchpoints.length - 1] || {};
        grouped[getDateBucket(latest.date)].push(item);
    });

    BUCKET_ORDER.forEach(bucket => {
        const bucketItems = grouped[bucket];
        if (bucketItems.length === 0) return;

        const header = document.createElement('li');
        header.className = 'section-header' + (bucket === 'overdue' ? ' overdue' : '');
        header.textContent = `${BUCKET_LABELS[bucket]} (${bucketItems.length})`;
        listEl.appendChild(header);

        bucketItems.forEach(item => {
            const touchpoints = item.touchpoints || [];
            const latest = touchpoints[touchpoints.length - 1] || {};
            const priorHistory = touchpoints.slice(0, -1);
            const currentLabel = `${escapeHtml(latest.action || 'follow up')} &middot; ${escapeHtml(latest.date || 'TBD')}`;
            listEl.appendChild(renderItemLi(item, latest, priorHistory, currentLabel));
        });
    });
}

/** Render items as a plain alphabetical list with no date grouping (e.g. companies). */
function renderFlatList(listEl, items, emptyMessage) {
    listEl.innerHTML = '';

    if (!items || items.length === 0) {
        listEl.innerHTML = `<div class="empty">${emptyMessage}</div>`;
        return;
    }

    items.forEach(item => {
        const touchpoints = item.touchpoints || [];
        const latest = touchpoints[touchpoints.length - 1] || {};
        const priorHistory = touchpoints.slice(0, -1);
        const currentLabel = escapeHtml(latest.note || '');
        listEl.appendChild(renderItemLi(item, latest, priorHistory, currentLabel));
    });
}

async function loadContacts() {
    try {
        const res = await fetch('/api/contacts');
        const data = await res.json();
        renderGroupedByDate(document.getElementById('contacts'), data.contacts, 'No contacts yet. Run to fetch diary notes.');
    } catch (e) {
        console.error(e);
    }
}

async function loadInterests() {
    try {
        const res = await fetch('/api/interests');
        const data = await res.json();
        renderFlatList(document.getElementById('companies'), data.companies, 'No companies of interest yet.');
        renderGroupedByDate(document.getElementById('events'), data.events, 'No events of interest yet.');
    } catch (e) {
        console.error(e);
    }
}

function showTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tab));
    document.getElementById('contacts').style.display = tab === 'contacts' ? '' : 'none';
    document.getElementById('interests').style.display = tab === 'interests' ? '' : 'none';
}

async function runAction(url, btn, describeResult) {
    const status = document.getElementById('status');
    btn.disabled = true;
    status.style.display = 'block';
    status.className = 'status running';
    status.textContent = 'Running...';

    try {
        const res = await fetch(url, { method: 'POST' });
        const data = await res.json();

        if (data.error) {
            status.className = 'status error';
            status.textContent = 'Error: ' + data.error;
        } else {
            status.className = 'status success';
            status.textContent = describeResult(data);
            loadContacts();
            loadInterests();
        }
    } catch (e) {
        status.className = 'status error';
        status.textContent = 'Error: ' + e.message;
    }

    btn.disabled = false;
    setTimeout(() => { status.style.display = 'none'; }, 5000);
}

function fetchMail() {
    runAction('/api/fetch-mail', document.getElementById('fetchBtn'),
        data => `Fetched ${data.emails_fetched || 0} new email(s) - ${data.total_contacts || 0} contact(s), ${data.total_companies || 0} companie(s), ${data.total_events || 0} event(s)`);
}

function processLocal() {
    runAction('/api/process', document.getElementById('processBtn'),
        data => `Processed diary notes - ${data.total_contacts || 0} contact(s), ${data.total_companies || 0} companie(s), ${data.total_events || 0} event(s)`);
}

loadContacts();
loadInterests();
