const InputBox = document.querySelector(".InputBox");
const SendButton = document.querySelector(".SendButton");
const Input = document.getElementById("Input");

// This variable will be 'true' initially and we'll set it to 'false' after the first message.
let isFirstMessage = true;

// Move down inputbox (This function is now only for the first-time setup)
// function MoveDownInputBox() {
//       const Instruction = document.getElementById("Instruction");
//       if (Instruction) Instruction.remove();

//        Input.placeholder = "Message...";
//          Input.value = '';
// }

// Send button click
SendButton.addEventListener('click', () => {
        const input = document.getElementById("Input");
        const text = input.value;
        fetch("/scrap?url=" + text).then(res => {
                res.json().then(data => {
                        console.info(data);
                        if (data) {
                                const contextWindow = document.getElementById("ContextWindow");
                                // Create and append assistant placeholder div
                                const assistantDiv = document.createElement('div');
                                assistantDiv.classList.add('context-item', 'assistant');
                                assistantDiv.innerHTML = '<span class="thinking">Thinking...</span>';
                                contextWindow.appendChild(assistantDiv);

                                // Create and append user message div
                                const userDiv = document.createElement('div');
                                userDiv.classList.add('context-item', 'user');
                                userDiv.innerText = data.data;
                                contextWindow.appendChild(userDiv);

                                

                                contextWindow.scrollTop = contextWindow.scrollHeight;

                                // Clear input and focus for the next message
                                Input.value = '';
                                Input.focus();
                        }

                }).catch(e => {
                        console.error(e);
                })
        }).catch(e => {
                console.error(e);
        });

 
});

// Enter key handling
Input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                SendButton.click();
        }
});

