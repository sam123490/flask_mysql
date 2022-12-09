from flask import redirect, session, request
from flask_app import app
from flask_app.models import post

@app.route('/create/post', methods=['POST'])
def create_post():
    if 'user_id' in session:
        data = {
            "content": request.form['content'],
            "user_id": session['user_id']
        }
        post.Post.save_post(data)
        return redirect('/wall')
    return redirect('/')