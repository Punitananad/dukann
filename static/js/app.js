/**
 * RackFinder — Shop Locator JS
 * Live search, AJAX suggestions, shelf loading
 */

/**
 * Initialize live search suggestions for a given input field.
 * @param {string} inputId   - id of the search <input>
 * @param {string} dropdownId - id of the suggestions container
 */
function initLiveSearch(inputId, dropdownId) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);
    if (!input || !dropdown) return;

    let debounceTimer = null;

    // Position the dropdown correctly
    function positionDropdown() {
        const rect = input.getBoundingClientRect();
        const parentRect = input.offsetParent.getBoundingClientRect();
        dropdown.style.width = input.offsetWidth + 'px';
        dropdown.style.left = (input.offsetLeft) + 'px';
        dropdown.style.top = (input.offsetTop + input.offsetHeight) + 'px';
    }

    input.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const q = this.value.trim();

        if (q.length < 2) {
            dropdown.style.display = 'none';
            dropdown.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/api/search/?q=${encodeURIComponent(q)}`)
                .then(r => r.json())
                .then(data => {
                    dropdown.innerHTML = '';
                    if (data.results.length === 0) {
                        dropdown.style.display = 'none';
                        return;
                    }

                    data.results.forEach(p => {
                        const item = document.createElement('a');
                        item.href = p.url;
                        item.className = 'suggestion-item';

                        let stockBadge = '';
                        if (p.stock_status === 'out') {
                            stockBadge = '<span class="badge bg-danger ms-1" style="font-size:0.65rem;">Out</span>';
                        } else if (p.stock_status === 'low') {
                            stockBadge = `<span class="badge bg-warning text-dark ms-1" style="font-size:0.65rem;">Low: ${p.quantity}</span>`;
                        } else {
                            stockBadge = `<span class="badge bg-success ms-1" style="font-size:0.65rem;">${p.quantity}</span>`;
                        }

                        let locationHtml = '';
                        if (p.rack) {
                            locationHtml = `<span class="suggestion-rack">Rack ${p.rack}</span>`;
                            if (p.shelf) {
                                locationHtml += `<span class="suggestion-shelf">${p.shelf}</span>`;
                            }
                        } else {
                            locationHtml = '<span class="text-muted small">No location</span>';
                        }

                        item.innerHTML = `
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <span class="fw-semibold">${p.brand} ${p.name}</span>
                                    <small class="text-muted ms-1">${p.category}</small>
                                </div>
                                <div class="d-flex align-items-center gap-1">
                                    ${locationHtml}
                                    ${stockBadge}
                                </div>
                            </div>`;

                        dropdown.appendChild(item);
                    });

                    positionDropdown();
                    dropdown.style.display = 'block';
                })
                .catch(() => {
                    dropdown.style.display = 'none';
                });
        }, 200);
    });

    // Hide on outside click
    document.addEventListener('click', function (e) {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });

    // Keyboard navigation
    input.addEventListener('keydown', function (e) {
        const items = dropdown.querySelectorAll('.suggestion-item');
        const current = dropdown.querySelector('.suggestion-item.active');
        let idx = Array.from(items).indexOf(current);

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            idx = Math.min(idx + 1, items.length - 1);
            items.forEach(i => i.classList.remove('active'));
            if (items[idx]) items[idx].classList.add('active');
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            idx = Math.max(idx - 1, 0);
            items.forEach(i => i.classList.remove('active'));
            if (items[idx]) items[idx].classList.add('active');
        } else if (e.key === 'Enter') {
            if (current) {
                e.preventDefault();
                window.location.href = current.href;
            }
        } else if (e.key === 'Escape') {
            dropdown.style.display = 'none';
        }
    });

    // Re-show if input has value and user re-focuses
    input.addEventListener('focus', function () {
        if (this.value.trim().length >= 2 && dropdown.innerHTML) {
            dropdown.style.display = 'block';
        }
    });
}

// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(el => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
            bsAlert.close();
        });
    }, 4000);
});
