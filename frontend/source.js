class Agent {

    constructor() {

        this.input = document.getElementById("input");
        this.send = document.getElementById("send");
        this.chats = document.getElementById("chats");
        this.makingRequest = false;

        window.addEventListener("keydown", (e) => {
            if (e.key === 'Enter') {
                this.createResponse(this.input.value);
            }
        });

        this.send.addEventListener("click", () => {
            this.createResponse(this.input.value);
        });
    
    }

    createResponse(input) {

        if (input.trim() === "" || this.makingRequest) return;

        this.makingRequest = true;

        const userMessage = document.createElement("div");
        userMessage.className = "user-message";
        userMessage.textContent = input;
        this.chats.appendChild(userMessage);
        this.input.value = "";

        const response = document.createElement("div");
        response.className = "bot-message";
        response.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bot">
                <path d="M12 8V4H8" />
                <rect width="16" height="12" x="4" y="8" rx="2" />
                <path d="M2 14h2" />
                <path d="M20 14h2" />
                <path d="M15 13v2" />
                <path d="M9 13v2" />
            </svg>
            <div class="loading-indicator"></div>
        `;
        const chat = this.chats.appendChild(response);
        this.chats.scrollTop = this.chats.scrollHeight;

        (async () => {
            try {
                const res = await fetch(`http://localhost:8000/api/agent?request=${encodeURIComponent(input)}`);
                const data = await res.json();
                chat.querySelector(".loading-indicator").remove();
                chat.innerHTML += `<div>${marked.parse(data.response)}</div>`;
            } catch (error) {
                chat.querySelector(".loading-indicator").remove();
                chat.innerHTML += "<div>An error occurred!</div>";
            } finally {
                this.makingRequest = false;
                this.chats.scrollTop = this.chats.scrollHeight;
            }
        })();

    }


}

document.addEventListener('DOMContentLoaded', () => {
    new Agent();
});