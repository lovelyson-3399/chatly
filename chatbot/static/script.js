const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');

function addMessage(content, sender) {
    const p = document.createElement('p');
    p.className = sender;
    p.innerText = content;
    chatbox.appendChild(p);
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
    const query = userInput.value.trim();
    if (!query) return;

    addMessage(query, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query }),
        });
        const data = await response.json();

        if (data.status === 'success') {
            addMessage(data.answer, 'bot');
        } else {
            addMessage(data.message || 'No relevant information found.', 'bot');
        }
    } catch (error) {
        addMessage('Error fetching response. Please try again.', 'bot');
    }
}
