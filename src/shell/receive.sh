URL='http://127.0.0.1:5000'


curl -X POST "$URL/download-mailbox" \
        -H 'Content-Type: application/json' \
        -d '{ 
                "username" : "cammello",
                "auth_token" : "false"
        }'