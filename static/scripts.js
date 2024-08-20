async function createUser() {
    const username = document.getElementById('username').value;
    const response = await fetch('/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: Date.now().toString(), username: username })
    });
    const result = await response.json();
    alert(result.message);
}

async function createChannel() {
    const channelName = document.getElementById('channel-name').value;
    const response = await fetch('/create_channel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ channel_id: Date.now().toString(), channel_name: channelName })
    });
    const result = await response.json();
    alert(result.message);
    loadChannels();
}

async function sendMessage() {
    const channelSelect = document.getElementById('channel-select');
    const channelId = channelSelect.options[channelSelect.selectedIndex].value;
    const message = document.getElementById('message').value;
    const response = await fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ channel_id: channelId, user_id: 'owner', message: message })
    });
    const result = await response.json();
    alert(result.message);
    loadMessages(channelId);
}

async function loadChannels() {
    const response = await fetch('/get_channels');
    const channels = await response.json();
    const channelSelect = document.getElementById('channel-select');
    channelSelect.innerHTML = '';
    channels.forEach(channel => {
        const option = document.createElement('option');
        option.value = channel.channel_id;
        option.text = channel.channel_name;
        channelSelect.add(option);
    });
}

async function loadMessages(channelId) {
    const response = await fetch(`/get_messages/${channelId}`);
    const result = await response.json();
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = '';
    result.messages.forEach(msg => {
        const messageElement = document.createElement('div');
        messageElement.textContent = `${msg.user_id}: ${msg.message}`;
        messagesDiv.appendChild(messageElement);
    });
}

window.onload = function() {
    loadChannels();
};

