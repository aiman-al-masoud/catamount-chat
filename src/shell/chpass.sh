URL='http://127.0.0.1:5000'


curl -X POST "$URL/reset-password" \
        -H 'Content-Type: application/json' \
        -d '{ 
                "username" : "cammello",
                "old_pass" : "password",
                "new_pass" : "caciocavallo"
        }'