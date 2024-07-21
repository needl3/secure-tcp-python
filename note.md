1. Generate a AES private key ( Going to be password protected )
   ```bash
   openssl genrsa -aes-256-cbc -out server.key 2048
   ```
2. Remove the password protection to be used by test script
   ```bash
       cp server.key server.key.p
       openssl rsa -in server.key.p -provider default -provider legacy -passin pass:llll -out server.key
       rm server.key.p
   ```
3. Generate certificate signing request
   ```bash
      openssl req -new -key server.key -out server.csr
   ```
4. Sign this request with our aes key and output a certificate
   ```bash
       openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
   ```
