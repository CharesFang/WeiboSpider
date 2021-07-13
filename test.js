/*
    create connection to initial mongodb container
*/

conn = new Mongo("localhost:27017");
db = conn.getDB('admin');

// to initial administrator
print(`Create datatabse: ${db}, and then enter administator passwd.`);

// create administrator
db.createUser(
    {
        user: "admin",
        pwd: passwordPrompt(),
        roles: [
            { role: "root", db: "admin" }
        ]
    }
);

// auth as admin
print("Enter passwd to auth as admin.");
db.auth("admin", passwordPrompt());


// change database to weibo
db = db.getSiblingDB('weibo');

// create another user
print("Enter passwd to for weibo database user.");
db.createUser(
    {
        user: "weibo",
        pwd: passwordPrompt(),
        roles: [
            { role: "readWrite", db: "weibo" }
        ]
    }
);

// close this connection
conn.close();

// create another connection and create collections
conn = new Mongo("localhost:27017");
db = conn.getDB('weibo');

// auth as weibo user
print(`Enter user weibo passwd.`);
var auth_res=db.auth("weibo", passwordPrompt());
if (!auth_res){
    print("auth failed.")
}else{
    print("auth as weibo");
    db.createCollection('user');
    db.createCollection('tweet');
}
conn.close();
