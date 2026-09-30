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

function escapeAttr(text) {
    return String(text).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
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

/** All touchpoints as a compact, always-visible timeline - oldest to newest, current one bolded. */
function buildTimelineHtml(touchpoints) {
    if (touchpoints.length === 0) return '';
    return touchpoints.map((t, i) => {
        const isLatest = i === touchpoints.length - 1;
        const label = t.note !== undefined
            ? (t.note || '(no note)')
            : `${t.action || 'follow up'} · ${t.date || 'TBD'}`;
        const title = `from note on ${formatDate(t.noted_at)}`;
        const cls = isLatest ? 'tl-current' : 'tl-past';
        return `<span class="${cls}" title="${escapeAttr(title)}">${escapeHtml(label)}</span>`;
    }).join('<span class="tl-arrow">→</span>');
}

async function editName(type, currentName) {
    const corrected = prompt('Fix this name:', currentName);
    if (!corrected || corrected.trim() === '' || corrected.trim() === currentName) return;

    try {
        const res = await fetch('/api/corrections', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type, wrong_name: currentName, correct_name: corrected.trim() }),
        });
        const data = await res.json();
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        loadContacts();
        loadInterests();
    } catch (e) {
        alert('Error: ' + e.message);
    }
}

function renderItemRow(type, item) {
    const touchpoints = item.touchpoints || [];
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td class="name-cell">
            <span>${escapeHtml(item.name)}</span>
            <button class="edit-btn" title="Fix this name">&#9998;</button>
        </td>
        <td class="timeline-cell">${buildTimelineHtml(touchpoints)}</td>
    `;
    tr.querySelector('.edit-btn').addEventListener('click', () => editName(type, item.name));
    return tr;
}

/** Render items grouped into This Week / Next Week / Later / No Date sections, based on each item's latest touchpoint date. */
function renderGroupedByDate(tableEl, items, emptyMessage, type) {
    tableEl.innerHTML = '';

    if (!items || items.length === 0) {
        tableEl.innerHTML = `<tr><td class="empty" colspan="2">${emptyMessage}</td></tr>`;
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

        const headerRow = document.createElement('tr');
        headerRow.className = 'section-header-row' + (bucket === 'overdue' ? ' overdue' : '');
        headerRow.innerHTML = `<td colspan="2">${BUCKET_LABELS[bucket]} (${bucketItems.length})</td>`;
        tableEl.appendChild(headerRow);

        bucketItems.forEach(item => tableEl.appendChild(renderItemRow(type, item)));
    });
}

/** Render items as a plain alphabetical list with no date grouping (e.g. companies). */
function renderFlatList(tableEl, items, emptyMessage, type) {
    tableEl.innerHTML = '';

    if (!items || items.length === 0) {
        tableEl.innerHTML = `<tr><td class="empty" colspan="2">${emptyMessage}</td></tr>`;
        return;
    }

    items.forEach(item => tableEl.appendChild(renderItemRow(type, item)));
}

async function loadContacts() {
    try {
        const res = await fetch('/api/contacts');
        const data = await res.json();
        renderGroupedByDate(document.getElementById('contacts'), data.contacts, 'No contacts yet. Run to fetch diary notes.', 'contacts');
    } catch (e) {
        console.error(e);
    }
}

async function loadInterests() {
    try {
        const res = await fetch('/api/interests');
        const data = await res.json();
        renderFlatList(document.getElementById('companies'), data.companies, 'No companies of interest yet.', 'companies');
        renderGroupedByDate(document.getElementById('events'), data.events, 'No events of interest yet.', 'events');
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
    setTimeout(() => { status.className = 'status'; }, 5000);
}

function fetchMail() {
    runAction('/api/fetch-mail', document.getElementById('fetchBtn'),
        data => `Fetched ${data.emails_fetched || 0} new email(s), extracted ${data.new_extractions || 0} via Claude - ${data.total_contacts || 0} contact(s), ${data.total_companies || 0} companie(s), ${data.total_events || 0} event(s)`);
}

function processLocal() {
    runAction('/api/process', document.getElementById('processBtn'),
        data => `Extracted ${data.new_extractions || 0} new note(s) via Claude - ${data.total_contacts || 0} contact(s), ${data.total_companies || 0} companie(s), ${data.total_events || 0} event(s)`);
}

function syncObsidian() {
    runAction('/api/sync-obsidian', document.getElementById('syncBtn'),
        data => `Created ${(data.contacts_created || []).length} contact note(s), ${(data.companies_created || []).length} company note(s) in Obsidian`);
}

loadContacts();
loadInterests();
