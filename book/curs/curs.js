/* Curs del BernatLab — JavaScript
 *
 * Mostra estadistiques basades en localStorage. Si vols un registre
 * persistent al terminal, usa python book/curs/quiz.py --stats.
 */

(function() {
    'use strict';

    const STORAGE_KEY = 'bernatlab_curs_progress';

    function loadProgress() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        } catch (e) {
            return {};
        }
    }

    function saveProgress(data) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch (e) {
            console.warn('No sha pogut guardar el progres:', e);
        }
    }

    function updateStats() {
        const data = loadProgress();
        let totalAttempts = 0;
        let totalCorrect = 0;
        let totalQ = 0;
        let lastDate = null;
        let streak = 0;

        for (const key in data) {
            const attempts = data[key].attempts || [];
            totalAttempts += attempts.length;
            for (const a of attempts) {
                totalCorrect += a.correct || 0;
                totalQ += a.total || 0;
                if (a.date) {
                    const d = new Date(a.date);
                    if (!lastDate || d > lastDate) lastDate = d;
                }
            }
        }

        // Calcular ratxa de dies
        if (lastDate) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const last = new Date(lastDate);
            last.setHours(0, 0, 0, 0);
            const diffDays = Math.floor((today - last) / (1000 * 60 * 60 * 24));
            streak = diffDays === 0 ? 1 : (diffDays === 1 ? 2 : 0);
        }

        document.getElementById('stat-attempts').textContent = totalAttempts;
        document.getElementById('stat-correct').textContent = totalCorrect;
        const pct = totalQ > 0 ? Math.round((totalCorrect / totalQ) * 100) : 0;
        document.getElementById('stat-percent').textContent = pct + '%';
        document.getElementById('stat-streak').textContent = streak;
    }

    function updateCapitolStatus() {
        const data = loadProgress();
        const statusEls = document.querySelectorAll('.capitol-status[data-cap-key]');
        statusEls.forEach(el => {
            const key = el.getAttribute('data-cap-key');
            if (data[key] && data[key].attempts && data[key].attempts.length > 0) {
                const last = data[key].attempts[data[key].attempts.length - 1];
                const total = last.total || 0;
                const correct = last.correct || 0;
                const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
                if (pct === 100) {
                    el.className = 'capitol-status fet';
                    el.textContent = '✓ ' + correct + '/' + total;
                } else if (pct >= 70) {
                    el.className = 'capitol-status encerts';
                    el.textContent = correct + '/' + total + ' (' + pct + '%)';
                } else {
                    el.className = 'capitol-status errors';
                    el.textContent = correct + '/' + total + ' (' + pct + '%)';
                }
            }
        });
    }

    // Exposar funcions per al Python
    window.bernatlabCurs = {
        update: function() {
            updateStats();
            updateCapitolStatus();
        },
        getData: loadProgress,
        saveData: saveProgress,
    };

    // Inicialitzar al carregar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            updateStats();
            updateCapitolStatus();
        });
    } else {
        updateStats();
        updateCapitolStatus();
    }
})();
