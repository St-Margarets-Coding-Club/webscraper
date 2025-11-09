const InputBox = document.querySelector(".InputBox");
const SendButton = document.querySelector(".SendButton");
const Input = document.getElementById("Input");
const contextWindow = document.getElementById("ContextWindow");

// This variable will be 'true' initially and we'll set it to 'false' after the first message.
let isFirstMessage = true;

// Move down inputbox (This function is now only for the first-time setup)
function MoveDownInputBox() {
        const Instruction = document.getElementById("Instruction");
        if (Instruction) Instruction.remove();

        Input.placeholder = "Message...";
        Input.value = '';
}

// Send button click
SendButton.addEventListener('click', () => {
        const text = Input.value.trim();

        if (text) {
                // Create and append user message div
                const userDiv = document.createElement('div');
                userDiv.classList.add('context-item', 'user');
                userDiv.innerText = text;
                contextWindow.appendChild(userDiv);

                // Create and append assistant placeholder div
                const assistantDiv = document.createElement('div');
                assistantDiv.classList.add('context-item', 'assistant');
                assistantDiv.innerHTML = '<span class="thinking">Thinking...</span>';
                contextWindow.appendChild(assistantDiv);

                if (isFirstMessage) {
                        MoveDownInputBox();
                        isFirstMessage = false;
                }

                contextWindow.scrollTop = contextWindow.scrollHeight;

                // Clear input and focus for the next message
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
