const InputBox = document.querySelector(".InputBox");
const SendButton = document.querySelector(".SendButton");
const Input = document.getElementById("Input");

// This variable will be 'true' initially and we'll set it to 'false' after the first message.
let isFirstMessage = true;

// Keep last scraped context so the user can ask follow-up questions
let lastContext = null;

// Send button click
SendButton.addEventListener('click', async () => {
        const text = Input.value.trim();
        const contextWindow = document.getElementById("ContextWindow");

        if (!text) {
                // show a small inline message instead of sending empty requests
                const err = document.createElement('div');
                err.classList.add('context-item', 'error');
                err.innerText = 'Please enter a URL to scrape.';
                contextWindow.appendChild(err);
                contextWindow.scrollTop = contextWindow.scrollHeight;
                return;
        }

        // Append user message immediately
        const userDiv = document.createElement('div');
        userDiv.classList.add('context-item', 'user');
        userDiv.innerText = text;
        contextWindow.appendChild(userDiv);

        // Create and append assistant placeholder div
        const assistantDiv = document.createElement('div');
        assistantDiv.classList.add('context-item', 'assistant');
        assistantDiv.innerHTML = '<span class="thinking">Thinking...</span>';
        contextWindow.appendChild(assistantDiv);
        contextWindow.scrollTop = contextWindow.scrollHeight;

        try {
                // If input looks like a URL, call /scrap; otherwise treat it as a follow-up question
                const isUrl = /^https?:\/\//i.test(text);
                if (isUrl) {
                        const encoded = encodeURIComponent(text);
                        const res = await fetch(`/scrap?url=${encoded}`);
                        let payload = null;
                        try { payload = await res.json(); } catch (e) { console.error('Failed to parse JSON response', e); }

                        if (!res.ok) {
                                const message = payload && payload.error ? payload.error : `Request failed: ${res.status}`;
                                assistantDiv.innerText = message;
                        } else {
                                const reply = payload && payload.data ? payload.data : 'No data returned.';
                                assistantDiv.innerText = reply;
                                // store the full context for follow-ups
                                lastContext = payload && payload.context ? payload.context : null;
                        }
                } else {
                        // follow-up question flow
                        if (!lastContext) {
                                assistantDiv.innerText = 'No context available. Please enter a URL first to scrape.';
                        } else {
                                const encodedQ = encodeURIComponent(text);
                                const res = await fetch(`/ask?question=${encodedQ}`);
                                let payload = null;
                                try { payload = await res.json(); } catch (e) { console.error('Failed to parse JSON response', e); }

                                if (!res.ok) {
                                        const message = payload && payload.error ? payload.error : `Request failed: ${res.status}`;
                                        assistantDiv.innerText = message;
                                } else {
                                        const reply = payload && payload.data ? payload.data : 'No answer returned.';
                                        assistantDiv.innerText = reply;
                                }
                        }
                }

        } catch (err) {
                console.error(err);
                assistantDiv.innerText = 'Network error while contacting server.';
        } finally {
                Input.value = '';
                Input.focus();
        }
});

// Enter key handling
Input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                SendButton.click();
        }
});

