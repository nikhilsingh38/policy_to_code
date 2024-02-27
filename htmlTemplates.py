css = '''
<style>
.chat-message {
    paddingborder-radius: 0.5rem; display: flex
}
.chat-message.bot {
    background-color: #1a1c24
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 20px;
  max-height: 20px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 100%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
</div>
'''
