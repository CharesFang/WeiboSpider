// create connection to initial mongodb container
conn = new Mongo("localhost:27017");
// db = conn.getDB("weibo");
db = conn.getDB('admin');

// to initial administrator
// db = db.getSiblingDB('admin');
print(`Create datatabse: ${db}, and then enter administator passwd.`);

// create administrator
db.createUser(
    {
        user: "admin",
        pwd: passwordPrompt(),
        roles: [
            { role: "userAdminAnyDatabase", db: "admin" }
        ]
    }
);

// auth as admin
print("Enter passwd to auth as admin.");
db.auth("admin", passwordPrompt());
print();

// create weibo user
print(`Enter user weibo passwd.`);
db.createUser(
    {
        user: "weibo",
        pwd: passwordPrompt(),
        roles: [
            { role: "userAdmin", db: "weibo" }
        ]
    }
);

// set target database
print("auth as weibo");
var auth_res=db.auth("weibo", passwordPrompt());
if (auth_res){
    db = db.getSiblingDB('weibo');
    print(`${db}`);
    db.createCollection('user');
    db.createCollection('tweet');
}


// print("Enter passwd to auth as weibo.");
// db.auth("weibo", passwordPrompt());
// print();

// create collection




print("Database init finished.");