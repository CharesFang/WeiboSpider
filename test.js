// create connection to initial mongodb container
conn = new Mongo("localhost:27017");
// db = conn.getDB("weibo");
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

// create another user
print("Enter passwd to for weibo database user.");

db = db.getSiblingDB('weibo');
print(`${db}`);

db.createUser(
    {
        user: "test",
        pwd: passwordPrompt(),
        roles: [
            { role: "readWrite", db: "weibo" }
        ]
    }
);

conn.close();


conn = new Mongo("localhost:27017");
db = conn.getDB('weibo');

// auth as weibo user
print(`Enter user weibo passwd.`);
var auth_res=db.auth("test", passwordPrompt());
if (!auth_res){
    print("auth failed.")
}else{
    print("auth as weibo");
    // db.createCollection('user');
    // db.createCollection('tweet');
    db.user.insertOne({test:123});
    printjson(db.adminCommand('listDatabases'));
    printjson(db.getCollectionNames());
}
conn.close();

// conn = new Mongo("localhost:27017");
// db = conn.getDB('weibo');



// conn.close();
// // auth as admin
// print("Enter passwd to auth as admin.");
// db.auth("admin", passwordPrompt());
// print();
//
// // create weibo user
// print(`Enter user weibo passwd.`);
// db.createUser(
//     {
//         user: "weibo",
//         pwd: passwordPrompt(),
//         roles: [
//             { role: "userAdmin", db: "weibo" }
//         ]
//     }
// );
//
// // set target database
// print("auth as weibo");
// var auth_res=db.auth("weibo", passwordPrompt());
// if (auth_res){
//     db = db.getSiblingDB('weibo');
//     print(`${db}`);
//     db.createCollection('user');
//     db.createCollection('tweet');
// }
//
// print("Database init finished.");