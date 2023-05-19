from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
ca = certifi.where()
app = Flask(__name__)

client = MongoClient('mongodb+srv://sparta:test@cluster0.1ygt7yh.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result': buckets})

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    doc ={
        'bucket': bucket_receive
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

@app.route("/bucket/del", methods=["POST"])
def bucket_del():
    bucket_receive = request.form['bucket_give']
    doc ={
        'bucket': bucket_receive
    }
    db.bucket.delete_one(doc)
    return jsonify({'msg': '삭제 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done_post():
    bucket_receive = request.form['bucket_give']
    doc ={
        'bucket': bucket_receive
    }
    db.bucket_done.insert_one(doc)
    return jsonify({'msg': '버킷 달성 완료!'})

@app.route("/bucket/done", methods=["GET"])
def bucket_done_get():
    buckets = list(db.bucket_done.find({},{'_id':False}))
    return jsonify({'result': buckets})

@app.route("/bucket/edit", methods=["POST"])
def bucket_edit():
    edit_bucket_receive = request.form['edit_bucket_give']
    bucket_receive = request.form['bucket_give']
    
    doc ={
        'bucket': edit_bucket_receive
    }
    db.bucket.update_one({'bucket':bucket_receive},{'$set':doc})
    return jsonify({'msg': '수정 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)