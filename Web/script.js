const InputBox = document.querySelector(".InputBox");

function MoveDownInputBox() {
        InputBox.classList.add("Move_Down");

        const Instruction = document.getElementById("Instruction");
        Instruction.remove();

        const Input = document.getElementById("Input");
        Input.placeholder = "Type your message";
        Input.value = '';

        CreateChatBox();
}

InputBox.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                MoveDownInputBox();
        }
});
