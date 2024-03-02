URL='http://127.0.0.1:5000'


curl -X POST "$URL/get-auth-token" \
        -H 'Content-Type: application/json' \
        -d '{ 
                "username" : "cammello",
                "password" : "password"
        }'