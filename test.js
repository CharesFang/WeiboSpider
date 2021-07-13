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
print();

// auth as admin
print("Enter passwd to auth as admin.");
db.auth("admin", passwordPrompt());
print();

// change database to weibo
db = db.getSiblingDB('weibo');

// create user for weibo database
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
print();

// create target collection
db.createCollection('user');
db.createCollection('tweet');
print("Successfully create collections.");

conn.close();
print("Mongodb initial finished.")
