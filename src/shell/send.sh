URL='http://127.0.0.1:5000'


curl -X POST "$URL/upload-message" \
        -H 'Content-Type: application/json' \
        -d '{ 
                "auth_token" : "false",
        "message" : { 
                "group_id" : "riunione", 
                "sender_id" : "capra",
                "text" : "buu ruuf !", 
                "date" : 0
                }
        }'