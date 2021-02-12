## To generate the ssl cert

```
sudo snap install --classic certbot
sudo certbot certonly --manual --preferred-challenges dns
```

When prompted, enter the following info:

- email address: `code@umuzi.org`
- domain: `*.tilde.umuzi.org`

Use dns checker to check dns propagation:

https://dnschecker.org/#TXT/_acme-challenge.tilde.umuzi.org

Output should look like this:

```
IMPORTANT NOTES:

- Congratulations! Your certificate and chain have been saved at:
  /etc/letsencrypt/live/tilde.umuzi.org/fullchain.pem
  Your key file has been saved at:
  /etc/letsencrypt/live/tilde.umuzi.org/privkey.pem
  Your cert will expire on 2020-11-25. To obtain a new or tweaked
  version of this certificate in the future, simply run certbot
  again. To non-interactively renew _all_ of your certificates, run
  "certbot renew"
- Your account credentials have been saved in your Certbot
  configuration directory at /etc/letsencrypt. You should make a
  secure backup of this folder now. This configuration directory will
  also contain certificates and private keys obtained by Certbot so
  making regular backups of this folder is ideal.
- If you like Certbot, please consider supporting our work by:

  Donating to ISRG / Let's Encrypt: https://letsencrypt.org/donate
  Donating to EFF: https://eff.org/donate-le
```

## Renewing secrets

```
certbot renew --manual-auth-hook ./null.sh
```

We are using a dns based challenge, go add the txt record to the dns, and be quick about it

Go to the G cloud DNS console and edit the `_acme-challenge.tilde.umuzi.org` TXT record. Get the value from certbot.out.


Then delete and recreate the tls secrets:
```
kubectl delete secret tilde-domain-ssl      
```
You may need to delete and recreate the ingress

## Configuring cluster to use secrets

Followed : https://cloud.google.com/kubernetes-engine/docs/how-to/ingress-multi-ssl

To upload secrets to k8s:

```
CERT_CHAIN_PATH="/etc/letsencrypt/live/tilde.umuzi.org/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/tilde.umuzi.org/privkey.pem"

sudo cp $CERT_CHAIN_PATH .
sudo cp $KEY_PATH .

sudo chown $USER:$USER privkey.pem
sudo chown $USER:$USER fullchain.pem

kubectl create secret tls tilde-domain-ssl \
  --cert fullchain.pem --key privkey.pem

rm privkey.pem
rm fullchain.pem
```

kubectl describe ingress tilde-prod-ingress

curl http://backend.tilde.umuzi.org
curl -v https://backend.tilde.umuzi.org
