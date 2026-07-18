/* Curs BernatLab — progrés, navegació, cerca i qüestionaris web. */
(function () {
    'use strict';

    const STORAGE_KEY = 'bernatlab_curs_progress_v2';
    const LEGACY_KEY = 'bernatlab_curs_progress';
    const onIndex = /\/curs\/?(?:index\.html)?$/.test(location.pathname);
    const base = onIndex ? './' : '../';

    function loadProgress() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || localStorage.getItem(LEGACY_KEY) || '{}');
        } catch (_) {
            return {};
        }
    }

    function saveProgress(data) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }

    function chapterKey() {
        const match = location.pathname.match(/\/curs\/(M\d+)\/([^/]+)\.html$/);
        return match ? match[1] + '/' + match[2] : null;
    }

    async function loadManifest() {
        const response = await fetch(base + 'course-manifest.json');
        if (!response.ok) throw new Error('No s’ha pogut carregar el manifest del curs.');
        return response.json();
    }

    function attemptsFor(entry) {
        return Array.isArray(entry && entry.attempts) ? entry.attempts : [];
    }

    function isComplete(entry) {
        return Boolean(entry && (entry.completed || attemptsFor(entry).length));
    }

    function updateStats(manifest) {
        const data = loadProgress();
        let attempts = 0;
        let correct = 0;
        let total = 0;
        const activeDays = new Set();

        Object.values(data).forEach(entry => {
            attemptsFor(entry).forEach(attempt => {
                attempts += 1;
                correct += attempt.correct || 0;
                total += attempt.total || 0;
                if (attempt.date) activeDays.add(attempt.date.slice(0, 10));
            });
        });

        const completed = manifest.chapters.filter(chapter => isComplete(data[chapter.key])).length;
        const set = (id, value) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value;
        };
        set('stat-attempts', attempts);
        set('stat-correct', correct);
        set('stat-percent', total ? Math.round(correct / total * 100) + '%' : '0%');
        set('stat-streak', calculateStreak(activeDays));
        set('stat-completed', completed + '/' + manifest.chapterCount);
        set('course-summary', `${manifest.moduleCount} mòduls · ${manifest.chapterCount} capítols · ${manifest.questionCount.toLocaleString('ca-ES')} preguntes`);
    }

    function calculateStreak(activeDays) {
        if (!activeDays.size) return 0;
        let cursor = new Date();
        cursor.setHours(0, 0, 0, 0);
        const today = cursor.toISOString().slice(0, 10);
        if (!activeDays.has(today)) {
            cursor.setDate(cursor.getDate() - 1);
            if (!activeDays.has(cursor.toISOString().slice(0, 10))) return 0;
        }
        let streak = 0;
        while (activeDays.has(cursor.toISOString().slice(0, 10))) {
            streak += 1;
            cursor.setDate(cursor.getDate() - 1);
        }
        return streak;
    }

    function updateChapterStatuses(manifest) {
        const data = loadProgress();
        manifest.chapters.forEach(chapter => {
            const element = document.querySelector(`[data-cap-key="${chapter.key}"]`);
            if (!element) return;
            const entry = data[chapter.key];
            const attempts = attemptsFor(entry);
            if (attempts.length) {
                const last = attempts[attempts.length - 1];
                const pct = last.total ? Math.round(last.correct / last.total * 100) : 0;
                element.className = 'capitol-status ' + (pct >= 70 ? 'fet' : 'errors');
                element.textContent = `✓ ${last.correct}/${last.total} (${pct}%)`;
            } else if (entry && entry.completed) {
                element.className = 'capitol-status fet';
                element.textContent = '✓ Completat';
            }
        });
        document.querySelectorAll('.modul[data-module]').forEach(module => {
            const chapters = manifest.chapters.filter(chapter => chapter.module === module.dataset.module);
            const completed = chapters.filter(chapter => isComplete(data[chapter.key])).length;
            const badge = module.querySelector('.badge-progress');
            if (badge) badge.textContent = `${completed}/${chapters.length} completats`;
        });
    }

    function setupIndex(manifest) {
        updateStats(manifest);
        updateChapterStatuses(manifest);

        const data = loadProgress();
        const continueBox = document.getElementById('continue-course');
        const lastKey = localStorage.getItem('bernatlab_last_chapter');
        const last = manifest.chapters.find(chapter => chapter.key === lastKey);
        if (continueBox && last) {
            continueBox.hidden = false;
            continueBox.querySelector('a').href = last.href;
            continueBox.querySelector('strong').textContent = last.module + ' · ' + last.title;
        }

        const search = document.getElementById('course-search');
        const filter = document.getElementById('course-filter');
        function applyFilters() {
            const query = (search ? search.value : '').trim().toLowerCase();
            const mode = filter ? filter.value : 'all';
            document.querySelectorAll('.capitol[data-key]').forEach(item => {
                const key = item.dataset.key;
                const text = item.textContent.toLowerCase();
                const complete = isComplete(data[key]);
                const modeMatch = mode === 'all' || (mode === 'complete' && complete) || (mode === 'pending' && !complete);
                item.hidden = !text.includes(query) || !modeMatch;
            });
            document.querySelectorAll('.modul[data-module]').forEach(module => {
                module.hidden = !module.querySelector('.capitol[data-key]:not([hidden])');
            });
        }
        if (search) search.addEventListener('input', applyFilters);
        if (filter) filter.addEventListener('change', applyFilters);
    }

    function parseQuiz(markdown) {
        return markdown.split(/\n(?=##\s+Pregunta\b)/i).filter(block => /^##\s+Pregunta\b/i.test(block.trim())).map(block => {
            const lines = block.trim().split('\n');
            const heading = lines.shift();
            const options = [];
            const text = [];
            lines.forEach(line => {
                const option = line.match(/^- \[([ xX])\]\s*(.+)$/);
                if (option) options.push({correct: option[1].toLowerCase() === 'x', text: option[2]});
                else if (line.trim() && !line.startsWith('**Pistes**')) text.push(line.trim());
            });
            return {open: /\(obert[au]\)/i.test(heading) || !options.length, text: text.join(' '), options};
        });
    }

    function escapeHtml(value) {
        const div = document.createElement('div');
        div.textContent = value;
        return div.innerHTML;
    }

    async function setupChapter(manifest) {
        const key = chapterKey();
        const index = manifest.chapters.findIndex(chapter => chapter.key === key);
        if (index < 0) return;
        const chapter = manifest.chapters[index];
        localStorage.setItem('bernatlab_last_chapter', key);

        const nav = document.createElement('nav');
        nav.className = 'course-pager';
        const previous = manifest.chapters[index - 1];
        const next = manifest.chapters[index + 1];
        nav.innerHTML = `${previous ? `<a href="../${previous.href}">← ${escapeHtml(previous.title)}</a>` : '<span></span>'}
            <button type="button" class="mark-complete">✓ Marcar completat</button>
            ${next ? `<a href="../${next.href}">${escapeHtml(next.title)} →</a>` : '<a href="../index.html">Índex del curs →</a>'}`;
        document.querySelector('main').prepend(nav);
        document.querySelector('main').append(nav.cloneNode(true));

        document.querySelectorAll('.mark-complete').forEach(button => {
            const progress = loadProgress();
            if (isComplete(progress[key])) button.textContent = '✓ Completat';
            button.addEventListener('click', () => {
                const current = loadProgress();
                current[key] = current[key] || {attempts: []};
                current[key].completed = !current[key].completed;
                current[key].completedAt = current[key].completed ? new Date().toISOString() : null;
                saveProgress(current);
                document.querySelectorAll('.mark-complete').forEach(other => {
                    other.textContent = current[key].completed ? '✓ Completat' : '✓ Marcar completat';
                });
            });
        });

        const quizSection = document.getElementById('quiz');
        if (!quizSection) return;
        const previewHeading = Array.from(quizSection.querySelectorAll('h3')).find(heading =>
            heading.textContent.toLowerCase().includes('vista prèvia')
        );
        if (previewHeading) {
            const previewList = previewHeading.nextElementSibling;
            if (previewList && previewList.matches('ol, ul')) previewList.remove();
            previewHeading.remove();
        }
        const response = await fetch('../' + chapter.quizUrl);
        if (!response.ok) return;
        const questions = parseQuiz(await response.text());
        const widget = document.createElement('div');
        widget.className = 'web-quiz';
        widget.innerHTML = `<h3>Fes el qüestionari aquí</h3><p>${questions.length} preguntes. Les obertes són d’autoreflexió i no puntuen automàticament.</p>
            <form>${questions.map((question, qIndex) => `<fieldset data-question="${qIndex}">
                <legend>${qIndex + 1}. ${escapeHtml(question.text)}</legend>
                ${question.open ? '<textarea rows="3" placeholder="Escriu la teva resposta..."></textarea>' : question.options.map((option, oIndex) => `<label><input type="radio" name="q${qIndex}" value="${oIndex}"> ${escapeHtml(option.text)}</label>`).join('')}
                <p class="quiz-feedback" aria-live="polite"></p>
            </fieldset>`).join('')}
            <button type="submit" class="quiz-submit">Corregir qüestionari</button><p class="quiz-result" aria-live="polite"></p></form>`;
        quizSection.prepend(widget);

        widget.querySelector('form').addEventListener('submit', event => {
            event.preventDefault();
            let correct = 0;
            let total = 0;
            questions.forEach((question, qIndex) => {
                if (question.open) return;
                total += 1;
                const selected = widget.querySelector(`input[name="q${qIndex}"]:checked`);
                const feedback = widget.querySelector(`[data-question="${qIndex}"] .quiz-feedback`);
                const selectedIndex = selected ? Number(selected.value) : -1;
                if (selectedIndex >= 0 && question.options[selectedIndex].correct) {
                    correct += 1;
                    feedback.textContent = '✓ Correcte';
                    feedback.className = 'quiz-feedback correct';
                } else {
                    const answer = question.options.find(option => option.correct);
                    feedback.textContent = 'Resposta correcta: ' + (answer ? answer.text : 'consulta les respostes');
                    feedback.className = 'quiz-feedback incorrect';
                }
            });
            const progress = loadProgress();
            progress[key] = progress[key] || {attempts: []};
            progress[key].attempts = progress[key].attempts || [];
            progress[key].attempts.push({date: new Date().toISOString(), correct, total});
            progress[key].completed = true;
            saveProgress(progress);
            widget.querySelector('.quiz-result').innerHTML = `<strong>Resultat: ${correct}/${total}</strong> (${total ? Math.round(correct / total * 100) : 0}%). <a href="../${chapter.answersUrl}">Consulta les respostes explicades</a>.`;
            document.querySelectorAll('.mark-complete').forEach(button => button.textContent = '✓ Completat');
        });
    }

    loadManifest().then(manifest => {
        if (onIndex) setupIndex(manifest);
        else setupChapter(manifest);
    }).catch(error => console.warn(error.message));
})();
